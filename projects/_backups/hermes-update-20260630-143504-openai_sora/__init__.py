"""OpenAI Sora Videos API backend for Hermes video_generate.

Uses OpenAI's asynchronous Videos API:
  POST /v1/videos -> poll GET /v1/videos/{id} -> download GET /v1/videos/{id}/content

Authentication: OPENAI_API_KEY. VOICE_TOOLS_OPENAI_KEY is accepted as a local
fallback so existing voice tooling keys can be reused if they have Videos API
access, but OPENAI_API_KEY is the setup-schema source of truth.
"""

from __future__ import annotations

import json
import logging
import mimetypes
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from agent.video_gen_provider import VideoGenProvider, error_response, save_bytes_video, success_response

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "sora-2"
PRO_MODEL = "sora-2-pro"
DEFAULT_TIMEOUT_SECONDS = int(os.getenv("OPENAI_SORA_TIMEOUT_SECONDS", "900"))
DEFAULT_POLL_INTERVAL_SECONDS = int(os.getenv("OPENAI_SORA_POLL_INTERVAL_SECONDS", "8"))

MODELS: Dict[str, Dict[str, Any]] = {
    "sora-2": {
        "display": "Sora 2",
        "speed": "minutes",
        "strengths": "Fast iteration, social clips, rough cuts, flexible prompt exploration.",
        "price": "OpenAI API billing",
        "modalities": ["text", "image"],
    },
    "sora-2-pro": {
        "display": "Sora 2 Pro",
        "speed": "slower",
        "strengths": "Production-quality output, higher fidelity, 1080p vertical/horizontal exports.",
        "price": "OpenAI API billing — premium",
        "modalities": ["text", "image"],
    },
}


def _api_key() -> str:
    return (os.getenv("OPENAI_API_KEY") or os.getenv("VOICE_TOOLS_OPENAI_KEY") or "").strip()


def _base_url() -> str:
    return (os.getenv("OPENAI_BASE_URL") or DEFAULT_BASE_URL).strip().rstrip("/")


def _headers(api_key: str, *, json_content: bool = True) -> Dict[str, str]:
    headers = {"Authorization": f"Bearer {api_key}", "User-Agent": "hermes-agent/video_gen/openai-sora"}
    if json_content:
        headers["Content-Type"] = "application/json"
    return headers


def _resolve_model(explicit: Optional[str], resolution: str) -> str:
    candidates = [explicit, os.getenv("OPENAI_SORA_MODEL")]
    try:
        from hermes_cli.config import load_config

        cfg = load_config()
        vg = cfg.get("video_gen") if isinstance(cfg, dict) else None
        if isinstance(vg, dict):
            sora_cfg = vg.get("openai_sora") if isinstance(vg.get("openai_sora"), dict) else {}
            if isinstance(sora_cfg, dict):
                candidates.append(sora_cfg.get("model"))
            candidates.append(vg.get("model"))
    except Exception:
        pass
    for c in candidates:
        if isinstance(c, str) and c.strip() in MODELS:
            return c.strip()
    if resolution == "1080p":
        return PRO_MODEL
    return DEFAULT_MODEL


def _size_for(aspect_ratio: str, resolution: str, model: str) -> str:
    # OpenAI docs show Sora 2 Pro for 1920x1080 / 1080x1920. Use 720p for
    # fast/default Sora 2 runs and 1080p only when Pro is selected/requested.
    high = resolution == "1080p" or model == PRO_MODEL
    if aspect_ratio == "9:16":
        return "1080x1920" if high else "720x1280"
    if aspect_ratio == "1:1":
        return "1024x1024" if high else "720x720"
    # Default to landscape for unsupported ratios; the common Hermes tool schema
    # includes more ratios than Sora currently documents.
    return "1920x1080" if high else "1280x720"


def _seconds_for(duration: Optional[int]) -> str:
    if duration is None:
        return "8"
    # Sora docs currently show 8s examples and 16/20s support. Keep short clips
    # as the default for Shorts assembly, clamp outliers.
    value = max(4, min(20, int(duration)))
    return str(value)


def _multipart_form(fields: Dict[str, str], files: Optional[Dict[str, Tuple[str, bytes, str]]] = None) -> Tuple[bytes, str]:
    boundary = f"----hermes-openai-sora-{int(time.time() * 1000)}"
    chunks: List[bytes] = []
    for name, value in fields.items():
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        chunks.append(str(value).encode())
        chunks.append(b"\r\n")
    for name, (filename, data, content_type) in (files or {}).items():
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode())
        chunks.append(f"Content-Type: {content_type}\r\n\r\n".encode())
        chunks.append(data)
        chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), boundary


def _read_image_ref(image_url: str) -> Tuple[str, bytes, str]:
    ref = image_url.strip()
    if ref.startswith(("http://", "https://")):
        with urllib.request.urlopen(ref, timeout=60) as resp:
            data = resp.read()
            ctype = resp.headers.get_content_type() or "image/png"
        filename = Path(urllib.parse.urlparse(ref).path).name or "reference.png"
        return filename, data, ctype
    path = Path(ref).expanduser()
    data = path.read_bytes()
    ctype = mimetypes.guess_type(path.name)[0] or "image/png"
    return path.name or "reference.png", data, ctype


def _request_json(method: str, url: str, api_key: str, payload: Optional[Dict[str, Any]] = None, timeout: int = 60) -> Dict[str, Any]:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=_headers(api_key), method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _raise_api_error(exc: urllib.error.HTTPError) -> str:
    try:
        body = exc.read().decode("utf-8", errors="replace")
    except Exception:
        body = ""
    return f"HTTP {exc.code}: {body[:800]}"


class OpenAISoraVideoGenProvider(VideoGenProvider):
    @property
    def name(self) -> str:
        return "openai-sora"

    @property
    def display_name(self) -> str:
        return "OpenAI Sora"

    def is_available(self) -> bool:
        return bool(_api_key())

    def list_models(self) -> List[Dict[str, Any]]:
        return [{"id": mid, **meta} for mid, meta in MODELS.items()]

    def default_model(self) -> Optional[str]:
        return DEFAULT_MODEL

    def capabilities(self) -> Dict[str, Any]:
        return {
            "modalities": ["text", "image"],
            "aspect_ratios": ["16:9", "9:16", "1:1"],
            "resolutions": ["720p", "1080p"],
            "min_duration": 4,
            "max_duration": 20,
            "supports_audio": True,
            "supports_negative_prompt": False,
            "max_reference_images": 1,
        }

    def get_setup_schema(self) -> Dict[str, Any]:
        return {
            "name": "OpenAI Sora",
            "badge": "paid",
            "tag": "Sora 2 / Sora 2 Pro via OpenAI Videos API — text-to-video and first-frame image-to-video",
            "env_vars": [
                {
                    "key": "OPENAI_API_KEY",
                    "prompt": "OpenAI API key with Videos/Sora API access",
                    "url": "https://platform.openai.com/api-keys",
                },
            ],
        }

    def generate(
        self,
        prompt: str,
        *,
        model: Optional[str] = None,
        image_url: Optional[str] = None,
        reference_image_urls: Optional[List[str]] = None,
        duration: Optional[int] = None,
        aspect_ratio: str = "16:9",
        resolution: str = "720p",
        negative_prompt: Optional[str] = None,
        audio: Optional[bool] = None,
        seed: Optional[int] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        api_key = _api_key()
        if not api_key:
            return error_response(
                error="OPENAI_API_KEY is not set. ChatGPT/Sora UI subscription access is not the same as API access; add an OpenAI API key with Videos API access.",
                error_type="auth_required",
                provider=self.name,
                prompt=prompt,
            )
        prompt = (prompt or "").strip()
        if not prompt:
            return error_response(error="prompt is required", error_type="missing_prompt", provider=self.name)

        model_id = _resolve_model(model, resolution)
        size = _size_for(aspect_ratio, resolution, model_id)
        seconds = _seconds_for(duration)
        fields = {"model": model_id, "prompt": prompt, "size": size, "seconds": seconds}
        if audio is not None:
            # Sora models include audio capabilities; if the API ignores this
            # field, it will fail clearly rather than silently changing output.
            fields["audio"] = "true" if audio else "false"

        files = None
        modality = "text"
        ref = (image_url or "").strip() or None
        if ref:
            try:
                filename, data, ctype = _read_image_ref(ref)
                # The Videos guide describes images as first-frame references;
                # current SDK/cURL examples use multipart/form-data. The field
                # name is intentionally conservative and may need adjustment if
                # OpenAI changes the beta surface.
                files = {"image": (filename, data, ctype)}
                modality = "image"
            except Exception as exc:
                return error_response(
                    error=f"Could not read image_url for Sora image-to-video: {exc}",
                    error_type="bad_image_reference",
                    provider=self.name,
                    model=model_id,
                    prompt=prompt,
                )

        try:
            body, boundary = _multipart_form(fields, files)
            req = urllib.request.Request(
                f"{_base_url()}/videos",
                data=body,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": f"multipart/form-data; boundary={boundary}", "User-Agent": "hermes-agent/video_gen/openai-sora"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=90) as resp:
                job = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            return error_response(error=f"OpenAI Sora job creation failed: {_raise_api_error(exc)}", error_type="api_error", provider=self.name, model=model_id, prompt=prompt)
        except Exception as exc:
            return error_response(error=f"OpenAI Sora job creation failed: {exc}", error_type="api_error", provider=self.name, model=model_id, prompt=prompt)

        video_id = job.get("id")
        if not video_id:
            return error_response(error=f"OpenAI Sora response missing id: {job}", error_type="empty_response", provider=self.name, model=model_id, prompt=prompt)

        deadline = time.time() + DEFAULT_TIMEOUT_SECONDS
        status = str(job.get("status") or "queued")
        last = job
        try:
            while time.time() < deadline:
                if status == "completed":
                    break
                if status in {"failed", "cancelled", "canceled"}:
                    return error_response(error=f"OpenAI Sora generation {status}: {last}", error_type="generation_failed", provider=self.name, model=model_id, prompt=prompt)
                time.sleep(DEFAULT_POLL_INTERVAL_SECONDS)
                last = _request_json("GET", f"{_base_url()}/videos/{video_id}", api_key, timeout=60)
                status = str(last.get("status") or "")
            if status != "completed":
                return error_response(error=f"OpenAI Sora generation timed out after {DEFAULT_TIMEOUT_SECONDS}s; last status={status}", error_type="timeout", provider=self.name, model=model_id, prompt=prompt)

            content_req = urllib.request.Request(f"{_base_url()}/videos/{video_id}/content", headers=_headers(api_key, json_content=False), method="GET")
            with urllib.request.urlopen(content_req, timeout=180) as resp:
                raw = resp.read()
            path = save_bytes_video(raw, prefix="openai_sora", extension="mp4")
        except urllib.error.HTTPError as exc:
            return error_response(error=f"OpenAI Sora polling/download failed: {_raise_api_error(exc)}", error_type="api_error", provider=self.name, model=model_id, prompt=prompt)
        except Exception as exc:
            return error_response(error=f"OpenAI Sora polling/download failed: {exc}", error_type="api_error", provider=self.name, model=model_id, prompt=prompt)

        return success_response(
            video=str(path),
            model=model_id,
            prompt=prompt,
            modality=modality,
            aspect_ratio=aspect_ratio,
            duration=int(seconds),
            provider=self.name,
            extra={"video_id": video_id, "size": size, "status": status},
        )


def register(ctx):
    ctx.register_video_gen_provider(OpenAISoraVideoGenProvider())

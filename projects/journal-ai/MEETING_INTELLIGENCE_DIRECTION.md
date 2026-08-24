# Journal AI Meeting Intelligence Architecture

Journal AI is the durable, privacy-first reflection product. `local-meeting-transcriber` should be preserved as source material and migrated as a Journal AI capability, not nested as a second standalone app.

## Source audit

Canonical source paths reviewed:

- `/opt/data/HeRmEz/projects/local-meeting-transcriber` — tracked inside the main `HeRmEz` repository history; keep this as the canonical local workspace until migration slices are verified.
- `/opt/data/kanban/workspaces/t_d9fceed6/local-meeting-transcriber` — older Kanban scratch copy with generated Expo output and node_modules; not a Git repo and not the source of truth.

History preservation decision:

- Do not archive or delete `projects/local-meeting-transcriber` yet.
- Preserve migration traceability by referencing original file paths in Journal AI implementation PRs/tasks.
- If source is eventually archived, first move it with Git history intact or retain a documented commit reference in Journal AI docs.

License status:

- No top-level `LICENSE` file was found in `projects/local-meeting-transcriber`.
- Dependency licenses are visible in lockfiles/package metadata, but the project code itself has no explicit reuse license. Because it is under the same owner/workspace, internal migration is acceptable; public redistribution should add/confirm a project license first.
- WhisperX, pyannote.audio, Ollama, Expo, .NET/EF, Terraform/Azure provider licenses and model licenses must be checked at implementation time before bundling models or publishing a hosted product.

## Reusable pieces from Local Meeting Transcriber

### Backend API (.NET/ASP.NET Core)

Source:

- `Backend/src/api/Controllers/AuthController.cs`
- `Backend/src/api/Controllers/MeetingsController.cs`
- `Backend/src/api/Models/Meeting.cs`
- `Backend/src/api/Models/AppDbContext.cs`
- `Backend/src/api/DTOs/*`

Reusable ideas:

- Authenticated meeting ownership using user-scoped records.
- Basic upload/list/detail route shape: `/api/meetings/upload`, `/api/meetings`, `/api/meetings/{id}`.
- Meeting aggregate with audio path, transcript, diarized transcript, summary, creation timestamp.
- SQLite-friendly EF migrations as a reference for local/dev storage.

Do not directly import without redesign:

- Upload processing runs inline during the HTTP request; Journal AI needs asynchronous job state with retry/cancel.
- `Meeting.AudioPath` stores raw server paths; Journal AI should store opaque file ids and use short-lived signed URLs.
- `/file/{name}` serves files by basename without an ownership check; Journal AI must authorize every audio/transcript download.
- The current schema mixes raw audio, transcript, diarization, summary, and durable journal reflection in one row; Journal AI needs separate retention/delete controls.

### Expo/mobile recording UI

Source:

- `Frontend/src/screens/Record.native.tsx`
- `Frontend/src/screens/Record.web.tsx`
- `Frontend/src/screens/Meetings.tsx`
- `Frontend/src/screens/MeetingDetail.tsx`
- `Frontend/src/services/api.ts`
- `Frontend/src/utils/storage.ts`

Reusable ideas:

- Expo `expo-av` native recording flow.
- Web `MediaRecorder` fallback for browser recording.
- Meeting list/detail navigation pattern.
- Local secure-token storage abstraction.

Do not directly import without redesign:

- No explicit participant-consent attestation before recording starts.
- Native recording immediately uploads on stop in the primary path.
- Demo login accepts any password and stores mock JWTs; this must stay out of production Journal AI.
- UI displays local recording URIs and uses verbose console logs around private audio actions; production logs should avoid paths and sensitive metadata.

### WhisperX / pyannote transcription and diarization

Source:

- `Backend/src/api/Services/TranscriptionService.cs`
- `Backend/src/api/scripts/whisperx_runner.py`
- `script.sh` duplicate scaffold

Reusable ideas:

- Python subprocess adapter behind a backend service boundary.
- WhisperX base model transcription, alignment, and optional pyannote diarization when `HF_TOKEN` is configured.
- JSON result contract returning transcript and speaker-labeled transcript.

Do not directly import without redesign:

- Script assumes local Python/torch/whisperx availability and no dependency lockfile.
- Diarization labels are generic (`Speaker?`/model labels) and must remain uncertain; Journal AI must never invent identities.
- No chunking, timeout, cancellation, resource limits, model warmup, GPU/CPU policy, or structured error taxonomy.
- Hugging Face token/model-license requirements are implicit; Journal AI must gate diarization setup behind explicit local configuration.

### Ollama summarization

Source:

- `Backend/src/api/Services/SummaryService.cs`

Reusable ideas:

- Local Ollama endpoint (`http://localhost:11434/api/generate`) for private summarization.
- Summary prompt extracts decisions, action items, and blockers.

Do not directly import without redesign:

- Prompt injects raw transcript directly into instructions. Journal AI needs a prompt-injection boundary: transcript is untrusted data, model output must cite source spans, and no summary/action item should become a durable journal insight until user-reviewed.
- No unavailable-model handling, retry/backoff, timeout, partial response handling, or user-visible degraded state.
- No provenance fields tying claims back to transcript segment ids.

### Terraform/Azure scaffold

Source:

- `infra/main.tf`
- `infra/variables.tf`
- `infra/outputs.tf`

Reusable ideas:

- Minimal Azure resource group + Linux App Service plan + app settings scaffold.
- Secret-bearing values passed as Terraform variables, not literals.

Do not directly import without redesign:

- `Backend.csproj` targets `net9.0` while Terraform config sets `dotnet_version = "8.0"`; runtime alignment is unresolved.
- No database, private storage account, managed identity, Key Vault, logs redaction, queue worker, or audio retention policy.
- Hosted transcription is likely a poor default for private meeting audio; Journal AI should default local-first and treat cloud processing as opt-in.

## Journal AI target boundaries

Journal AI should own these product boundaries:

1. Identity and consent
   - The user must explicitly attest that recording is allowed before capture/import.
   - Show a visible recording state on all platforms.
   - No covert/background recording.

2. Storage and retention
   - Store raw audio, normalized audio, transcript segments, diarization labels, summaries, embeddings, journal reflections, and exports as separate artifacts.
   - Each artifact type needs delete/export/retention controls.
   - Raw audio should be deletable while retaining a user-approved transcript or reflection.

3. Processing jobs
   - Upload/import creates a `meeting_processing_job` with states such as `queued`, `normalizing`, `transcribing`, `diarizing`, `summarizing`, `needs_review`, `failed`, `cancelled`, `completed`.
   - Jobs need retry/cancel, timeout, progress, and structured errors.
   - Processing adapters should be replaceable: local Whisper/faster-whisper/WhisperX first; external providers only by explicit configuration.

4. Transcript and diarization review
   - Speaker labels are provisional (`Speaker 1`, `Speaker 2`) until the user names or merges them.
   - Store confidence/uncertainty where available.
   - Allow user editing before derived summaries become durable.

5. AI insight boundary
   - Treat transcripts as untrusted input.
   - Summaries, decisions, commitments, risks, and reflection prompts must cite transcript segments.
   - Do not fabricate commitments, motives, diagnoses, emotion certainty, or speaker identities.
   - User chooses what enters the journal.

6. Mobile/web experience
   - Journal AI remains the primary UI.
   - Meeting intelligence appears as a recording/import/reflection flow inside Journal AI, alongside written journals and dream logs.
   - Public demo can show seeded/sample meetings; real recording/transcription is local/private by default.

## Migration map for the next implementation card

The child card `Journal AI: implement consented meeting recording, transcription, and diarization` should use this map:

- Build new Journal AI domain models rather than copying the LMT `Meeting` table wholesale:
  - `meeting_sources` or equivalent for uploaded/imported audio metadata.
  - `meeting_processing_jobs` for async work and errors.
  - `transcript_segments` with timestamps, text, source span, and optional speaker label id.
  - `speaker_labels` with user-edited display names and confidence/uncertainty.
  - `meeting_summaries` / `journal_reflection_links` only after user review.
- Reuse Expo/native/web recording patterns only after adding consent UX and a non-auto-upload review step.
- Wrap WhisperX/pyannote behind a Journal AI adapter interface; add dependency/setup checks before enabling.
- Wrap Ollama summarization behind a provenance-aware summarizer that cites transcript segments and fails closed.
- Keep Terraform as reference only; do not deploy audio processing to shared cloud until storage, secrets, worker queue, and retention controls exist.

## Security and privacy gaps to close before production

- Missing explicit participant consent flow.
- Demo/mock JWT login fallback in frontend.
- File download endpoint lacks per-user authorization.
- Raw filesystem paths are stored and can leak through DTOs/logs.
- Inline request processing can hang uploads and exposes private audio to retry ambiguity.
- No malware/file-type validation, size policy beyond request limit, duration cap, or quarantine for uploads.
- No encryption-at-rest design for raw audio/transcripts/embeddings.
- No export/delete path for derived artifacts.
- No prompt-injection isolation for transcripts sent to Ollama.
- No cited/provenance-backed summaries; summaries can currently become uncited assertions.
- No license/model acceptance workflow for pyannote/Hugging Face-gated diarization.
- No production-ready cloud storage/key/worker topology.

## Completion gates

- Source/license audit documented here.
- Consent-first recording/import flow.
- Secure upload/import with file validation and artifact-level retention.
- Async job state machine with retry/cancel/failure states.
- Local-first transcription adapter and diarization adapter with uncertainty.
- User-reviewed transcript editing and speaker label correction.
- Cited summaries/actions/reflections with prompt-injection boundary.
- Journal linkage only after user approval.
- Export/delete coverage for audio, transcripts, summaries, embeddings, and journal links.
- Mobile/web QA and deterministic tests.

## Archive rule

Do not archive `projects/local-meeting-transcriber` until Journal AI has verified replacement behavior for the migrated slices, this document points to the replacement paths, and the source history remains reachable.

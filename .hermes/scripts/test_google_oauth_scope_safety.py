import importlib.util
import unittest


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROFILE = load("google_profile_oauth", "/opt/data/scripts/google_profile_oauth.py")
WORKFLOW = load("google_reauth_workflow", "/opt/data/scripts/google_reauth_workflow.py")


class OAuthScopeSafetyTests(unittest.TestCase):
    def test_workspace_grant_rejects_any_missing_canonical_scope(self):
        required = PROFILE.FULL_WORKSPACE_SCOPES
        granted = required[:-1]
        self.assertEqual(PROFILE.missing_required_scopes(granted, required), [required[-1]])

    def test_workspace_grant_accepts_canonical_scope_bundle(self):
        required = PROFILE.FULL_WORKSPACE_SCOPES
        self.assertEqual(PROFILE.missing_required_scopes(list(reversed(required)), required), [])

    def test_workspace_verification_fails_when_any_probe_fails(self):
        result = {
            "valid": True, "identity_match": True, "scope_complete": True,
            "has_refresh_token": True,
            "probes": {"gmail_profile": {"ok": True}, "calendar": {"ok": False}, "drive": {"ok": True}},
        }
        self.assertFalse(WORKFLOW.workspace_verification_ok(result))

    def test_workspace_verification_requires_refresh_token_for_durable_auth(self):
        result = {
            "valid": True, "identity_match": True, "scope_complete": True,
            "has_refresh_token": False, "probes": {"gmail_profile": {"ok": True}},
        }
        self.assertFalse(WORKFLOW.workspace_verification_ok(result))

    def test_workspace_verification_passes_only_complete_identity_and_probes(self):
        result = {
            "valid": True, "identity_match": True, "scope_complete": True,
            "has_refresh_token": True,
            "probes": {name: {"ok": True} for name in
                       ["gmail_profile", "gmail_labels", "calendar", "drive", "contacts"]},
        }
        self.assertTrue(WORKFLOW.workspace_verification_ok(result))


if __name__ == "__main__":
    unittest.main()

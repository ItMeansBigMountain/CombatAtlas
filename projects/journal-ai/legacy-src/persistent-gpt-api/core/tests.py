import json
from pathlib import Path

from django.test import SimpleTestCase
from django.urls import reverse

PROJECT_DIR = Path(__file__).resolve().parents[1]


class HealthCheckTests(SimpleTestCase):
    def test_health_check_returns_ok_json(self):
        response = self.client.get(reverse("health-check"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.json(), {"status": "ok", "service": "journal-ai-api"})


class VercelDeploymentConfigTests(SimpleTestCase):
    def test_dependency_manifests_are_present(self):
        requirements = (PROJECT_DIR / "requirements.txt").read_text()
        pyproject = (PROJECT_DIR / "pyproject.toml").read_text()

        self.assertIn("Django>=5.1,<5.3", requirements)
        self.assertIn('name = "journal-ai-api"', pyproject)
        self.assertIn('requires-python = ">=3.11"', pyproject)

    def test_vercel_json_routes_all_requests_to_serverless_wsgi_entry(self):
        config_path = PROJECT_DIR / "vercel.json"
        self.assertTrue(config_path.exists(), "vercel.json is required for Vercel deployment")

        config = json.loads(config_path.read_text())
        self.assertEqual(config["builds"], [{"src": "api/index.py", "use": "@vercel/python"}])
        self.assertIn({"src": "/(.*)", "dest": "api/index.py"}, config["routes"])

    def test_vercel_wsgi_entry_exposes_application(self):
        entry_path = PROJECT_DIR / "api" / "index.py"
        self.assertTrue(entry_path.exists(), "api/index.py is required for Vercel Python runtime")

        entry_source = entry_path.read_text()
        self.assertIn("DJANGO_SETTINGS_MODULE", entry_source)
        self.assertIn("Persistent_GPT_api.settings", entry_source)
        self.assertIn("application = get_wsgi_application()", entry_source)

from django.conf import settings
from django.test import SimpleTestCase, TestCase


class RuntimeSettingsTests(SimpleTestCase):
    def test_local_runtime_settings_are_safe_and_test_client_friendly(self):
        self.assertTrue(settings.SECRET_KEY)
        self.assertNotEqual(settings.SECRET_KEY, "")
        self.assertIn("testserver", settings.ALLOWED_HOSTS)
        self.assertIn("localhost", settings.ALLOWED_HOSTS)
        self.assertEqual(settings.DATABASES["default"]["ENGINE"], "django.db.backends.sqlite3")


class EndpointSmokeTests(TestCase):
    def test_root_endpoint_returns_welcome(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"welcome!")

    def test_workout_keys_endpoint_returns_categories(self):
        response = self.client.get("/api/workout-keys")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertGreater(len(response.json()), 0)

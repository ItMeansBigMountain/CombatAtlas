from django.test import TestCase
from rest_framework.test import APIClient

from .models import DrillCategory, DrillExercise, MartialArt


class PublicCatalogApiTests(TestCase):
    def setUp(self):
        art = MartialArt.objects.create(
            name="Boxing",
            sport_type="striking",
            description="Test art",
        )
        category = DrillCategory.objects.create(
            name="Footwork",
            martial_art=art,
            description="Test category",
        )
        self.drill = DrillExercise.objects.create(
            name="Step and jab",
            difficulty_level="beginner",
            drill_type="technical",
            category=category,
            description="Test drill",
        )
        self.client = APIClient()

    def test_catalog_endpoints_are_publicly_readable(self):
        for path in ("/martialarts/", "/drillcategories/", "/drillexercises/"):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data["count"], 1)

    def test_random_drill_can_filter_by_martial_art(self):
        response = self.client.get(
            "/drillexercises/random/",
            {"martial_art": self.drill.category.martial_art_id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Step and jab")

    def test_anonymous_catalog_writes_are_rejected(self):
        response = self.client.post(
            "/martialarts/",
            {"name": "Judo", "sport_type": "grappling", "description": "Test"},
        )
        self.assertIn(response.status_code, (401, 403))

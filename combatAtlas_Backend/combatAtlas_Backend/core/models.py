from django.db import models


class MartialArt(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sport_type = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to="martial_art/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class DrillCategory(models.Model):
    name = models.CharField(max_length=100)
    martial_art = models.ForeignKey(
        MartialArt,
        on_delete=models.CASCADE,
        related_name="categories"
    )
    description = models.TextField()
    image = models.ImageField(upload_to="drill_categories/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("name", "martial_art")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.martial_art.name})"


class DrillExercise(models.Model):
    name = models.CharField(max_length=100)
    difficulty_level = models.CharField(max_length=50)
    drill_type = models.CharField(max_length=100)
    category = models.ForeignKey(
        DrillCategory,
        on_delete=models.CASCADE,
        related_name="drills"
    )
    description = models.TextField()
    image = models.ImageField(upload_to="drill_exercise/", null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("name", "category")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.category.name})"

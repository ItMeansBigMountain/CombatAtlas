from django.db import models





CATEGORY_CHOICES = (
    ('Abs', 'Abs'),
    ('Arms', 'Arms'),
    ('Back', 'Back'),
    ('Chest', 'Chest'),
    ('Shoulders', 'Shoulders'),
    ('butt-hips', 'butt-hips'),
    ('full-body-integrated', 'full-body-integrated'),
    ('legs-calves-and-shins', 'legs-calves-and-shins'),
    ('legs-thighs', 'legs-thighs'),
    ('Neck', 'Neck'),
)





class Workout(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=3000 , null = True) 
    author = models.CharField(max_length=100 , default=None)
    email = models.EmailField(max_length=100 , default=None)
    phone = models.CharField(max_length=10, default=None)
    date = models.DateTimeField(auto_now_add=True)
    # img = models.ImageField(blank=True, null=True, upload_to="media")
    img_uri = models.CharField(max_length=999999)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=128)
    community_contrib = models.BooleanField(default=False)


    def __str__(self):
        return self.title



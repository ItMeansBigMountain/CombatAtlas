from . import views
from django.urls import include, path
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"martialarts", views.MartialArtViewSet)
router.register(r"drillcategories", views.DrillCategoryViewSet)
router.register(r"drillexercises", views.DrillExerciseViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
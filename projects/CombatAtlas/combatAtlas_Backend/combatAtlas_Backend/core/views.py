from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import Group, User
from django.db.models import QuerySet
import random

from .models import MartialArt, DrillCategory, DrillExercise
from .serializers import (
    MartialArtSerializer,
    DrillCategoriesSerializer,
    DrillExerciseSerializer,
    UserSerializer,
    GroupSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class MartialArtViewSet(viewsets.ModelViewSet):
    queryset = MartialArt.objects.all()
    serializer_class = MartialArtSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["get"])
    def categories(self, request, pk=None):
        categories = DrillCategory.objects.filter(martial_art=pk)
        serializer = DrillCategoriesSerializer(categories, many=True)
        return Response(serializer.data)


class DrillCategoryViewSet(viewsets.ModelViewSet):
    queryset = DrillCategory.objects.all()
    serializer_class = DrillCategoriesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["get"])
    def drills(self, request, pk=None):
        drills = DrillExercise.objects.filter(category=pk)
        serializer = DrillExerciseSerializer(drills, many=True)
        return Response(serializer.data)


class DrillExerciseViewSet(viewsets.ModelViewSet):
    queryset = DrillExercise.objects.all()
    serializer_class = DrillExerciseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"])
    def random(self, request):
        martial_art = request.query_params.get("martial_art")
        category = request.query_params.get("category")

        queryset: QuerySet = DrillExercise.objects.all()

        if martial_art:
            queryset = queryset.filter(category__martial_art=martial_art)

        if category:
            queryset = queryset.filter(category=category)

        if not queryset.exists():
            return Response({"detail": "No drills found."}, status=404)

        drill = random.choice(queryset)
        serializer = self.get_serializer(drill)
        return Response(serializer.data)

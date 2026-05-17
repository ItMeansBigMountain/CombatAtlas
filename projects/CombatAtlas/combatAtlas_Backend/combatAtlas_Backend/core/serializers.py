from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import MartialArt, DrillCategory, DrillExercise


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]

class MartialArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = MartialArt
        fields = '__all__'

class DrillCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrillCategory
        fields = '__all__'

class DrillExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrillExercise
        fields = '__all__'
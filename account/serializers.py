from rest_framework import serializers
from .models import Position, Faculty, Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name',]


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['name',]



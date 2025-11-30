from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


    def validate_importance(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError("Importance must be between 1 and 10")
        return value

    def validate_estimated_hours(self, value):
        if value <= 0:
            raise serializers.ValidationError("Estimated hours must be > 0")
        return value
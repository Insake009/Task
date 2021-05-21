from rest_framework import serializers
from .models import Category, Task


class TaskSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = Task
        fields = ['id', 'category_id', 'title', 'date_created', 'date_modified',
                  'description', 'status', 'deadline', 'done']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'title', 'date_created',
                  'date_modified', 'status']


class CategoryTaskSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'date_created',
                  'date_modified', 'tasks', 'status']

from django.forms import model_to_dict
from rest_framework import viewsets, generics
from rest_framework.response import Response

from .services import TaskService
from .models import Category, Task
from .serializers import CategorySerializer, TaskSerializer, CategoryTaskSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    service_class = TaskService

    def perform_create(self, serializer):
        self.service_class.save_or_update(serializer)

    def perform_update(self, serializer):
        instance = self.get_object()
        self.service_class.check_task_status(instance)
        self.service_class.save_or_update(serializer)

    def perform_destroy(self, instance):
        self.service_class.check_category_status(
            instance.category_id
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.service_class.check_task_status(model_to_dict(instance))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.service_class.check_tasks_status(serializer.data)
        print(serializer.data)
        return Response(serializer.data)


class CategoryTaskAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryTaskSerializer
    service_class = TaskService

    def get(self, request, *args, **kwargs):
        data = self.list(request, *args, **kwargs).data
        for d in data:
            tasks = d.get('tasks')
            self.service_class.check_tasks_status(tasks)

        return self.list(request, *args, **kwargs)

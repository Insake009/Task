from datetime import timedelta, datetime
import dateutil.parser

from django.utils import timezone

from tasks.models import Task


class TaskService:

    @classmethod
    def save_or_update(cls, serializer):
        category = serializer.validated_data.get('category_id')
        cls.check_category_status(category)
        serializer.save()

    @classmethod
    def check_category_status(cls, category):
        tasks = category.tasks.values_list('done', flat=True)

        if not any(tasks):
            category.status = 'ACTIVE'
            category.save()

    @classmethod
    def check_task_status(cls, task_dict):
        task = Task.objects.filter(id=task_dict.get('id')).first()
        difference = timezone.now() - dateutil.parser.parse(task_dict.get('deadline'))

        if abs(difference) < timedelta(hours=12):
            if task.status == 'RED':
                pass
            else:
                task.status = 'RED'
                task.save()
        elif abs(difference) < timedelta(days=3):
            if task.status == 'YELLOW':
                pass
            else:
                task.status = 'YELLOW'
                task.save()
        else:
            if task.status == 'GREEN':
                pass
            else:
                task.status = 'GREEN'
                task.save()

    @classmethod
    def check_tasks_status(cls, tasks):
        for task in tasks:
            cls.check_task_status(task)

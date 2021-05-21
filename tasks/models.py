from datetime import timedelta

from django.db import models
from django.utils import timezone

from .constants import CATEGORY_STATUS, TASK_STATUS


class BaseModel(models.Model):
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.title


class Category(BaseModel):
    status = models.CharField(max_length=10, choices=CATEGORY_STATUS, default='NOT ACTIVE')


class Task(BaseModel):
    category_id = models.ForeignKey(Category, related_name='tasks', on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=6, choices=TASK_STATUS, default='GREEN')
    deadline = models.DateTimeField()
    done = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        difference = timezone.now() - self.deadline

        if abs(difference) < timedelta(hours=12):
            self.status = 'RED'
        elif abs(difference) < timedelta(days=3):
            self.status = 'YELLOW'
        else:
            self.status = 'GREEN'

        super().save(*args, **kwargs)


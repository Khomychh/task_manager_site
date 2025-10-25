from django.contrib.auth.models import AbstractUser
from django.db import models


class Worker(AbstractUser):
    position = models.ForeignKey("Position", on_delete=models.CASCADE)

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.position})"


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "URGENT", "Urgent"
        HIGH = "HIGH", "High"
        MEDIUM = "MEDIUM", "Medium"
        LOW = "LOW", "Low"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    task_type = models.ForeignKey("TaskType", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
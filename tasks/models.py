from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Worker(AbstractUser):
    position = models.ForeignKey(
        "Position",
        on_delete=models.CASCADE,
        related_name="workers",
        null=True,
        blank=True,
    )
    full_name = models.CharField(
        max_length=150,
        editable=False,
        null=True,
        blank=True,
    )
    biography = models.TextField(
        blank=True,
        default="",
    )

    class Meta:
        ordering = ["username"]

    def __str__(self):
        if self.first_name and self.last_name:
            return self.full_name
        return self.username

    def create_full_name(self):
        parts = [self.last_name, self.first_name]
        cleaned = [p.strip() for p in parts]
        return " ".join(cleaned)

    def save(self, *args, **kwargs):
        self.full_name = self.create_full_name()
        self.full_clean()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("tasks:worker-detail", kwargs={"pk": self.pk})


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
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM
    )
    type = models.ForeignKey(
        "TaskType",
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True,
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tasks",
        blank=True,
    )

    class Meta:
        ordering = ["deadline"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "project"],
                name="unique_task_name_per_project",
            ),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tasks:task-detail", kwargs={"pk": self.pk})


class TaskType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    # можна добавити зображення для типу завдання

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tasks:task-type-detail", kwargs={"pk": self.pk})


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(
        blank=True, default="This position has no description."
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tasks:position-detail", kwargs={"pk": self.pk})


class Team(models.Model):
    """
    Команда не працює над окремими завданнями,
    але працює над проєктамм
    """
    name = models.CharField(max_length=100)
    leader = models.ForeignKey(
        "Worker",
        on_delete=models.SET_NULL,
        related_name="team_leaders",
        null=True,
        blank=True,
    )
    workers = models.ManyToManyField(
        "Worker",
        related_name="teams",
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tasks:team-detail", kwargs={"pk": self.pk})


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(
        blank=True, default=""
    )
    leader = models.ForeignKey(
        "Worker",
        on_delete=models.SET_NULL,
        related_name="projects",
        null=True,
        blank=True,
    )
    team = models.ForeignKey(
        "Team",
        on_delete=models.SET_NULL,
        related_name="projects",
        null=True,
        blank=True,
    )

    # дедлайни завдань, які належать до даного проекту не можуть пізніше дедлайну проекту
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tasks:project-detail", kwargs={"pk": self.pk})
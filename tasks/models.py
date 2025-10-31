from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Worker(AbstractUser):
    position = models.ForeignKey(
        "Position",
        on_delete=models.CASCADE,
        related_name="workers",
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        _("first name"),
        max_length=150,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
    )
    full_name = models.CharField(
        max_length=150,
        editable=False,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return self.full_name

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


class Team(models.Model):
    """
    Команда не працює над окремими завданнями,
    але працює над проєктамм
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    workers = models.ManyToManyField(
        "Worker",
        related_name="teams",
    )
    projects = models.ManyToManyField(
        "Project",
        related_name="teams",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(
        blank=True, default=""
    )

    # дедлайни завдань, які належать до даного проекту не можуть пізніше дедлайну проекту
    # Від цього постає питання, що робити, якщо хочеть додати завдання до проекту, дедлайн якого пізніше
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    # Наступне поле дає можливість ставити лідера проєкту,
    # а також призначати проєкт одній людині, а не команді.
    # Також дає можливість, щоб над проєктом працювало декілька команд

    # Лідер проєкту є лідером команди, хоча це можна реалізувати
    leader = models.ForeignKey(
        "Worker",
        on_delete=models.SET_NULL,
        related_name="projects",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
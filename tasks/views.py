from django.shortcuts import render

from tasks.models import Task


def index(request):
    tasks_count = Task.objects.count()
    context = {"tasks_count": tasks_count}
    return render(request, "index.html", context=context)

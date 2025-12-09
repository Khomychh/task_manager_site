# Task Manager Site

Link to the site: https://task-manager-0ro2.onrender.com/

Test user:

    login: user
    password: user12345

## Overview
Task Manager Site is a Django web application for managing work across teams and projects. It provides full CRUD for:
- Tasks and Task Types
- Positions, Teams, and Workers (custom user model)
- Projects

## Installing / Getting started

Python must be installed on your system.

```shell
git clone https://github.com/Khomychh/task_manager_site.git
cd task_manager_site
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

## Features:
- Authentication via Django's auth system (login/logout)
- Search across lists (tasks, task types, workers, positions, teams, projects)
- Filters for list tasks by deadline, completion status, my tasks
- Task assignment helpers (take/assign/remove from me) and completion toggles for tasks/projects
- Crispy Forms with Bootstrap 5 styling
- Tests for all models, views, forms
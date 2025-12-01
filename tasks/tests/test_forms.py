from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from tasks.forms import TaskSearchForm, WorkerCreationForm, TaskCreateForm, TaskUpdateForm, TaskTypeSearchForm, \
    WorkerUpdateForm, PositionCreateForm, WorkerSearchForm, TeamCreateForm, ProjectCreateForm, ProjectUpdateForm, \
    TeamSearchForm, TaskTypeCreateForm, TaskTypeUpdateForm, ProjectSearchForm, PositionSearchForm
from tasks.models import Task, TaskType, Position, Project, Team
from tasks.views import PositionUpdateView


class PrivateTaskFormsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="ivank",
            password="PASSWORD123",
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="Test Type")
        self.deadline = timezone.now() + timezone.timedelta(days=1)
        self.task = Task.objects.create(
            name="Task",
            deadline=self.deadline,
            type=self.task_type
        )

    def test_task_search_form_no_data(self):
        form = TaskSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())

    def test_task_search_form_valid_data(self):
        name = "another"
        name2 = "just121214412"
        Task.objects.create(
            name=name,
            deadline=self.deadline,
            type=self.task_type
        )
        Task.objects.create(
            name=name,
            deadline=self.deadline,
            type=self.task_type
        )
        form = TaskSearchForm(data={"name": name})
        self.assertTrue(form.is_valid())
        url = f"{reverse('tasks:task-list')}?name={name}"
        response = self.client.get(url)
        self.assertContains(response, name)
        self.assertNotContains(response, name2)

    def test_task_create_form_valid_data(self):
        deadline2 = timezone.now().date() + timezone.timedelta(days=10)
        project = Project.objects.create(
            name="Project for test",
            deadline=deadline2
        )
        form_data = {
            "name": "Test Task",
            "deadline": self.deadline,
            "type": self.task_type.id,
            "priority": Task.Priority.HIGH,
            "project": project.id,
            "description": "Test Description"
        }
        form = TaskCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Test Task")
        self.assertEqual(form.cleaned_data["deadline"], self.deadline)
        self.assertEqual(form.cleaned_data["type"], self.task_type)
        self.assertEqual(form.cleaned_data["priority"], Task.Priority.HIGH)
        self.assertEqual(form.cleaned_data["project"], project)
        self.assertEqual(form.cleaned_data["description"], "Test Description")
        
    def test_task_create_form_invalid_data_deadline(self):
        form_data = {
            "name": "Test Task",
            # Wrong deadline
            "deadline": timezone.now().date(),
            "type": self.task_type.id,
            "priority": Task.Priority.HIGH,
            "description": "Test Description"
        }
        form = TaskCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_task_update_form_valid_data(self):
        p_deadline = timezone.now() + timezone.timedelta(days=10)
        project = Project.objects.create(
            name="Project for test",
            deadline=p_deadline
        )
        form_data = {
            "is_completed": True,
            "name": "New Name",
            "priority": Task.Priority.MEDIUM,
            "type": self.task_type.id,
            "deadline": self.deadline.isoformat(),
            "project": project.id,
            "description": "New Description",
            "assignees": [self.user.id]
        }
        form = TaskUpdateForm(data=form_data, instance=self.task)
        self.assertTrue(form.is_valid())


class PrivateTaskTypeFormsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="ivank",
            password="PASSWORD123",
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="Test Type")

    def test_task_type_create_form_no_data(self):
        form = TaskCreateForm(data={"name": ""})
        self.assertFalse(form.is_valid())

    def test_task_type_update_form_no_data(self):
        form = TaskUpdateForm(data={}, instance=self.task_type)
        self.assertFalse(form.is_valid())

    def test_task_type_create_form_invalid_data(self):
        TaskType.objects.create(name="Test")
        form_data = {
            "name": "Test",
            "description": "Test Description"
        }
        form = TaskCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_task_type_update_form_invalid_data(self):
        TaskType.objects.create(name="Test")
        form_data = {
            "name": "Test",
            "description": "Test Description"
        }
        form = TaskUpdateForm(data=form_data, instance=self.task_type)

    def test_task_type_create_form_valid_data(self):
        form_data = {
            "name": "Test Type 2",
            "description": "Test Description"
        }
        form = TaskTypeCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_type_update_form_valid_data(self):
        form_data = {
            "name": "New Type",
            "description": "Test Description"
        }
        form = TaskTypeUpdateForm(data=form_data, instance=self.task_type)
        self.assertTrue(form.is_valid())

    def test_task_type_search_form_valid_data(self):
        name = "another"
        name2 = "just121214412"
        TaskType.objects.create(name=name)
        TaskType.objects.create(name=name2)
        form = TaskTypeSearchForm(data={"name": name})
        self.assertTrue(form.is_valid())
        url = f"{reverse('tasks:task-type-list')}?name={name}"
        response = self.client.get(url)
        self.assertContains(response, name)
        self.assertNotContains(response, name2)

    def test_task_type_search_form_no_data(self):
        form = TaskSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())
        

class PrivateWorkerFormsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="ivank",
            password="PASSWORD123",
        )
        self.client.force_login(self.user)

    def test_worker_create_form_valid_data(self):
        position = Position.objects.create(name="Test Position")
        form_data = {
            "username": "test_worker",
            "last_name": "Testowicz",
            "first_name": "Test",
            "email": "test@test.com",
            "position": position.id,
            "biography": "Testowy biografia",
            "password1": "Password123!",
            "password2": "Password123!"
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test_worker")
        self.assertEqual(form.cleaned_data["position"], position)
        self.assertEqual(form.cleaned_data["last_name"], "Testowicz")
        self.assertEqual(form.cleaned_data["first_name"], "Test")
        self.assertEqual(form.cleaned_data["email"], "test@test.com")
        self.assertEqual(form.cleaned_data["position"], position)
        self.assertEqual(form.cleaned_data["biography"], "Testowy biografia")

    def test_worker_update_form_valid_date(self):
        old_user = get_user_model().objects.create_user(
            username="test_worker",
            password="Password123!"
        )
        position = Position.objects.create(name="Test Position")
        form_data = {
            "username": "test_worker",
            "last_name": "Testowicz",
            "first_name": "Test",
            "email": "test@test.com",
            "position": position.id,
            "biography": "Testowy biografia",
        }
        form = WorkerUpdateForm(data=form_data, instance=old_user)
        self.assertTrue(form.is_valid())

    def test_worker_search_form_valid_data(self):
        worker1 = get_user_model().objects.create_user(
            username="test_worker1",
            password="Password123!",
            last_name="Last1",
            first_name="First1"
        )
        worker2 = get_user_model().objects.create_user(
            username="test_worker22342",
            password="Password123!",
            last_name="Last2",
            first_name="First2"
        )
        form = WorkerSearchForm(data={"full_name": worker1.full_name})
        self.assertTrue(form.is_valid())
        url = f"{reverse('tasks:worker-list')}?full_name={worker1.full_name}"
        response = self.client.get(url)
        self.assertContains(response, worker1.full_name)
        self.assertNotContains(response, worker2.full_name)

    def test_worker_search_form_no_data(self):
        form = WorkerSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())


class PrivatePositionFormsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="ivank",
            password="PASSWORD123",
        )
        self.client.force_login(self.user)

    def test_position_create_form_valid_data(self):
        form_data = {
            "name": "Test Position",
            "description": "Test Description"
        }
        form = PositionCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_position_search_form_valid_data(self):
        name = "another"
        name2 = "just121214412"
        Position.objects.create(name=name)
        Position.objects.create(name=name2)
        form = PositionSearchForm(data={"name": name})
        self.assertTrue(form.is_valid())
        url = f"{reverse('tasks:position-list')}?name={name}"
        response = self.client.get(url)
        self.assertContains(response, name)
        self.assertNotContains(response, name2)

    def test_position_search_form_no_data(self):
        form = PositionSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())


class PrivateTeamFormsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="ivank",
            password="PASSWORD123",
        )
        self.client.force_login(self.user)

    def test_team_create_form_valid_data(self):
        worker1 = get_user_model().objects.create_user(
            username="test_worker1",
            password="Password123!"
        )
        worker2 = get_user_model().objects.create_user(
            username="test_worker2",
            password="Password123!"
        )
        form_data = {
            "name": "Test Team",
            "leader": self.user.id,
            "workers": [worker1.id, worker2.id]
        }
        form = TeamCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_team_update_form_valid_data(self):
        team = Team.objects.create(name="Test Team")
        form_data = {
            "name": "New Team Name",
            "workers": [self.user.id]
        }
        form = TeamCreateForm(data=form_data, instance=team)
        self.assertTrue(form.is_valid())

    def test_team_search_form_valid_data(self):
        name = "another"
        name2 = "just121214412"
        Team.objects.create(name=name)
        Team.objects.create(name=name2)
        form = TeamSearchForm(data={"name": name})
        self.assertTrue(form.is_valid())
        url = f"{reverse('tasks:team-list')}?name={name}"
        response = self.client.get(url)
        self.assertContains(response, name)
        self.assertNotContains(response, name2)

    def test_team_search_form_no_data(self):
        form = TeamSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())


class PrivateProjectFormsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="ivank",
            password="PASSWORD123",
        )
        self.client.force_login(self.user)
        self.deadline = timezone.now() + timezone.timedelta(days=10)

    def test_project_create_form_valid_data(self):
        form_data = {
            "name": "Test Project",
            "description": "Test Description",
            "deadline": self.deadline.date().isoformat()
        }
        form = ProjectCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_project_update_form_valid_data(self):
        p_deadline = timezone.now() + timezone.timedelta(days=10)
        project = Project.objects.create(
            name="Test Project",
            deadline=p_deadline
        )
        form_data = {
            "name": "New Project Name",
            "deadline": self.deadline.date().isoformat()
        }
        form = ProjectUpdateForm(data=form_data, instance=project)
        self.assertTrue(form.is_valid())

    def test_project_search_form_valid_data(self):
        name = "another"
        name2 = "just121214412"
        p_deadline = timezone.now() + timezone.timedelta(days=10)
        Project.objects.create(
            name=name,
            deadline=p_deadline
        )
        Project.objects.create(
            name=name2,
            deadline=p_deadline
        )
        form = ProjectSearchForm(data={"name": name})
        self.assertTrue(form.is_valid())
        url = f"{reverse('tasks:project-list')}?name={name}"
        response = self.client.get(url)
        self.assertContains(response, name)
        self.assertNotContains(response, name2)

    def test_project_search_form_no_data(self):
        form = ProjectSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())

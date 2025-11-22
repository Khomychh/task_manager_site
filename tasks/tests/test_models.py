from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from tasks.models import Position, Task, TaskType, Team, Project


class WorkerTest(TestCase):
    def test_worker_create_field_full_name(self):
        worker = get_user_model().objects.create_user(
            username="test_worker",
            last_name="User",
            first_name="Test",
            password="Password123!",
        )
        self.assertEqual(worker.username, "test_worker")
        self.assertEqual(worker.full_name, "User Test")

    def test_worker_str_without_first_and_last_name(self):
        worker = get_user_model().objects.create_user(
            username="test_worker",
            password="Password123!",
        )
        self.assertEqual(str(worker), worker.username)

    def test_worker_create_with_position(self):
        position = Position.objects.create(name="Test Position")
        worker = get_user_model().objects.create_user(
            username="test_worker",
            password="Password123!",
            position=position,
        )
        self.assertEqual(worker.position, position)

    def test_worker_create_with_biography(self):
        worker = get_user_model().objects.create_user(
            username="test_worker",
            password="Password123!",
            biography="Test biography",
        )
        self.assertEqual(worker.biography, "Test biography")

    def test_worker_str(self):
        worker = get_user_model().objects.create_user(
            username="test_worker",
            last_name="User",
            first_name="Test",
            password="Password123!",
        )
        self.assertEqual(str(worker), worker.full_name)


class TaskTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Test Type")
        self.project = Project.objects.create(
            name="Test Project",
            deadline=timezone.now().date() + timezone.timedelta(days=10)
        )
        self.worker1 = get_user_model().objects.create_user(
            username="test_worker1",
            password="testpass123"
        )
        self.worker2 = get_user_model().objects.create_user(
            username="test_worker2",
            password="testpass123"
        )

    def test_task_create_with_name(self):
        deadline = timezone.now() + timezone.timedelta(days=1)
        task = Task.objects.create(
            name="Test Task",
            deadline=deadline,
            type=self.task_type,
        )
        self.assertEqual(task.name, "Test Task")

    def test_task_name_unique_in_project(self):
        deadline = timezone.now() + timezone.timedelta(days=1)
        task_name = "Test Name"
        Task.objects.create(
            name=task_name,
            deadline=deadline,
            type=self.task_type,
            project=self.project,
        )
        with self.assertRaises(ValidationError):
            Task.objects.create(
                name=task_name,
                deadline=deadline,
                project=self.project,
                type=self.task_type,
            )

    def test_task_create_with_deadline(self):
        deadline = timezone.now() + timezone.timedelta(days=1)
        task = Task.objects.create(
            name="Test Task",
            deadline=deadline,
            type=self.task_type,
        )
        self.assertEqual(task.deadline, deadline)

    def test_task_deadline_validation(self):
        with self.assertRaises(ValidationError):
            Task.objects.create(
                name="Test Task",
                deadline=timezone.now() - timezone.timedelta(days=1),
                type=self.task_type,
            )

    def test_task_project_deadline_validation(self):
        with self.assertRaises(ValidationError):
            Task.objects.create(
                name="Test Task",
                deadline=timezone.now() + timezone.timedelta(days=20),
                type=self.task_type,
                project=self.project,
            )
        
    def test_task_create_with_type(self):
        deadline = timezone.now() + timezone.timedelta(days=1)
        task = Task.objects.create(
            name="Test Task",
            deadline=deadline,
            type=self.task_type,
        )
        self.assertEqual(task.type, self.task_type)

    def test_task_create_with_description(self):
        deadline = timezone.now() + timezone.timedelta(days=1)
        task = Task.objects.create(
            name="Test Task",
            deadline=deadline,
            description="Test Description",
            type=self.task_type,
        )
        self.assertEqual(task.description, "Test Description")
        
    def test_task_create_with_is_completed(self):
        deadline = timezone.now() + timezone.timedelta(days=1)
        task = Task.objects.create(
            name="Test Task",
            deadline=deadline,
            type=self.task_type,
        )
        self.assertFalse(task.is_completed)
    
    def test_task_create_with_priority(self):
        deadline = timezone.now() + timezone.timedelta(days=1)
        task = Task.objects.create(
            name="Test Task",
            deadline=deadline,
            priority=Task.Priority.MEDIUM,
            type=self.task_type,
        )
        self.assertEqual(task.priority, "MEDIUM")
        
    def test_task_create_with_project(self):
        deadline = timezone.now() + timezone.timedelta(days=1)
        task = Task.objects.create(
            name="Test Task",
            deadline=deadline,
            project=self.project,
            type=self.task_type,
        )
        self.assertEqual(task.project, self.project)
        
    def test_task_create_with_assignees(self):
        deadline = timezone.now() + timezone.timedelta(days=1)
        task = Task.objects.create(
            name="Test Task",
            deadline=deadline,
            type=self.task_type,
        )
        task.assignees.add(self.worker1, self.worker2)
        self.assertIn(self.worker1, task.assignees.all())
        self.assertIn(self.worker2, task.assignees.all())

    def test_task_str(self):
        task = Task.objects.create(
            name="Test Task",
            deadline=timezone.now() + timezone.timedelta(days=1),
            type=self.task_type,
        )
        self.assertEqual(str(task), task.name)


class TaskTypeTest(TestCase):
    def test_task_type_create_with_name_and_description(self):
        task_type = TaskType.objects.create(
            name="Test Type",
            description="Test Description"
        )
        self.assertEqual(task_type.name, "Test Type")
        self.assertEqual(task_type.description, "Test Description")

    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="Test Type")
        self.assertEqual(str(task_type), task_type.name)


class PositionTest(TestCase):
    def test_position_create_with_name_and_description(self):
        position = Position.objects.create(
            name="Test Position",
            description="Test Description"
        )
        self.assertEqual(position.name, "Test Position")
        self.assertEqual(position.description, "Test Description")

    def test_position_str(self):
        position = Position.objects.create(name="Test Position")
        self.assertEqual(str(position), position.name)


class TeamTest(TestCase):
    def setUp(self):
        self.leader = get_user_model().objects.create_user(
            username="test_leader",
            password="testpass123"
        )
        self.worker1 = get_user_model().objects.create_user(
            username="test_worker1",
            password="testpass123"
        )
        self.worker2 = get_user_model().objects.create_user(
            username="test_worker2",
            password="testpass123"
        )

    def test_team_create_with_name_and_leader(self):
        team = Team.objects.create(
            name="Test Team",
            leader=self.leader
        )
        self.assertEqual(team.name, "Test Team")
        self.assertEqual(team.leader, self.leader)

    def test_team_create_with_workers(self):
        team = Team.objects.create(
            name="Test Team",
            leader=self.leader,
        )
        team.workers.add(self.worker1, self.worker2)
        self.assertIn(self.worker1, team.workers.all())
        self.assertIn(self.worker2, team.workers.all())

    def test_team_str(self):
        team = Team.objects.create(name="Test Team")
        self.assertEqual(str(team), team.name)


class ProjectTest(TestCase):
    def setUp(self):
        self.leader = get_user_model().objects.create_user(
            username="test_leader",
            password="testpass123"
        )
        self.team = Team.objects.create(
            name="Test Team",
            leader=self.leader
        )

    def test_project_create_with_name_description_deadline(self):
        deadline = timezone.now().date() + timezone.timedelta(days=10)
        project = Project.objects.create(
            name="Test Project",
            description="Test Description",
            deadline=deadline
        )
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(project.description, "Test Description")
        self.assertEqual(project.deadline, deadline)

    def test_project_deadline_validation(self):
        with self.assertRaises(ValidationError):
            Project.objects.create(
                name="Test Project",
                deadline=timezone.now().date() - timezone.timedelta(days=1)
            )

    def test_project_create_with_leader(self):
        deadline = timezone.now().date() + timezone.timedelta(days=10)
        project = Project.objects.create(
            name="Test Project",
            leader=self.leader,
            deadline=deadline
        )
        self.assertEqual(project.leader, self.leader)

    def test_project_create_with_team(self):
        deadline = timezone.now().date() + timezone.timedelta(days=10)
        project = Project.objects.create(
            name="Test Project",
            deadline=deadline,
            team=self.team
        )
        self.assertEqual(project.team, self.team)

    def test_project_str(self):
        project = Project.objects.create(
            name="Test Project",
            deadline=timezone.now().date() + timezone.timedelta(days=10)
        )
        self.assertEqual(str(project), project.name)

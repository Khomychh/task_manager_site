from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from tasks.models import Worker, Project, Task, TaskType, Position, Team

WORKER_URL = reverse("tasks:worker-list")
TASK_URL = reverse("tasks:task-list")
TASK_TYPE_URL = reverse("tasks:task-type-list")
POSITION_URL = reverse("tasks:position-list")
TEAM_URL = reverse("tasks:team-list")
PROJECT_URL = reverse("tasks:project-list")


class PublicHomePageTest(TestCase):
    def test_login_required(self):
        response = self.client.get("/")
        self.assertNotEqual(response.status_code, 200)


class PrivateHomePageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="Password123!"
        )
        self.client.force_login(self.user)

    def test_retrieve_home_page(self):
        deadline = timezone.now() + timezone.timedelta(days=1)
        task_type = TaskType.objects.create(name="Test Type")

        Project.objects.create(name="Test Project", deadline=deadline)
        Task.objects.create(
            name="Test Task",
            type=task_type,
            deadline=deadline
        )
        Worker.objects.create(username="test_worker", password="Password123!")

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["tasks_count"], 1)
        self.assertEqual(response.context["project_count"], 1)
        self.assertEqual(response.context["worker_count"], 2)

        self.assertTemplateUsed(response, "index.html")


class PublicWorkerTest(TestCase):
    def setUp(self):
        self.worker = Worker.objects.create(
            username="test_worker",
            password="Password123!"
        )

    def test_worker_list_login_required(self):
        response = self.client.get(WORKER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_worker_create_login_required(self):
        response = self.client.get(WORKER_URL + "create/")
        self.assertNotEqual(response.status_code, 200)

    def test_worker_detail_login_required(self):
        response = self.client.get(WORKER_URL + f"{self.worker.id}/")
        self.assertNotEqual(response.status_code, 200)

    def test_worker_update_login_required(self):
        response = self.client.get(WORKER_URL + f"{self.worker.id}/update/")
        self.assertNotEqual(response.status_code, 200)

    def test_worker_delete_login_required(self):
        response = self.client.get(WORKER_URL + f"{self.worker.id}/delete/")
        self.assertNotEqual(response.status_code, 200)


class PrivateWorkerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="Password123!"
        )
        self.client.force_login(self.user)

    def test_retrieve_workers(self):
        get_user_model().objects.create_user(
            username="test_worker2",
            password="Password123!"
        )
        response = self.client.get(WORKER_URL)
        self.assertEqual(response.status_code, 200)

        workers = Worker.objects.all()
        self.assertEqual(list(response.context["worker_list"]), list(workers))

        self.assertIn("search_form", response.context)

        self.assertTemplateUsed(response, "tasks/worker_list.html")

    def test_retrieve_worker_detail(self):
        response = self.client.get(WORKER_URL + f"{self.user.id}/")
        self.assertEqual(response.status_code, 200)

    def test_retrieve_create_worker(self):
        response = self.client.get(WORKER_URL + "create/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_retrieve_update_worker(self):
        response = self.client.get(WORKER_URL + f"{self.user.id}/update/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_retrieve_delete_worker(self):
        response = self.client.get(WORKER_URL + f"{self.user.id}/delete/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/worker_confirm_delete.html")


class PublicTaskTest(TestCase):
    def setUp(self):
        deadline = timezone.now() + timezone.timedelta(days=1)
        task_type = TaskType.objects.create(name="Test Type")
        self.task = Task.objects.create(
            name="Test Task",
            deadline=deadline,
            type=task_type
        )

    def test_tasks_login_required(self):
        response = self.client.get(TASK_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_task_detail_login_required(self):
        response = self.client.get(TASK_URL + f"{self.task.id}/")
        self.assertNotEqual(response.status_code, 200)

    def test_task_update_login_required(self):
        response = self.client.get(TASK_URL + f"{self.task.id}/update/")
        self.assertNotEqual(response.status_code, 200)

    def test_task_delete_login_required(self):
        response = self.client.get(TASK_URL + f"{self.task.id}/delete/")
        self.assertNotEqual(response.status_code, 200)

    def test_task_create_login_required(self):
        response = self.client.get(TASK_URL + "create/")
        self.assertNotEqual(response.status_code, 200)

    def test_task_complete_login_required(self):
        response = self.client.get(TASK_URL + f"{self.task.id}/complete/")
        self.assertNotEqual(response.status_code, 200)

    def test_task_assign_login_required(self):
        response = self.client.get(TASK_URL + f"{self.task.id}/assign/")
        self.assertNotEqual(response.status_code, 200)

    def test_task_remove_from_me_login_required(self):
        response = self.client.get(TASK_URL + f"{self.task.id}/remove_from_me/")
        self.assertNotEqual(response.status_code, 200)


class PrivateTaskTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="Password123!"
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="Test Type")
        self.deadline = timezone.now() + timezone.timedelta(days=1)
        self.task = Task.objects.create(
            name="Test Task",
            deadline=self.deadline,
            type=self.task_type
        )

    def test_retrieve_tasks(self):
        deadline2 = timezone.now() + timezone.timedelta(days=2)
        deadline3 = timezone.now() + timezone.timedelta(days=3)
        Task.objects.create(
            name="Test Task 3",
            type=self.task_type,
            deadline=deadline3
        )
        Task.objects.create(
            name="Test Task 2",
            type=self.task_type,
            deadline=deadline2
        )

        response = self.client.get(TASK_URL)
        self.assertEqual(response.status_code, 200)

        tasks = Task.objects.all()
        self.assertEqual(list(response.context["task_list"]), list(tasks))

        self.assertIn("search_form", response.context)

        self.assertTemplateUsed(response, "tasks/task_list.html")

    def test_retrieve_my_tasks(self):
        Task.objects.create(
            name="Test Task 2",
            type=self.task_type,
            deadline=self.deadline,
        )
        self.task.assignees.add(self.user)
        response = self.client.get(TASK_URL + "?my=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["task_list"]), 1)

    def test_filter_tasks_by_status(self):
        Task.objects.create(
            name="Test Task 2",
            type=self.task_type,
            deadline=self.deadline,
            is_completed=True
        )
        response = self.client.get(TASK_URL + "?status=completed")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["task_list"]), 1)

        response = self.client.get(TASK_URL + "?status=uncompleted")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["task_list"]), 1)

    def test_order_by_deadline(self):
        deadline2 = timezone.now() + timezone.timedelta(days=2)
        deadline3 = timezone.now() + timezone.timedelta(days=3)
        Task.objects.create(
            name="Test Task 3",
            type=self.task_type,
            deadline=deadline3
        )
        Task.objects.create(
            name="Test Task 2",
            type=self.task_type,
            deadline=deadline2
        )

        response = self.client.get(TASK_URL + "?ordering=-deadline")
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all().order_by("-deadline")
        self.assertEqual(list(response.context["task_list"]), list(tasks))

        response = self.client.get(TASK_URL + "?ordering=deadline")
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all().order_by("deadline")
        self.assertEqual(list(response.context["task_list"]), list(tasks))

    def test_retrieve_task_detail(self):
        response = self.client.get(TASK_URL + f"{self.task.id}/")
        self.assertEqual(response.status_code, 200)

    def test_retrieve_create_task(self):
        response = self.client.get(TASK_URL + "create/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        
    def test_task_create_success_url(self):
        response = self.client.post(
            TASK_URL + "create/",
            {
                "name": "Test Task 2",
                "type": self.task_type.id,
                "deadline": self.deadline.isoformat(),
                "priority": "LOW"
            }
        )
        self.assertRedirects(response, TASK_URL)

    def test_retrieve_update_task(self):
        response = self.client.get(TASK_URL + f"{self.task.id}/update/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        
    def test_retrieve_delete_task(self):
        response = self.client.get(TASK_URL + f"{self.task.id}/delete/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_confirm_delete.html")

    def test_task_delete_success_url(self):
        response = self.client.post(TASK_URL + f"{self.task.id}/delete/")
        self.assertRedirects(response, TASK_URL)

    def test_complete_task(self):
        url = TASK_URL + f"{self.task.id}/completed/" + f"?next={TASK_URL}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)

    def test_uncomplete_task(self):
        self.task.is_completed = True
        self.task.save()
        url = TASK_URL + f"{self.task.id}/completed/" + f"?next={TASK_URL}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)

    def test_retrieve_assign_task(self):
        response = self.client.get(TASK_URL + f"{self.task.id}/assign/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_task_take(self):
        response = self.client.get(TASK_URL + f"{self.task.id}/take/")
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertIn(self.user, self.task.assignees.all())

    def test_task_remove_from_me(self):
        self.task.assignees.add(self.user)
        response = self.client.get(TASK_URL + f"{self.task.id}/remove-from-me/")
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertNotIn(self.user, self.task.assignees.all())


class PublicTaskTypeTest(TestCase):
    def test_task_types_login_required(self):
        response = self.client.get(TASK_TYPE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_detail_task_type_login_required(self):
        task_type = TaskType.objects.create(name="Test Type")
        response = self.client.get(TASK_TYPE_URL + f"{task_type.id}/")
        self.assertNotEqual(response.status_code, 200)

    def test_create_task_type_login_required(self):
        response = self.client.get(TASK_TYPE_URL + "create/")
        self.assertNotEqual(response.status_code, 200)

    def test_update_task_type_login_required(self):
        task_type = TaskType.objects.create(name="Test Type")
        response = self.client.get(TASK_TYPE_URL + f"{task_type.id}/update/")
        self.assertNotEqual(response.status_code, 200)

    def test_delete_task_type_login_required(self):
        task_type = TaskType.objects.create(name="Test Type")
        response = self.client.get(TASK_TYPE_URL + f"{task_type.id}/delete/")
        self.assertNotEqual(response.status_code, 200)


class PrivateTaskTypeTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="Password123!"
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="Type")

    def test_retrieve_task_types(self):
        TaskType.objects.create(name="Test Type 2")
        response = self.client.get(TASK_TYPE_URL)
        self.assertEqual(response.status_code, 200)

        task_types = TaskType.objects.all()
        self.assertEqual(list(response.context["task_type_list"]), list(task_types))

        self.assertIn("search_form", response.context)

        self.assertTemplateUsed(response, "tasks/task_type_list.html")

    def test_retrieve_task_type_detail(self):
        response = self.client.get(TASK_TYPE_URL + f"{self.task_type.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("task_type" in response.context)
        self.assertContains(response, self.task_type.name)
        self.assertTemplateUsed(response, "tasks/task_type_detail.html")

    def test_retrieve_create_task_type(self):
        response = self.client.get(TASK_TYPE_URL + "create/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertTemplateUsed(response, "tasks/task_type_form.html")

    def test_retrieve_update_task_type(self):
        url = TASK_TYPE_URL + f"{self.task_type.id}/update/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertTemplateUsed(response, "tasks/task_type_form.html")

    def test_retrieve_delete_task_type(self):
        url = TASK_TYPE_URL + f"{self.task_type.id}/delete/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("task_type" in response.context)
        self.assertTemplateUsed(
            response,
            "tasks/task_type_confirm_delete.html"
        )


class PublicPositionTest(TestCase):
    def test_positions_login_required(self):
        response = self.client.get(POSITION_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_detail_position_login_required(self):
        position = Position.objects.create(name="Test Position")
        response = self.client.get(POSITION_URL + f"{position.id}/")
        self.assertNotEqual(response.status_code, 200)

    def test_create_position_login_required(self):
        response = self.client.get(POSITION_URL + "create/")
        self.assertNotEqual(response.status_code, 200)

    def test_update_position_login_required(self):
        position = Position.objects.create(name="Test Position")
        response = self.client.get(POSITION_URL + f"{position.id}/update/")
        self.assertNotEqual(response.status_code, 200)

    def test_delete_position_login_required(self):
        position = Position.objects.create(name="Test Position")
        response = self.client.get(POSITION_URL + f"{position.id}/delete/")
        self.assertNotEqual(response.status_code, 200)


class PrivatePositionTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="Password123!"
        )
        self.client.force_login(self.user)
        self.position = Position.objects.create(name="Test Position")

    def test_retrieve_positions(self):
        Position.objects.create(name="Test Position 2")

        response = self.client.get(POSITION_URL)
        self.assertEqual(response.status_code, 200)

        positions = Position.objects.all()
        self.assertEqual(list(response.context["position_list"]), list(positions))
        self.assertIn("search_form", response.context)
        self.assertTemplateUsed(response, "tasks/position_list.html")

    def test_retrieve_position_detail(self):
        response = self.client.get(POSITION_URL + f"{self.position.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/position_detail.html")

    def test_create_position(self):
        response = self.client.get(POSITION_URL + "create/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_create_position_success_url(self):
        response = self.client.post(
            POSITION_URL + "create/",
            {
                "name": "Test Position 2"
            }
        )
        self.assertRedirects(response, POSITION_URL)

    def test_update_position(self):
        response = self.client.get(POSITION_URL + f"{self.position.id}/update/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_update_position_success_url(self):
        response = self.client.post(
            POSITION_URL + f"{self.position.id}/update/",
            {
                "name": "Test Position 2"
            }
        )
        self.assertRedirects(response, POSITION_URL + f"{self.position.id}/")

    def test_delete_position(self):
        response = self.client.get(POSITION_URL + f"{self.position.id}/delete/")
        self.assertEqual(response.status_code, 200)

    def test_delete_position_success_url(self):
        response = self.client.post(
            POSITION_URL + f"{self.position.id}/delete/",
        )
        self.assertRedirects(response, POSITION_URL)


class PublicTeamTest(TestCase):
    def test_teams_login_required(self):
        response = self.client.get(TEAM_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_team_detail_login_required(self):
        team = Team.objects.create(name="Test Team")
        response = self.client.get(TEAM_URL + f"{team.id}/")
        self.assertNotEqual(response.status_code, 200)

    def test_team_create_login_required(self):
        response = self.client.get(TEAM_URL + "create/")
        self.assertNotEqual(response.status_code, 200)

    def test_team_update_login_required(self):
        team = Team.objects.create(name="Test Team")
        response = self.client.get(TEAM_URL + f"{team.id}/update/")
        self.assertNotEqual(response.status_code, 200)

    def test_team_delete_login_required(self):
        team = Team.objects.create(name="Test Team")
        response = self.client.get(TEAM_URL + f"{team.id}/delete/")
        self.assertNotEqual(response.status_code, 200)


class PrivateTeamTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="Password123!"
        )
        self.client.force_login(self.user)
        self.team = Team.objects.create(name="Test Team")

    def test_retrieve_teams(self):
        Team.objects.create(name="Test Team 2")

        response = self.client.get(TEAM_URL)
        self.assertEqual(response.status_code, 200)

        teams = Team.objects.all()
        self.assertEqual(list(response.context["team_list"]), list(teams))
        self.assertIn("search_form", response.context)
        self.assertTemplateUsed(response, "tasks/team_list.html")

    def test_retrieve_team_detail(self):
        response = self.client.get(TEAM_URL + f"{self.team.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/team_detail.html")

    def test_create_team(self):
        response = self.client.get(TEAM_URL + "create/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_create_team_success_url(self):
        response = self.client.post(
            TEAM_URL + "create/",
            {
                "name": "Test Team 2"
            }
        )
        self.assertRedirects(response, TEAM_URL)

    def test_update_team(self):
        response = self.client.get(TEAM_URL + f"{self.team.id}/update/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_update_team_success_url(self):
        response = self.client.post(
            TEAM_URL + f"{self.team.id}/update/",
            {
                "name": "Test Team 2"
            }
        )
        self.assertRedirects(response, TEAM_URL + f"{self.team.id}/")

    def test_delete_team(self):
        response = self.client.get(TEAM_URL + f"{self.team.id}/delete/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/team_confirm_delete.html")

    def test_delete_team_success_url(self):
        response = self.client.post(
            TEAM_URL + f"{self.team.id}/delete/",
        )
        self.assertRedirects(response, TEAM_URL)


class PublicProjectTest(TestCase):
    def test_projects_login_required(self):
        response = self.client.get(PROJECT_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_project_detail_login_required(self):
        deadline = timezone.now() + timezone.timedelta(days=10)
        project = Project.objects.create(
            name="Test Project",
            deadline=deadline
        )
        response = self.client.get(PROJECT_URL + f"{project.id}/")
        self.assertNotEqual(response.status_code, 200)

    def test_project_create_login_required(self):
        response = self.client.get(PROJECT_URL + "create/")
        self.assertNotEqual(response.status_code, 200)

    def test_project_update_login_required(self):
        deadline = timezone.now() + timezone.timedelta(days=10)
        project = Project.objects.create(
            name="Test Project",
            deadline=deadline
        )
        response = self.client.get(PROJECT_URL + f"{project.id}/update/")
        self.assertNotEqual(response.status_code, 200)

    def test_project_delete_login_required(self):
        deadline = timezone.now() + timezone.timedelta(days=10)
        project = Project.objects.create(
            name="Test Project",
            deadline=deadline
        )
        response = self.client.get(PROJECT_URL + f"{project.id}/delete/")
        self.assertNotEqual(response.status_code, 200)

    def test_project_toggle_complete_login_required(self):
        deadline = timezone.now() + timezone.timedelta(days=10)
        project = Project.objects.create(
            name="Test Project",
            deadline=deadline
        )
        response = self.client.get(PROJECT_URL + f"{project.id}/toggle-complete/")
        self.assertNotEqual(response.status_code, 200)


class PrivateProjectTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="Password123!"
        )
        self.client.force_login(self.user)
        self.deadline = timezone.now() + timezone.timedelta(days=10)
        self.project = Project.objects.create(
            name="Test Project",
            deadline=self.deadline
        )

    def test_retrieve_projects(self):
        Project.objects.create(
            name="Test Project 2",
            deadline=self.deadline
        )

        response = self.client.get(PROJECT_URL)
        self.assertEqual(response.status_code, 200)

        projects = Project.objects.all()
        self.assertEqual(list(response.context["project_list"]), list(projects))
        self.assertIn("search_form", response.context)
        self.assertTemplateUsed(response, "tasks/project_list.html")

    def test_retrieve_project_detail(self):
        response = self.client.get(PROJECT_URL + f"{self.project.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/project_detail.html")

    def test_retrieve_create_project(self):
        response = self.client.get(PROJECT_URL + "create/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertTemplateUsed(response, "tasks/project_form.html")

    def test_create_project_success_url(self):
        response = self.client.post(
            PROJECT_URL + "create/",
            {
                "name": "Test Project 2",
                "deadline": self.deadline.date().isoformat()
            }
        )
        project = Project.objects.get(name="Test Project 2")
        self.assertRedirects(response, PROJECT_URL + f"{project.id}/")

    def test_retrieve_update_project(self):
        response = self.client.get(PROJECT_URL + f"{self.project.id}/update/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertTemplateUsed(response, "tasks/project_form.html")

    def test_update_project_success_url(self):
        response = self.client.post(
            PROJECT_URL + f"{self.project.id}/update/",
            {
                "name": "Test Project 2",
                "deadline": self.deadline.date().isoformat(),
            }
        )
        self.assertRedirects(response, PROJECT_URL + f"{self.project.id}/")

    def test_retrieve_delete_project(self):
        response = self.client.get(PROJECT_URL + f"{self.project.id}/delete/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/project_confirm_delete.html")

    def test_delete_project_success_url(self):
        response = self.client.post(
            PROJECT_URL + f"{self.project.id}/delete/",
        )
        self.assertRedirects(response, PROJECT_URL)

    def test_project_toggle_complete(self):
        next_url = f"?next={PROJECT_URL}"
        response = self.client.post(PROJECT_URL + f"{self.project.id}/completed/{next_url}")
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertTrue(self.project.is_completed)

    def test_project_toggle_uncomlete(self):
        next_url = f"?next={PROJECT_URL}"
        self.project.is_completed = True
        self.project.save()
        response = self.client.post(PROJECT_URL + f"{self.project.id}/completed/{next_url}")
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertFalse(self.project.is_completed)
        

import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from main.models import Project, Task, Team
from users.models import User


class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Начинаю заполнение базы данных...'))
        
        self.stdout.write('\nСоздание пользователей...')
        users = []
        user_data = [
            {'username': 'иван_петров', 'first_name': 'Иван', 'last_name': 'Петров', 'about': 'Ведущий разработчик, 10 лет опыта'},
            {'username': 'мария_соколова', 'first_name': 'Мария', 'last_name': 'Соколова', 'about': 'UI/UX дизайнер, люблю создавать красивые интерфейсы'},
            {'username': 'петр_сидоров', 'first_name': 'Петр', 'last_name': 'Сидоров', 'about': 'Backend разработчик, специалист по Django'},
            {'username': 'анна_козлова', 'first_name': 'Анна', 'last_name': 'Козлова', 'about': 'Project manager, организую процессы'},
            {'username': 'дмитрий_волков', 'first_name': 'Дмитрий', 'last_name': 'Волков', 'about': 'Frontend разработчик, React и Vue'},
            {'username': 'елена_морозова', 'first_name': 'Елена', 'last_name': 'Морозова', 'about': 'Тестировщик, ищу баги'},
            {'username': 'алексей_павлов', 'first_name': 'Алексей', 'last_name': 'Павлов', 'about': 'DevOps инженер'},
            {'username': 'ольга_смирнова', 'first_name': 'Ольга', 'last_name': 'Смирнова', 'about': 'Аналитик данных'},
        ]
        
        for data in user_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': f"{data['username']}@example.com".lower(),
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'about_me': data['about']
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'  ✓ Создан пользователь: {user.get_full_name()} (@{user.username})')
            else:
                self.stdout.write(f'  • Пользователь уже существует: {user.get_full_name()}')
            users.append(user)
        
        self.stdout.write('\nСоздание проектов...')
        projects = []
        project_data = [
            {
                'title': 'Интернет-магазин "Электроника"',
                'description': 'Разработка современного интернет-магазина с корзиной, личным кабинетом и интеграцией с платежными системами',
                'is_private': False
            },
            {
                'title': 'CRM система для бизнеса',
                'description': 'Внутренняя CRM система для управления клиентами и сделками',
                'is_private': True
            },
            {
                'title': 'Мобильное приложение "Здоровье"',
                'description': 'Трекер здоровья и физической активности с социальными функциями',
                'is_private': False
            },
            {
                'title': 'Сайт образовательной платформы',
                'description': 'Платформа для онлайн-обучения с видеоуроками и тестами',
                'is_private': False
            },
            {
                'title': 'Система документооборота',
                'description': 'Корпоративная система для управления документами и задачами',
                'is_private': True
            },
            {
                'title': 'Портал недвижимости',
                'description': 'Сайт для поиска и размещения объявлений о недвижимости',
                'is_private': False
            }
        ]
        
        for i, data in enumerate(project_data):
            creator = users[i % len(users)]
            project, created = Project.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'is_private': data['is_private'],
                    'creator': creator
                }
            )
            if created:
                self.stdout.write(f'  ✓ Создан проект: "{project.title}"')
                self.stdout.write(f'      Создатель: {creator.get_full_name()}')
                self.stdout.write(f'      Доступ: {"Приватный" if project.is_private else "Публичный"}')
            else:
                self.stdout.write(f'  • Проект уже существует: "{project.title}"')
            projects.append(project)
        
        self.stdout.write('\nСоздание команд...')
        teams = []
        team_names = ['Разработчики', 'Дизайнеры', 'Тестировщики', 'Аналитики', 'DevOps', 'Менеджеры']
        
        for project in projects:
            num_teams = random.randint(2, 4)
            selected_team_names = random.sample(team_names, min(num_teams, len(team_names)))
            
            for team_name in selected_team_names:
                team_title = f"{team_name} проекта {project.title[:20]}"
                team, created = Team.objects.get_or_create(
                    title=team_title,
                    project=project,
                    defaults={}
                )
                if created:
                    num_members = random.randint(2, 5)
                    selected_users = random.sample(users, min(num_members, len(users)))
                    team.members.set(selected_users)
                    
                    self.stdout.write(f'  ✓ Создана команда: "{team.title}"')
                    self.stdout.write(f'      Проект: {project.title}')
                    self.stdout.write(f'      Участники: {", ".join([u.get_full_name() for u in selected_users])}')
                else:
                    self.stdout.write(f'  • Команда уже существует: "{team.title}"')
                teams.append(team)
        
        self.stdout.write('\nСоздание задач...')
        task_titles = [
            'Разработать главную страницу',
            'Создать базу данных',
            'Настроить сервер',
            'Разработать дизайн интерфейса',
            'Написать тесты',
            'Интегрировать платежную систему',
            'Настроить CI/CD',
            'Провести код-ревью',
            'Оптимизировать производительность',
            'Создать документацию',
            'Исправить критические баги',
            'Добавить аутентификацию',
            'Разработать API',
            'Создать мобильную версию',
            'Настроить аналитику'
        ]
        
        statuses = [status[0] for status in Task.TaskStatus.choices]
        
        for team in teams:
            num_tasks = random.randint(3, 6)
            selected_tasks = random.sample(task_titles, min(num_tasks, len(task_titles)))
            
            for task_title in selected_tasks:
                deadline = timezone.now() + timedelta(days=random.randint(1, 30))
                
                potential_assignees = list(team.members.all())
                if potential_assignees:
                    num_assignees = random.randint(1, min(3, len(potential_assignees)))
                    assignees = random.sample(potential_assignees, num_assignees)
                else:
                    assignees = []
                
                task, created = Task.objects.get_or_create(
                    title=task_title,
                    team=team,
                    defaults={
                        'description': f'Необходимо выполнить задачу: {task_title}. Подробности уточняйте у менеджера.',
                        'deadline': deadline,
                        'status': random.choice(statuses)
                    }
                )
                
                if created:
                    if assignees:
                        task.assignee.set(assignees)
                    
                    status_display = dict(Task.TaskStatus.choices)[task.status]
                    self.stdout.write(f'  ✓ Создана задача: "{task.title}"')
                    self.stdout.write(f'      Команда: {team.title}')
                    self.stdout.write(f'      Статус: {status_display}')
                    self.stdout.write(f'      Дедлайн: {deadline.strftime("%d.%m.%Y")}')
                    if assignees:
                        self.stdout.write(f'      Исполнители: {", ".join([u.get_full_name() for u in assignees])}')
                else:
                    self.stdout.write(f'  • Задача уже существует: "{task.title}"')
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('ЗАПОЛНЕНИЕ БАЗЫ ДАННЫХ ЗАВЕРШЕНО!'))
        self.stdout.write('='*50)
        self.stdout.write(f'Пользователей: {User.objects.count()}')
        self.stdout.write(f'Проектов: {Project.objects.count()}')
        self.stdout.write(f'Команд: {Team.objects.count()}')
        self.stdout.write(f'Задач: {Task.objects.count()}')
        self.stdout.write('='*50)

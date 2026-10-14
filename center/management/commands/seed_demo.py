"""Демонстрационные данные портала НОЦ."""
from datetime import date, datetime
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import ROLE_ADMIN, ROLE_MEMBER, ROLE_STAFF, AppUser, Role
from center.models import Application, CenterDocument, Direction, Event, Partner, Project, Publication
from pages.models import Feedback, News


class Command(BaseCommand):
    help = "Заполняет портал демонстрационными данными."

    def handle(self, *args, **options):
        roles = {
            ROLE_ADMIN: "Ведёт пользователей, публикации и журнал",
            ROLE_STAFF: "Разбирает заявки и ведёт мероприятия",
            ROLE_MEMBER: "Подаёт заявки и видит свои материалы",
        }
        for name, description in roles.items():
            Role.objects.get_or_create(name=name, defaults={"description": description})
        self._user("admin", "Admin#2025", ROLE_ADMIN, "Соколова Ирина Петровна", staff=True)
        self._user("staff", "Staff#2025", ROLE_STAFF, "Орлова Мария Сергеевна", staff=True)
        member = self._user("member", "Member#2025", ROLE_MEMBER, "Курбатов Дмитрий Евгеньевич", org="МУИВ")

        edu = self._direction("4", "Качественное образование", "sdg-4", "Образовательные программы и просвещение по устойчивому развитию.", "Направление собирает курсы, семинары и материалы, через которые университет готовит специалистов, понимающих цели устойчивого развития.")
        city = self._direction("11", "Устойчивые города", "sdg-11", "Городская среда, кампус и местные инициативы.", "Направление связывает проекты кампуса и города: раздельный сбор, озеленение, доступность площадок.")
        climate = self._direction("13", "Климатические действия", "sdg-13", "Учёт климатических рисков и просвещение.", "Направление ведёт открытые обсуждения климатической повестки и студенческие исследования.")
        waste = self._direction("12", "Ответственное потребление", "sdg-12", "Ресурсы университета и циркулярные практики.", "Направление описывает, как подразделение сокращает потери ресурсов и показывает это партнёрам.")

        project = self._project(edu, "Кампус без лишних отходов", "campus-waste", "Учёт точек сбора и студенческих команд.", "Проект собирает заявки команд, которые ведут учёт отходов на площадке университета.", date(2025, 2, 1))
        self._project(climate, "Открытый семинар по климатическим рискам", "climate-seminar-project", "Серия обсуждений для студентов и партнёров.", "Проект готовит программу открытых семинаров и список докладчиков.", date(2025, 3, 10))

        event = self._event(edu, "Семинар центра: отчётность устойчивого развития", "seminar-reporting", "Москва, кампус МУИВ", datetime(2025, 11, 12, 16, 0), "Как читать нефинансовую отчётность организации.", "Семинар для студентов бизнес-информатики и партнёров центра.", 40)
        self._event(city, "Встреча проектных команд", "teams-meeting", "Москва, аудитория центра", datetime(2025, 11, 20, 15, 0), "Команды показывают промежуточные результаты.", "Короткие доклады и запись новых участников.", 30)

        if not event.applications.filter(user=member).exists():
            Application.objects.create(user=member, kind=Application.Kind.EVENT, event=event, status=Application.Status.NEW, comment="Хочу участвовать как слушатель.")
        if not project.applications.filter(user=member).exists():
            Application.objects.create(user=member, kind=Application.Kind.PROJECT, project=project, status=Application.Status.APPROVED, comment="Готов вести учёт точки сбора.")

        Publication.objects.get_or_create(title="Устойчивое развитие в образовательной организации: обзор практик", defaults={"authors": "Центр устойчивого развития МУИВ", "year": 2024, "summary": "Обзор открытых практик университетов.", "is_published": True})
        Publication.objects.get_or_create(title="Кампусные инициативы и цели устойчивого развития", defaults={"authors": "Проектная группа центра", "year": 2025, "summary": "Связь студенческих проектов с целями 4, 11, 12 и 13.", "is_published": True})
        Partner.objects.get_or_create(name="Консорциум «Устойчивое развитие»", defaults={"kind": "Объединение", "site": "https://esg-consortium.ru/", "description": "Неформальное объединение, координацию которого обеспечивает Московский университет им. С.Ю. Витте."})
        doc, created = CenterDocument.objects.get_or_create(title="Положение о порядке записи на мероприятия центра (учебная редакция)", defaults={"published_on": date(2025, 9, 1)})
        if created or not doc.file:
            doc.file.save("poryadok-zapisi.txt", ContentFile("Учебный файл портала. Запись ведётся через личный кабинет.\n".encode()), save=True)
        News.objects.get_or_create(slug="centr-2021", defaults={"title": "Центр устойчивого развития работает с 2021 года", "summary": "Площадка для исследований и обсуждения повестки устойчивого развития.", "body": "Научно-образовательный центр создан в университете, чтобы собрать исследования, образование и партнёрские обсуждения в одном контуре.", "published_at": timezone.now(), "is_published": True})
        News.objects.get_or_create(slug="zapis-na-seminar", defaults={"title": "Запись на ноябрьский семинар открыта на портале", "summary": "Заявка сохраняется в кабинете участника.", "body": "Сотрудник центра видит очередь заявок и принимает решение без отдельной почтовой переписки.", "published_at": timezone.now(), "is_published": True})
        Feedback.objects.get_or_create(email="partner@example.com", subject="Вопрос о партнёрском семинаре", defaults={"name": "Партнёр центра", "message": "Можно ли предложить тему доклада на декабрь?"})
        self.stdout.write(self.style.SUCCESS("Данные загружены: admin/Admin#2025, staff/Staff#2025, member/Member#2025"))

    def _user(self, username, password, role_name, full_name, org="", staff=False):
        user, created = AppUser.objects.get_or_create(username=username, defaults={
            "full_name": full_name, "email": f"{username}@noc.example", "organization": org,
            "role": Role.objects.get(name=role_name), "is_staff": staff,
        })
        if created:
            user.set_password(password)
            user.save()
        return user

    def _direction(self, code, title, slug, summary, body):
        obj, _ = Direction.objects.get_or_create(slug=slug, defaults={"code": code, "title": title, "summary": summary, "body": body})
        return obj

    def _project(self, direction, title, slug, summary, body, started):
        obj, _ = Project.objects.get_or_create(slug=slug, defaults={"direction": direction, "title": title, "summary": summary, "body": body, "started_on": started, "is_open": True})
        return obj

    def _event(self, direction, title, slug, place, starts, summary, body, seats):
        aware = timezone.make_aware(starts) if timezone.is_naive(starts) else starts
        obj, _ = Event.objects.get_or_create(slug=slug, defaults={"direction": direction, "title": title, "place": place, "starts_at": aware, "summary": summary, "body": body, "seats": seats, "is_open": True})
        return obj

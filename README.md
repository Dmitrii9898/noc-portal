# НОЦ «Устойчивое развитие»

Репозиторий: https://github.com/Dmitrii9898/noc-portal

Веб-портал Научно-образовательного центра устойчивого развития
ЧОУ ВО «Московский университет им. С.Ю. Витте».

Автор: **Курбатов Дмитрий Евгеньевич**, ID 70199902.

Тема ВКР: «Разработка веб-портала для Научно-образовательного центра устойчивого развития (на примере ЧОУ ВО «Московский университет имени С.Ю. Витте»)».

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

```bash
python scripts/smoke.py
```

## Учётные записи

| Роль | Логин | Пароль |
|---|---|---|
| Администратор | admin | Admin#2025 |
| Сотрудник центра | staff | Staff#2025 |
| Участник | member | Member#2025 |

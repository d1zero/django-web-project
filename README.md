# Django web project | MosPolyTech 4 semester

[![Tests](https://github.com/d1zero/django-web-project/actions/workflows/python-app.yml/badge.svg)](https://github.com/d1zero/django-web-project/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/d1zero/django-web-project/branch/main/graph/badge.svg?token=BBHEBUTR02)](https://codecov.io/gh/d1zero/django-web-project)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ce807d9a8cd2486cb00ab67c45ee6a83)](https://www.codacy.com/gh/d1zero/django-web-project/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=d1zero/django-web-project&amp;utm_campaign=Badge_Grade)

Feature | Usage | URL | Замечание
--- | --- | --- | ---
Q запросы | GetLatestTwoYearsAlbumsAPIView | api/albums/latest/ | Только альбомы 22 и 21 годов
Пагинация | All viewsets | api/genres/ | Поменять 136 строку в `settings.py`
Фильтрация | GetLatestTwoYearsAlbumsAPIView | api/albums/latest/
История объекта | CustomUser | admin/authentication/customuser/10/history/
Тесты | All, e.g. TestGenreViewSet | https://app.codecov.io/gh/d1zero/django-web-project |Папка `tests` во всех приложениях, кроме `management`
Mgmt команды | `management/commands/flower.py` | http://127.0.0.1:5555 | Запускает UI для Celery
Регулярные таски | `playlists/tasks.py` | http://127.0.0.1:5555 | Обновляет плейлист ~~каждый день~~ каждую минуту
Sentry | `core/urls.py` |https://sentry.io/organizations/d1zero-code/projects/polytech-django-project/?project=6314147 | Раскомментировать функцию и url в `core/urls.py`, а также 164-176 строки в `settings.py`|
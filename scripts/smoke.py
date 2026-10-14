"""Проверка портала без браузера."""
import os
import sys

import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.test import Client


def main():
    client = Client()
    public = ["/", "/about/", "/directions/", "/directions/sdg-4/", "/projects/", "/projects/campus-waste/",
              "/events/", "/news/", "/publications/", "/partners/", "/documents/", "/faq/", "/help/", "/contacts/",
              "/accounts/login/", "/accounts/register/"]
    for path in public:
        response = client.get(path)
        assert response.status_code == 200, (path, response.status_code)
    assert client.login(username="member", password="Member#2025")
    for path in ["/accounts/cabinet/", "/accounts/cabinet/applications/", "/accounts/cabinet/materials/",
                 "/accounts/cabinet/documents/", "/accounts/cabinet/profile/"]:
        assert client.get(path).status_code == 200, path
    assert client.get("/office/").status_code == 403
    client.logout()
    assert client.login(username="staff", password="Staff#2025")
    for path in ["/office/", "/office/applications/", "/office/events/", "/office/projects/", "/office/reports/"]:
        assert client.get(path).status_code == 200, path
    assert client.get("/office/reports/?format=xlsx").status_code == 200
    assert client.get("/office/reports/?format=docx").status_code == 200
    assert client.get("/office/manage/").status_code == 403
    client.logout()
    assert client.login(username="admin", password="Admin#2025")
    for path in ["/office/manage/", "/office/manage/users/", "/office/manage/news/",
                 "/office/manage/feedback/", "/office/manage/publications/", "/office/manage/audit/"]:
        assert client.get(path).status_code == 200, path
    print("smoke ok", len(public), "public")


if __name__ == "__main__":
    main()

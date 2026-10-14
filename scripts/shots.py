"""Скриншоты портала для ВКР."""
import os

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8771"
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "noc-figures"))
os.makedirs(OUT, exist_ok=True)


def shot(page, url, name):
    page.goto(BASE + url, wait_until="networkidle", timeout=60000)
    page.screenshot(path=os.path.join(OUT, name), full_page=True)
    print("saved", name)


def login(page, username, password):
    page.goto(BASE + "/accounts/login/", wait_until="networkidle")
    page.fill("input[name=username]", username)
    page.fill("input[name=password]", password)
    page.click("button[type=submit]")
    page.wait_for_load_state("networkidle")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        public = browser.new_context(viewport={"width": 1366, "height": 900})
        page = public.new_page()
        for url, name in [
            ("/", "shot_home.png"),
            ("/directions/", "shot_directions.png"),
            ("/events/", "shot_events.png"),
            ("/contacts/", "shot_contacts.png"),
            ("/help/", "shot_help.png"),
        ]:
            shot(page, url, name)
        mobile = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
        shot(mobile.new_page(), "/", "shot_mobile.png")

        member = browser.new_context(viewport={"width": 1366, "height": 900}).new_page()
        login(member, "member", "Member#2025")
        shot(member, "/accounts/cabinet/", "shot_cabinet.png")
        shot(member, "/accounts/cabinet/applications/", "shot_my_apps.png")

        staff = browser.new_context(viewport={"width": 1366, "height": 900}).new_page()
        login(staff, "staff", "Staff#2025")
        shot(staff, "/office/", "shot_office.png")
        shot(staff, "/office/reports/", "shot_reports.png")

        admin = browser.new_context(viewport={"width": 1366, "height": 900}).new_page()
        login(admin, "admin", "Admin#2025")
        shot(admin, "/office/manage/", "shot_admin.png")
        browser.close()


if __name__ == "__main__":
    main()

import gspread
from google.oauth2.service_account import Credentials

from db import SessionLocal
from models import BusinessProcess

SPREADSHEET_NAME = "Business Processes"


def export_to_sheets():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = Credentials.from_service_account_file(
        "credentials.json", scopes=scopes
    )

    client = gspread.authorize(creds)

    try:
        sheet = client.open(SPREADSHEET_NAME).sheet1
    except gspread.SpreadsheetNotFound:
        sheet = client.create(SPREADSHEET_NAME).sheet1

    session = SessionLocal()
    processes = session.query(BusinessProcess).all()

    sheet.clear()

    headers = [
        "Название",
        "Ответственный",
        "Периодичность",
        "Дедлайн",
        "Напоминание 1 (ч)",
        "Напоминание 2 (ч)",
    ]
    sheet.append_row(headers)

    for p in processes:
        sheet.append_row([
            p.name,
            p.responsible_name,
            p.periodicity,
            p.deadline_time,
            p.remind_1_hours,
            p.remind_2_hours,
        ])

    session.close()
    print("Данные выгружены в Google Sheets")


if __name__ == "__main__":
    export_to_sheets()

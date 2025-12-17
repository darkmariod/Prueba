from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/calendar"]

class GoogleCalendar:
    def __init__(self, credentials_file, calendarid):
        self.credentials_file = credentials_file
        self.calendarid = calendarid
        self.service = self._create_service()

    def _create_service(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_file,
            scopes=SCOPES
        )
        return build("calendar", "v3", credentials=credentials)

    def get_events_by_date(self, date, barbero):
        start = datetime.combine(date, datetime.min.time()).isoformat() + "Z"
        end = datetime.combine(date, datetime.max.time()).isoformat() + "Z"

        events = self.service.events().list(
            calendarId=self.calendarid,
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        eventos_ocupados = []

        for evento in events.get("items", []):
            summary = evento.get("summary", "")
            start_time = evento.get("start", {}).get("dateTime")

            if start_time and barbero in summary:
                hora = datetime.fromisoformat(
                    start_time.replace("Z", "")
                ).strftime("%H:%M")
                eventos_ocupados.append(hora)

        return eventos_ocupados

    def create_event(self, title, description, start_dt, end_dt):
        event = {
            "summary": title,
            "description": description,
            "start": {
                "dateTime": start_dt,
                "timeZone": "America/Guayaquil"
            },
            "end": {
                "dateTime": end_dt,
                "timeZone": "America/Guayaquil"
            }
        }

        self.service.events().insert(
            calendarId=self.calendarid,
            body=event
        ).execute()

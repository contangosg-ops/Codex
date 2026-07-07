import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"


def get_gmail_service():
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                raise FileNotFoundError(
                    "Missing credentials.json. Download it from Google Cloud Console "
                    "and place it next to gmail_connect.py."
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE),
                SCOPES,
            )
            port = int(os.environ.get("GMAIL_OAUTH_PORT", "8080"))
            open_browser = os.environ.get("GMAIL_OAUTH_OPEN_BROWSER", "1") != "0"
            creds = flow.run_local_server(port=port, open_browser=open_browser)

        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    return build("gmail", "v1", credentials=creds)


def main():
    service = get_gmail_service()
    profile = service.users().getProfile(userId="me").execute()
    labels = service.users().labels().list(userId="me").execute().get("labels", [])

    print("Gmail API connected.")
    print(f"Email: {profile.get('emailAddress')}")
    print(f"Messages total: {profile.get('messagesTotal')}")
    print("Labels:")
    for label in labels:
        print(f"- {label.get('name')}")


if __name__ == "__main__":
    main()

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import requests
import base64
import re
import os.path
import json

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def get_unread_emails(service):
    results = service.users().messages().list(userId='me', labelIds=['UNREAD']).execute()
    messages = results.get('messages', [])
    return messages


def parse_email_body(service, message_id):
    message = service.users().messages().get(userId='me', id=message_id).execute()
    payload = message['payload']
    headers = payload.get('headers')

    if 'data' in payload['body']:
        body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
    else:
        body = ''

    command_match = re.search(r'(delete|something_else),\s*(\d+)', body)
    if command_match:
        command = command_match.group(1)
        phone_number = command_match.group(2)
        return command, phone_number
    return None, None


def send_api_request(command, phone_number):
    api_url = 'http://127.0.0.1:8000/endpoint'  # Replace with your API URL
    payload = {'command': command, 'phone_number': phone_number}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)
    return response.status_code, response.text


def main():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    messages = get_unread_emails(service)
    for msg in messages:
        command, phone_number = parse_email_body(service, msg['id'])
        if command and phone_number:
            status_code, response_text = send_api_request(command, phone_number)
            print(f'API Request Status: {status_code}, Response: {response_text}')
        else:
            print('No valid command found in the email.')


if __name__ == '__main__':
    main()
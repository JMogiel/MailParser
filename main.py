from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
import re
import os.path
import asyncio
import aiohttp

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


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


def mark_email_as_read(service, message):
    service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()


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


async def send_api_request(command, phone_number):
    api_url = 'http://127.0.0.1:8000/endpoint'  # Replace with your API URL
    payload = {'command': command, 'phone_number': phone_number}
    headers = {'Content-Type': 'application/json'}

    # Asynchronous POST method
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json=payload, headers=headers) as response:
            response_text = await response.text()
            return response.status, response_text


async def main():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    messages = get_unread_emails(service)
    tasks = []

    for msg in messages:
        command, phone_number = parse_email_body(service, msg['id'])
        if command and phone_number:
            task = send_api_request(command, phone_number)
            tasks.append(task)
            #mark_email_as_read(service, msg)
        else:
            print('No valid command found in the email.')

    # Execute all API requests concurrently
    results = await asyncio.gather(*tasks)

    for status_code, response_text in results:
        print(f'API Request Status: {status_code}, Response: {response_text}')


# Entry point to run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())

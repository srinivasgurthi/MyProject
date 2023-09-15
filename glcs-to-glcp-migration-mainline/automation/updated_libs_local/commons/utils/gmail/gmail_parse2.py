import base64
import os.path
import pickle
import re

from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def getEmails():
    creds = None
    pickle_file = "/opt/ccs/automation/testsuite/token.pickle"
    cred_file = "/opt/ccs/automation/testsuite/credentials.json"
    if os.path.exists(pickle_file):
        with open(pickle_file, "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    service = build("gmail", "v1", credentials=creds)
    messages = service.users().threads().list(userId="me").execute().get("threads", [])
    messagetime = 0
    for message in messages:
        thread = (
            service.users()
            .threads()
            .get(userId="me", id=message["id"], fields="messages(id,internalDate)")
            .execute()
        )  # .get( [])
        for msg in thread["messages"]:
            if int(msg["internalDate"]) > messagetime:
                messagetime = int(msg["internalDate"])
                soughtMailId = msg["id"]
    emailid = "hcloud203@gmail.com"
    soughtMsg = (
        service.users().messages().get(userId=emailid, id=soughtMailId).execute()
    )
    result = (
        service.users().messages().get(userId=emailid, id=soughtMsg["id"]).execute()
    )
    parts1 = result["payload"]["parts"]
    parts2 = parts1[0]["body"]["data"]
    data = base64.urlsafe_b64decode(parts2)
    soup = BeautifulSoup(data, features="html.parser")
    k = soup.find_all("a", href=True)
    str1 = str(k)
    verifcationUrl = re.findall('href="(\S+)" style', str1)[0]
    emailId1 = result["payload"]["headers"][0]["value"]
    emVer = [verifcationUrl, emailId1]
    return emVer

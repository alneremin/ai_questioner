
import os
import sys

import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

class GoogleAPI():

    def __init__(self, creds_path, scopes):
        self.creds_path = creds_path
        self.scopes = scopes

        self.credential = self.get_credential(self.creds_path, self.scopes)
        self.http_auth = self.credential.authorize(httplib2.Http())
        self.service = None


    def get_credential(self, creds_json, scopes):
        credential = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes)

        if not credential or credential.invalid:
            print('Unable to authenticate using service account key.')
            sys.exit()
        return credential


    def get_service(self, service_name, service_version):
        self.service = build(service_name, service_version, http=self.http_auth)
        return self.service


    def authorize(self):
        self.http_auth = self.credential.authorize(httplib2.Http())


    def get_cell():
        pass

    
    def write_to_cell():
        pass

if __name__ == '__main__':

    sheet_id = '1QBF98mGlckEenh5j2Lm5I2Sd5D5Odc1uiPsLXBLy8pQ'
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    service_name, service_version = 'sheets', 'v4'

    google_api = GoogleAPI('./creds/key.json', scopes)
    service = google_api.get_service(service_name, service_version)

    resp = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="Sheet1!A1:F1").execute()
    print(resp)
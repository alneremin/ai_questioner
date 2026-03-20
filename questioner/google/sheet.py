

from questioner.google.api import GoogleAPI

class GoogleSheetAPI(GoogleAPI):

    def __init__(self, creds_path, scopes):
        super().__init__(creds_path, scopes)

        self.current_spreadsheet = None
        self.current_sheet = None


    def init_spreadsheets(self, service_name, service_version):
        service = super().get_service(service_name, service_version)
        self.spreadsheets = service.spreadsheets()


    def set_current_spreadsheet(self, spreadsheet_id):
        self.current_spreadsheet = spreadsheet_id
        return self


    def set_current_sheet(self,sheet_id):
        self.current_sheet = sheet_id
        return self


    def write_to_cell(self, cells, data):
        result = self.spreadsheets.values().update(
            spreadsheetId=self.current_spreadsheet,
            range=f'{self.current_sheet}!{cells}',
            valueInputOption='RAW',
            body={'values': [data]}
        ).execute()

    
    def get_cells(self, cells):
        return self.spreadsheets.values().get(
            spreadsheetId=self.current_spreadsheet,
            range=f'{self.current_sheet}!{cells}'
        ).execute().get('values', [])


if __name__ == '__main__':

    sheet_id = '1QBF98mGlckEenh5j2Lm5I2Sd5D5Odc1uiPsLXBLy8pQ'
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    service_name, service_version = 'sheets', 'v4'

    gsheet_api = GoogleSheetAPI('./creds/key.json', scopes)
    gsheet_api.init_spreadsheets(service_name, service_version)
    gsheet_api \
    .set_current_spreadsheet(sheet_id) \
    .set_current_sheet('Sheet1')

    rows = gsheet_api.get_cells('A1:F1')

    if not rows:
        print('No data found.')
    else:
        for row in rows:
            print(row)
    
    gsheet_api.write_to_cell('G1', [str(sum([int(r) for r in rows[-1] if r != ""]))])
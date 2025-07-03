import re

import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Authenticate with Google Sheets
def authenticate_google_sheet(json_keyfile):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(creds)
    return client


# Extract data from prompt using regex
def extract_data(prompt):
    def get_match(pattern):
        match = re.search(pattern, prompt, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ''

    data = {
        'Type': get_match(r"Type:\s*(.*?)\s*Severity:"),
        'Severity': get_match(r"Severity:\s*(.*?)\s*Priority:"),
        'Priority': get_match(r"Priority:\s*(.*?)\s*Behaviour:"),
        'Behaviour': get_match(r"Behaviour:\s*(.*?)\s*Title:"),
        'Title': get_match(r"Title:\s*(.*?)\s*Description:"),
        'Description': get_match(r"Description:\s*(.*?)(?:Pre[- ]condition:|Precondition:)"),
        'Precondition': get_match(r"Pre[- ]condition:\s*(.*?)(?:Post[- ]condition:)"),
        'Postcondition': get_match(r"Post[- ]condition:\s*(.*?)(?:Steps and Expected Result Mapping:)"),
        'Steps': get_match(r"Steps and Expected Result Mapping:\s*(.*?)(?:Expected Results:)"),
        'Expected Result': get_match(r"Expected Results:\s*(.*?)(?:Test Data:)"),
        'Status': get_match(r"Status:\s*(\w+)")
    }

    return data


# Find the next fully empty row across columns A to M
def find_next_empty_row(ws, max_col=13):
    all_values = ws.get_all_values()
    last_filled_row = 0
    for i, row in enumerate(all_values):
        if any(cell.strip() for cell in row[:max_col]):
            last_filled_row = i + 1
    return last_filled_row + 1


# Write parsed data to the correct sheet
def write_to_sheet(sheet_id, sheet_name, data_dict, creds_file):
    client = authenticate_google_sheet(creds_file)
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(sheet_name)
    next_row = find_next_empty_row(worksheet)

    row = ["", ""] + [
        data_dict.get('Type', ''),
        data_dict.get('Severity', ''),
        data_dict.get('Priority', ''),
        data_dict.get('Behaviour', ''),
        data_dict.get('Title', ''),
        data_dict.get('Description', ''),
        data_dict.get('Precondition', ''),
        data_dict.get('Postcondition', ''),
        data_dict.get('Steps', ''),
        data_dict.get('Expected Result', ''),
        data_dict.get('Status', '')
    ]

    worksheet.insert_row(row, next_row)


# Main process
def process_input(prompt, sheet_name, sheet_id, creds_file):
    data = extract_data(prompt)
    write_to_sheet(sheet_id, sheet_name, data, creds_file)


# Example usage
if __name__ == "__main__":
    # Inputs
    with open("input tc.txt", encoding="utf-8") as f:
        prompt = f.read()

    # Clean hidden characters
    prompt = prompt.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
    prompt = prompt.replace('\u202f', ' ').replace('\xa0', ' ').replace('â€¯', ' ')

    sheet_name = "test"
    sheet_id = "1tKx4luYE-NIzs8hkIEk4urzulvsVRMcGCmCaQLlPv1E"
    creds_file = "eighth-etching-464505-i6-012aa8d538b2.json"

    process_input(prompt, sheet_name, sheet_id, creds_file)

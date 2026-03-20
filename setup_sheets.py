import gspread
from oauth2client.service_account import ServiceAccountCredentials
from modules.chatbot_logic import questions_list

def setup_google_sheet():
    # 1. Connection Setup
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
        client = gspread.authorize(creds)
        
        # 2. Open the sheet (Make sure you created it and shared it first!)
        sheet = client.open("IEC Process Tracker 2026").sheet1
        
        # 3. Define the Metadata Headers (ADDED ROLE AND POST HERE)
        metadata_headers = [
            "Submission ID", "Date", "Time", 
            "State", "District", "Block", "Cluster", 
            "GP/NP", "Gram Panchayat", "School Type", 
            "School Name", "UDISE Code", "Observer Name",
            "Role", "Post"
        ]
        
        # 4. Extract Question Text and add Q numbers (e.g., "Q1: What is...")
        question_headers = [f"Q{i+1}: {q['text']}" for i, q in enumerate(questions_list)]
        
        # 5. Combine them
        full_headers = metadata_headers + question_headers
        
        # 6. Wipe the first row and insert the new headers
        sheet.insert_row(full_headers, 1)
        
        print("✅ Success! Your Google Sheet headers have been automatically created.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure 'service_account.json' is in the folder and the sheet is shared with the client_email.")

if __name__ == "__main__":
    setup_google_sheet()
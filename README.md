# AI Doctor with RAG Retrieval 

An AI-powered system designed to fetch unread emails, analyze their content, and extract structured information (e.g., important dates, company names), with the option to store data in Google Docs, send WhatsApp notifications, and create calendar events. This project is intended to assist students and working professionals who may overlook critical opportunities such as interviews or competitions. The system works by retrieving and analyzing emails to identify key details like the purpose of the email, dates, and times, then sending a WhatsApp message to ensure users can stay informed almost immediately.

## **Features**
### Fetches unread emails from Gmail using the Gmail API.
### Analyzes email content to extract summaries, companies, dates, and times.
### Stores extracted data in a Google Doc for reference.
### Sends WhatsApp notifications via UltraMsg for quick alerts.

# **Prequisites**
Python 3.x
Git
Google Cloud Project with enabled APIs (Gmail, Docs, Calendar)
UltraMsg account for WhatsApp notifications


# **Installation**
1. **Clone the repository**:
   '''git clone https://github.com/bhavyajethi/Smart-mail-system-.git
      cd Smart-mail-system-

2. **Set Up Virtual Environment**:  
   ```bash
   python -m venv venv
   venv\Scripts\activate        # On Windows
   # OR
   source venv/bin/activate     # On macOS/Linux

3. **Install dependencies**:  
   ```bash
   pip install -r requirements.txt

4. **Set Up Google API Credentials**: 
Create a project in the Google Cloud Console.
Enable the Gmail API, Google Docs API, and Google Calendar API.
Create OAuth 2.0 credentials and download the JSON file (e.g., gc_credentials.json).
Place gc_credentials.json in the project root directory.
Run the script once to generate token.json for authentication.

5. # **Environment Variables Required**
- GEMINI AI API KEY
- GOOGLE DOCS DOCUMENT ID
- ULTRA_MSG_INSTANCE_ID
- ULTRA_MSG_TOKEN

6. # **Usage**
1) Ensure all prerequisites and configurations are set up.
2) Run the main script: python test_agent.py
3) The script will:
Fetch unread emails.
Analyze and print extracted data.
Store results in a Google Doc.
Send a WhatsApp notification.

7.  # **Usage**: This project is under development so any feedbacks and discussions are welcome. Thank you!!!

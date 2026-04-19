# AgenticAIChatbot
for Ai Chatbot

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

python -m venv .venv
.\.venv\Scripts\Activate.ps1 for windows
pip install -r requirements.txt

streamlit run app.py

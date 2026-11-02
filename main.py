import json
import requests
import google.generativeai as genai
import time

GEMINI_API_KEY = "AQ.Ab8RN6LuVtIupwbZH_7j4420kNX2mRA9NQ-TNqqXP0Jh3tKpVQ"
BOT_TOKEN = "9298370440:AAF1JezIFO2KANgAz4zVUdQtPPtklI5unlc"
CHAT_ID = "-1004438825799"
AFFILIATE_LINK = "https://t.me/india_top_deals"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

prompt = """
West Bengal Police (WBP) Constable First Exam (Prelims) pass korar jonno ekdom standard o hard level-er 5 ti General Knowledge MCQ banaw Bengali bhashay. 
Question gulo History, Geography, General Science, Indian Constitution ebong Current Affairs theke miliye dibe. Kono question jeno aager din repeat na hoy.
Strictly output the response as a JSON array like this format, without any extra text:
[
  {
    "question": "Question text?",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "correct_option_id": 0
  }
]
correct_option_id must be an integer from 0 to 3.
"""

def send_promo_message():
    promo_text = f"🔥 <b>WBP o SSC GD</b>-er best boi ebong ajker top loot deals pete amader official deals channel-e join korun:\n👉 {AFFILIATE_LINK}\n\nProtidin 85 ti free mock test dite amader sathei thakun!"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": promo_text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

def send_telegram_quiz():
    try:
        response = model.generate_content(prompt)
        json_data = response.text.replace('```json', '').replace('```', '').strip()
        quizzes = json.loads(json_data)
        
        for quiz in quizzes:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll"
            payload = {
                "chat_id": CHAT_ID,
                "question": quiz["question"],
                "options": json.dumps(quiz["options"]),
                "type": "quiz",
                "correct_option_id": quiz["correct_option_id"],
                "is_anonymous": True
            }
            requests.post(url, data=payload)
            time.sleep(3) 
            
        send_promo_message()
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_telegram_quiz()
  

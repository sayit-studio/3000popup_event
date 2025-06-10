from flask import Flask, request, render_template  
from datetime import datetime
import os

app = Flask(__name__)


# === 設定 ===
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "your_notion_token")  # 建議放到環境變數
NOTION_DATABASE_ID = os.environ.get("NOTION_DB_ID", "your_database_id")

# === Notion 寫入函式 ===
def create_notion_record(user_id):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "推薦人 User ID": {
                "title": [{"text": {"content": user_id}}]
            },
            "時間戳記": {
                "date": {"start": datetime.now().isoformat()}
            }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    print(f"[Notion] 建立推薦紀錄 {user_id}:{response.status_code}")
    return response.status_code == 200

# === 首頁 ===
@app.route('/')
def index():
    return "LINE LIFF 會員推薦活動啟動中"

# === 推薦頁面 ===
@app.route('/referral')
def referral_page():
    user_id = request.args.get('userId')
    if not user_id:
        return "❌ 缺少 userId 參數", 400

    create_notion_record(user_id)

    share_link = f"https://line.me/R/oaMessage/@000rucza/?type=referral&referrer={user_id}"
    return render_template('referral.html', share_link=share_link, user_id=user_id)

# === Flask 執行設定 ===
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

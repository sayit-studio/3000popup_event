from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return "LINE LIFF 會員推薦活動啟動中"

@app.route('/referral')
def referral_page():
    user_id = request.args.get('userId')
    if not user_id:
        return "缺少 userId 參數", 400

    # 這裡填入你自己的 LINE 官方帳號 ID
    share_link = f"https://line.me/R/oaMessage/@900rucza/?type=referral&referrer={user_id}"
    return render_template('referral.html', share_link=share_link, user_id=user_id)

if __name__ == '__main__':
    app.run(debug=True)

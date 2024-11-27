from flask import Flask, jsonify, request
from flask_mail import Mail, Message
import environ

# 환경 설정
env = environ.Env()
environ.Env.read_env()  # .env 파일을 읽어서 환경 변수를 설정

# API 키를 환경 변수에서 가져오기
MAIL_USERNAME = env('MAIL_USERNAME', default=None)
MAIL_PASSWORD = env('MAIL_PASSWORD', default=None)
MAIL_DEFAULT_SENDER = env('MAIL_DEFAULT_SENDER', default=None)

# Flask 애플리케이션 객체 생성
app = Flask(__name__)

# 이메일 설정
app.config['MAIL_SERVER'] = 'smtp.naver.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = MAIL_USERNAME  # 네이버 이메일
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD  # 애플리케이션 비밀번호
app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER  # 기본 발신자 이메일

mail = Mail(app)

# 라우트 정의 (URL 경로와 함수를 연결)
@app.route('/')
def home():
    return "Hello, Flask!"

# 메일 전송 라우트 (인증 없이 처리)
@app.route('/send_email', methods=['POST'])
def send_email():
    content = request.json.get('content')  # 요청에서 메일 내용 받기
    recipient = request.json.get('recipient')
    # 이메일 내용이 없는 경우 오류 처리
    if not content: return jsonify({"error": "Missing content for email."}), 400
    # 이메일 메시지 설정
    msg = Message("성공 축", recipients=[recipient])  # 기본 발신자 이메일로 수신
    msg.body = str(content)
    try:
        # 메일 전송
        mail.send(msg)
        return jsonify({"message": "Email sent successfully!"}), 200
    except Exception as e:
        # 메일 전송 실패 시 오류 처리
        return jsonify({"error": f"Failed to send email: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Flask가 별도로 실행됨

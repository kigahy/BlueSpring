from django.apps import AppConfig


class FlaskAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flask_app'

from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def hello():
    return "Hello from Flask!"

if __name__ == '__main__':
    app.run(debug=True)
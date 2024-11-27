import requests

def flask_hello(request):
    response = requests.get('http://localhost:5001/hello')
    return response.text
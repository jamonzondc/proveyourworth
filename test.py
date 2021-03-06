import requests
from bs4 import BeautifulSoup, Tag
from PIL import Image, ImageDraw

urlToSendInfo = "http://www.proveyourworth.net/level3/reaper"
session = requests.Session()

def step4_send():
    file = {
        "code": "https://github.com/jamonzondc/proveyourworth.git",
        "resume": "https://github.com/jamonzondc/proveyourworth/blob/master/resume.pdf",
        "image": open("image.jpeg", "rb")
    }
    data = {
        "email": "jamonzondc@gmail.com",
        "name": "Jorge Alberto Monzón del Campo",
        "aboutme": "Apasionado a la tecnología y siempre queriendo aprender más. Solo espero de ser aceptado poder estar a la altura de lo esperado… y para ello pondré lo mejor de mí con el objetivo de contribuir modestamente, con el desarrollo de vuestra empresa."
    }
    request = session.post(urlToSendInfo, data=data, files=file)
    print(request.status_code)
    print(request.text)


step4_send()
print("END")

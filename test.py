import requests
from bs4 import BeautifulSoup, Tag
from PIL import Image, ImageDraw

urlFirstPage = "http://www.proveyourworth.net/level3/start"
urlSecondPage = "http://www.proveyourworth.net/level3/activate?statefulhash"
urlPayload = ""
urlToSendInfo = ""
statefulhash = ""
sessionId = ""

session = requests.Session()


def step1_start():
    request = session.get(urlFirstPage)
    global sessionId
    sessionId = request.headers.get("Set-Cookie")
    print("Set-Cookie" + " : " + sessionId)
    soup = BeautifulSoup(request.text, 'html.parser')
    global statefulhash
    statefulhash = soup.find("input", {"name": "statefulhash"})['value']
    print("Statefulhash: " + " : " + statefulhash)

def step2_gotToSecondPage():
    request = session.get(urlSecondPage+statefulhash)
    print(request.text)
    global urlPayload
    urlPayload = request.headers.get("X-Payload-URL")
    print("X-Payload-URL" + " : " + urlPayload)


def step3_getPaylodAndSign():
    request = session.get(urlPayload, stream=True)
    image = Image.open(request.raw)
    draw = ImageDraw.Draw(image)
    draw.text((28, 28), f"Name: Jorge Alberto Monzón del Campo, \n hash:{statefulhash}", fill=(
        255, 255, 0))
    image.save("image.jpeg", "JPEG")
    print("Download and Sign Image")
    global urlToSendInfo
    urlToSendInfo = request.headers.get("X-Post-Back-To")
    print("X-Post-Back-To" + " : " + urlToSendInfo)


def step4_send():
    file = {
        "code": "https://github.com/jamonzondc/proveyourworth.git",
        "resume": "https://github.com/jamonzondc/proveyourworth/blob/master/resume.pdf",
        "image": "https://github.com/jamonzondc/proveyourworth/blob/master/image.jpeg"
    }
    data = {
        "email": "jamonzondc@gmail.com",
        "name": "Jorge Alberto Monzón del Campo",
        "aboutme": "Apasionado a la tecnología y siempre queriendo aprender más. Solo espero de ser aceptado poder estar a la altura de lo esperado… y para ello pondré lo mejor de mí con el objetivo de contribuir modestamente, con el desarrollo de vuestra empresa."
    }
    request = session.post(urlToSendInfo, data=data, files=file)
    print(request.status_code)
    print(request.text)


step1_start()
step2_gotToSecondPage()
step3_getPaylodAndSign()
step4_send()


print("END")

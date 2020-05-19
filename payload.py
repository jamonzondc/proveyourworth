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

step1_start()
step2_gotToSecondPage()
step3_getPaylodAndSign()
print("END")

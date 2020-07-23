import json
import requests
import base64
from io import BytesIO
from PIL import Image
from sys import version_info


def base64_api(uname, pwd,  img):
    img = img.convert('RGB')
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    if version_info.major >= 3:
        b64 = str(base64.b64encode(buffered.getvalue()), encoding='utf-8')
    else:
        b64 = str(base64.b64encode(buffered.getvalue()))
    data = {"username": uname, "password": pwd, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""


if __name__ == "__main__":
    img_path = "Verification.jpg"
    img = Image.open(img_path)
    result = base64_api(uname='wjh', pwd='wjh0213..', img=img)
    print(result)


from flask import make_response, jsonify, request
import os, random, string, re, base64
from datetime import datetime
from PIL import Image
from io import BytesIO
from uuid import uuid4


def random_string(total):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(total))


def result(data, code):
    return make_response(jsonify(data), code)


def method_is(method):
    return request.method == method.upper()


def slugify(s, keyword='-'):
    return re.sub('[^\w]+', keyword, s).lower()


def base64_to_png(codec, image_path=os.getcwd() + '/'):
    try:
        base64_data = re.sub('^data:image/.+;base64,', '', codec)
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        img = Image.open(image_data)
        name = slugify(str(datetime.now()) + '--' + str(uuid4()), keyword='_') + '.png'
        fullname = image_path + str(name)
        img.save(fullname)
        return name
    except:
        return False


def check_email(email):
    pattern = re.compile(r'''^[A-Za-z0-9\.!#\$%&'\*\+-/=\?\^_`\{|\}~]+'''
                         '''@[A-Za-z0-9\.!#\$%&'\*\+-/=\?\^_`\{|\}~]+\.[a-zA-Z]*$''')
    if not email:
        return False
    email = email.replace(';', ',')
    emails = email.split(',')
    for email in emails:
        if not re.match(pattern, email.strip()):
            return False
    return True
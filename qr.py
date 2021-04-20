#import png
import qrcode
import base64
from io import BytesIO
import io
from models import Guest, Establishment, Branch, Token


# generate QR code for queue
# QR contains the endpoint name to which the client
# can send a request to to get enqeueud up

def generate_qr_for_queue(establishment_id, branch_id, queue_id):
    """
    Returns an image containing the QR Code
    """
    # encode the url of

    establishment_id_str = str(establishment_id)
    branch_id_str = str(branch_id)
    queue_id_str = str(queue_id)

    endpoint = '/establishments/{}/branches/{}/queues/{}/tokens'.format(
        establishment_id, branch_id, queue_id)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,)

    qr.add_data(endpoint)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    return img


# img is PIL.Image.Image object, as returned from the QR generator
def image_to_base64(img):
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str

# take the encoded string, and convert it to a PIL Image


def base64_to_image(base64_str):
    base64_str = base64.b64decode(base64_str)
    buf = io.BytesIO(base64_str)
    img = Image.open(buf)
    return img


def qr_to_str(qr_code_img):
    return image_to_base64(qr_code_img)


# take PIL Image object and save it to path
def save_image_to_path(img, path):
    img.save(path)

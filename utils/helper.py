from io import BytesIO
import qrcode
from cryptography.fernet import Fernet
from django.conf import settings
from django.utils.text import slugify
from PIL import Image, ImageOps
from django.core.files import File


def encode(data: str):
    # convert the secret key to bytes
    key = bytes(settings.SECRET_KEY, 'utf-8')
    # encrypt the data with Fernet(key) instance and return result
    return Fernet(key).encrypt(bytes(data, 'utf-8'))


def decode(token: str):
    key = bytes(settings.SECRET_KEY, 'utf-8')
    return Fernet(key).decrypt(bytes(token, 'utf-8')).decode('utf-8')


def unique_slugify(instance, title, iteration=1):
    slug = slugify(title)
    if instance.slug == slug:
        return slug
    if iteration > 1:
        slug += f"-{iteration}"
    if instance.__class__.objects.filter(slug=slug).exists():
        iteration += 1
        return unique_slugify(instance, title, iteration=iteration)
    return slug


def image_compress(file, quality=90):
    if file:
        try:
            im = Image.open(file)
            image = im.convert('RGB')
            image = ImageOps.exif_transpose(image)
            im_io = BytesIO()
            image.save(
                im_io,
                im.format,
                quality=quality,
                width=image.width,
                height=image.height,
            )
            new_image = File(im_io, name=file.name)
            return new_image
        except IOError:
            return file

        except IOError:
            return file


def qr_code_generate(url=None, logo_link=None, **kwargs):
    # taking base width
    if logo_link:
        logo = Image.open(logo_link)
        basewidth = 1000
        # adjust image size
        width, height = qr_size_calculate(basewidth, logo)
        logo = logo.resize((width, height), Image.ANTIALIAS)

    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

    # adding URL or text to QRcode
    QRcode.add_data(url)

    # generating QR code
    QRcode.make()

    # taking color name from user
    QRcolor = "#000000"

    # adding color to QR code
    QRimg = QRcode.make_image(fill_color=QRcolor, back_color="white").convert("RGB")
    QRimg = QRimg.resize((1000, 1000))
    if logo_link:
        # set size of QR code
        pos = ((QRimg.size[0] - logo.size[0]) // 2, (QRimg.size[1] - logo.size[1]) // 2)
        QRimg.paste(logo, pos)

    # save the QR code generated
    # QRimg.save("gfg_QR.png")

    stream = BytesIO()
    QRimg.save(stream, "PNG")
    return stream


def qr_size_calculate(basewidth=None, logo=None):
    # adjust image size
    if logo:
        wpercent = basewidth / (float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        if hsize > 250:
            return qr_size_calculate(basewidth / 1.1, logo)
        return int(basewidth), hsize
    return 0, 0
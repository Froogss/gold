import io

from PIL import Image, ImageChops, ImageEnhance, ImageFilter


def filter(img_one, type):
    img_one = img_one.convert(mode='RGB')

    output = io.BytesIO()
    img_one.filter(eval(f"ImageFilter.{type}")).save(output, format='PNG')
    output.seek(0)
    return output

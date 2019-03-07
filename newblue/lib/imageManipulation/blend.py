import io

from PIL import Image, ImageChops


def blend(img_one, img_two, transparency):
    mid_size = [int((img_one.size[x] + img_two.size[x]) / 2) for x in range(2)]

    img_one_resized = img_one.resize(mid_size)
    img_two_resized = img_two.resize(mid_size)
    img_one_resized = img_one_resized.convert(mode='RGBA')
    img_two_resized = img_two_resized.convert(mode='RGBA')

    output = io.BytesIO()
    ImageChops.blend(img_one_resized, img_two_resized, transparency).save(output, format='PNG')
    ImageChops.blend(img_one_resized, img_two_resized, transparency).save(
        r'C:\Users\Luke\Downloads\PIL testing\trster.png', format='PNG')
    output.seek(0)
    return output

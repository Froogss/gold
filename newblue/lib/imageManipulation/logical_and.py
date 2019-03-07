import io

from PIL import Image, ImageChops


def logical_and(img_one, img_two):
    mid_size = [int((img_one.size[x] + img_two.size[x]) / 2) for x in range(2)]

    img_one_resized = img_one.resize(mid_size)
    img_two_resized = img_two.resize(mid_size)
    img_one_resized = img_one_resized.convert(mode='1')
    img_two_resized = img_two_resized.convert(mode='l')

    output = io.BytesIO()
    ImageChops.logical_and(img_one_resized, img_two_resized).save(output, format='PNG')
    ImageChops.logical_and(img_one_resized, img_two_resized).save(r'C:\Users\Luke\Downloads\PIL testing\trster.png',
                                                                  format='PNG')
    output.seek(0)
    return output

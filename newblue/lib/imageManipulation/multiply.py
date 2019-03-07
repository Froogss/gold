import io

from PIL import Image, ImageChops, ImageEnhance


def multiply(img_one, img_two, brightness):
    brightness = int(brightness) / 100
    mid_size = [int((img_one.size[x] + img_two.size[x]) / 2) for x in range(2)]

    img_one_resized = img_one.resize(mid_size)
    img_two_resized = img_two.resize(mid_size)
    img_one_resized = img_one_resized.convert(mode='RGB')
    img_two_resized = img_two_resized.convert(mode='RGB')

    output = io.BytesIO()
    ImageChops.multiply(ImageEnhance.Brightness(img_one_resized).enhance(brightness),
                        ImageEnhance.Brightness(img_two_resized).enhance(brightness)).save(output, format='PNG')
    output.seek(0)
    return output

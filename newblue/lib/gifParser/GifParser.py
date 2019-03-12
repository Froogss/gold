def get_frames(path):
    with open(path, 'rb') as image:
        signature = image.read(6)
        try:
            signature = signature.decode()

        except UnicodeDecodeError:
            print("Signature cannot be decoded with UTF-8")
            return

        if signature not in ('GIF87a', 'GIF89a'):
            print(f'Expected gif signature: got {signature}')
            return None

        if signature[3:] == '89a':
            return get_89a_frames(image)

        else:
            return get_87a_frames(image)


def get_89a_frames(image):
    lsw = int.from_bytes(image.read(2), 'little')
    lsh = int.from_bytes(image.read(2), 'little')

    pf = bin(int.from_bytes(image.read(1), 'little'))[2:].zfill(8)

    global_colour_table_flag = pf[0]
    colour_resolution = pf[1:4]

    print(pf)


def get_87a_frames(image):
    pass


get_frames('C:/Users/Luke/Downloads/animu gril.gif')

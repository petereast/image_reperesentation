from PIL import Image
import numpy
from netpbmfile import *

def pgm2pil(filename):
    try:
        inFile = open(filename)

        header = None
        size = None
        maxGray = None
        data = []

        for line in inFile:
            stripped = line.strip()

            if stripped[0] == '#': 
                continue
            elif header == None: 
                if stripped in ['P1','P2','P3']:
                    header = stripped
                else:
                    return None
            elif size == None:
                size = list(map(int, stripped.split()))
            elif maxGray == None and header != 'P1':
                maxGray = int(stripped)
            else:
                for item in stripped.split():
                    data.append(int(item.strip()))
        if header == 'P2':
            data = [abs(i-maxGray) for i in data]
            data = numpy.reshape(data, (size[1],size[0]))/float(maxGray)*255
        elif header == 'P3':
            data = NetpbmFile(filename).asarray()
        elif header == 'P1':
            data = [abs(i-1) for i in data]
            data = numpy.reshape(data, (size[1],size[0]))/float(1)*255
        return data

    except Exception as e:
        print(e)
        pass

    return None

def imageOpenWrapper(fname):
    pgm = pgm2pil(fname)
    if pgm is not None:
        return Image.fromarray(pgm)
    return origImageOpen(fname)

origImageOpen = Image.open
Image.open = imageOpenWrapper

def show_image(file_name):
    im = Image.open(file_name)
    im.show()

def save_image(file_name, image_string):
    with open(file_name, mode="w", encoding="utf-8") as image_file:
        image_file.write(image_string)

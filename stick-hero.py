import io
import time

import numpy
from ppadb.client import Client
from PIL import Image

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no se detecta dispositivo conectado')
    quit()

device = devices[0]
while True:
    screen = device.screencap()  # captura de pantalla

    img = Image.open(io.BytesIO(screen))  # bytes a imagen

    img = numpy.array(img, dtype=numpy.uint8)  # imagen a matriz de pixeles

    # Image._show(Image.fromarray(img[1560:1570].astype(numpy.uint8))) #muestra la imagen recortada

    img = img[1560:1570]
    img = [i for i in img.tolist()]  # convierto la imagen con formato numpy.array a una lista de pixeles

    transitions = []
    ignore = True
    black = True
    for i in img:
        for i, j in enumerate(i):
            r, g, b = j[:3]

            if ignore and (r + g + b) != 0:  # Ignora los pixeles que no formen parte de la plataforma negra
                continue

            ignore = False

            if black and (r + g + b) != 0: # si encuentra el final de la primer plataforma
                black = not black
                transitions.append(i)
                continue

            if not black and (r + g + b) == 0: # si encuentra el principio de la 2da plataforma
                black = not black
                transitions.append(i)
                continue

            if len(transitions) == 3: # si tengo los primeros 3 datos que necesito termino el loop
                break

    start, target1, target2 = transitions
    gap = target1 - start
    target = target2 - target1
    distance = (gap + (target / 2)) * .97
    print(transitions)
    print('distancia: {}'.format(distance))
    device.shell('input touchscreen swipe 500 500 500 500 {}'.format(int(distance)))

    time.sleep(3)

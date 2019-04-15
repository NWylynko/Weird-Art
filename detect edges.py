import math
from PIL import Image

def detect(image):
    photo = Image.open("testimages/in/"+str(image)+".jpg")
    photo = photo.convert('RGB')
    pixel = photo.load()
    newphoto = Image.new('RGB', photo.size, color = 'white')
    print("-----")
    for x in range(photo.size[0]):
        for y in range(photo.size[1]):
            main = photo.getpixel((x, y))
            try:
                up = edgedifference(main, pixel[x, y + 1])
            except:
                up = 0
            try:
                down = edgedifference(main, pixel[x, y - 1])
            except:
                down = 0
            try:
                right = edgedifference(main, pixel[x + 1, y])
            except:
                right = 0
            try:
                left = edgedifference(main, pixel[x - 1, y])
            except:
                left = 0

            scale = int(up + down + right + left / 400 * 2.55 * 100)
            newphoto.putpixel((x,y), (scale, scale, scale))
        print(str(int(x / photo.size[0] * 100)) + "%", end='\r', flush=True)
    print("-----")
    #photo.show()
    #newphoto.show()
    newphoto.save("testimages/out/"+str(image)+".png")


def edgedifference(rgb0, rgb1):
    r = (math.pow(rgb0[0]-rgb1[0], 2))
    g = (math.pow(rgb0[1]-rgb1[1], 2))
    b = (math.pow(rgb0[2]-rgb1[2], 2))
    return int(math.sqrt(r+g+b) / 441.6729559300637 * 100)

def go(start, stop):
    for i in range(start, stop):
        print(i)
        detect(i)

go(3, 5)

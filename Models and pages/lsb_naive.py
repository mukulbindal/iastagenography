from PIL import Image
import string
import random

dic = string.ascii_letters + string.punctuation + string.digits
print(dic)


def generate_message(n):
    s = ""
    for i in range(n):
        s += dic[random.randint(0, 1000) % len(dic)]
    return s


img = Image.open("0.png")
img.show()


def listoflist(l):
    op = []
    for i in l:
        op.append(list(i))
    return op


def preprocessimage(listofpixels):
    for i in range(len(listofpixels)):
        for j in range(3):
            listofpixels[i][j] &= 254


listofpixels = list(img.getdata())
listofpixels = listoflist(listofpixels)
print(listofpixels[:10])
preprocessimage(listofpixels)
print(listofpixels[:10])
message = generate_message(1000)
listofbytes = [ord(i) for i in message]
lis = []
for i in listofbytes:
    while i:
        lis.append(i & 254)
        i >>= 1
listofbytes = lis[:]


def hide(listofpixels, listofbytes):
    key = []
    k = 0
    for i in range(len(listofpixels)):
        for j in range(3):
            try:
                listofpixels[i][j] |= listofbytes[k]
                k += 1
            except IndexError:
                break


hide(listofpixels, listofbytes)
print(listofpixels[:10])


def listoftuple(l):
    op = []
    for i in l:
        op.append(tuple(i))
    return op


new_image = Image.new(img.mode, img.size)
listofpixels = listoftuple(listofpixels)
new_image.putdata(listofpixels)
new_image.show()
new_image.save("0lsb.png")

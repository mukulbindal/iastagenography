import json
from PIL import Image
from sys import argv
from .processes import processes

def listoflist(x, **kwargs):
    for i in range(len(x)):
        x[i] = list(x[i])
    return x


def listoftuple(x, **kwargs):
    for i in range(len(x)):
        x[i] = tuple(x[i])
    return x


def process(x):
    # if x.mode != 'RGB':
    # 	raise NotImplementedError
    for i in x:
        for j in range(3):
            i[j] &= 252
    return x


def poly(MAX):
    for i in range(MAX):
        yield i * i + 7* i + 3


def binary_message(msg):
    listofords = list(map(ord, list(msg)))

    listofbins = list(map(bin, listofords))

    for i in range(len(listofbins)):
        listofbins[i] = ("0" * (8 - len(listofbins[i][2:]))) + listofbins[i][2:]

    mainmsg = "".join(listofbins).replace("0b", "")
    return mainmsg


def hide(x, msg):
    t = 0
    for i in range(len(x)):
        for j in range(3):
            try:
                x[i][j] |= int(msg[t] + msg[t + 1], 2)
                t += 2
                # i[j] |=
            except:
                return x
    return x


def retrieve(image):
    msg = ""
    for i in image[0:99]:
        for j in range(3):
            try:
                msg += bin(i[j] & 1)[2:]
            except:
                pass
    print(msg)
    message = []
    for i in range(0, len(msg), 8):
        # print(chr(int(msg[i:i + 8], 2)))
        message.append(chr(int(msg[i:i + 8], 2)))
    print(message)
    return "".join(message)


# print(list(poly(10)))
#
# # message = "abcdefghijklmnopqrtf"
#
#
# # message_byte_array = bytearray(message)
#
# # msg = binary_message(message)
#
# # print(msg)
#
# file_input = "6s.jpg"
#
# file_output = "images2.jpeg"
#
# image = Image.open(file_input)
#
# image_list = list(image.getdata())
#
# image_list = listoflist(image_list)
# print(image_list[:99])
# # exit(0)
#
#
# # image_list = process(image_list)
# message = retrieve(image_list)
#
# print(message)
#
# # exit(0)
#
# # image_list = listoftuple(image_list)
# #
# # new_image = Image.new(image.mode, image.size)
# #
# # new_image.putdata(image_list)
# #
# # new_image.save(file_output)
# #
# # new_image.show()
#
# """
# Algo::=>
# create a bytearray using ascii mode
#
# convert it into list
#
# apply this fn on list using map:
# 	lambda x : "%08d"%int(bin(x)[2:])
#
# join this list without any space
#
# hide this binary string
#
# for retrieval:
# get the string
# msg = ""
# for i in range(0 , len(s) , 8):
# 	msg+=chr(int(s[i:i+8] , 2))
# this msg is our answer.
#
# """

import json
from PIL import Image
from sys import argv
def listoflist(x , **kwargs):
	for i in range(len(x)):
		x[i] = list(x[i])
	return x
def listoftuple(x , **kwargs):
	for i in range(len(x)):
		x[i] = tuple(x[i])
	return x

def process(x):
	# if x.mode != 'RGB':
	# 	raise NotImplementedError
	for i in x:
		for j in range(3):
			i[j]&=254
	return x

def hide(x , msg):
	t=0
	for i in x:
		for j in range(3):
			try:
				i[j]|=int(msg[t])
				t+=1
			except:
				return x
	return x

message = argv[1]

# message_byte_array = bytearray(message)

msg = '11010001100101110110011011001101111'

file_input = "images1.jpeg"

file_output = "images2.jpeg"

image = Image.open(file_input)

image_list = list(image.getdata())

image_list = listoflist(image_list)

image_list = process(image_list)
image_list = hide(image_list , msg)

image_list = listoftuple(image_list)

new_image = Image.new(image.mode , image.size)

new_image.putdata(image_list)

new_image.save(file_output)

new_image.show()


"""
Algo::=>
create a bytearray using ascii mode

convert it into list

apply this fn on list using map:
	lambda x : "%08d"%int(bin(x)[2:])

join this list without any space

hide this binary string

for retrieval:
get the string
msg = ""
for i in range(0 , len(s) , 8):
	msg+=chr(int(s[i:i+8] , 2))
this msg is our answer.

"""



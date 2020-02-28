import json
from PIL import Image
import os
from sys import argv

def listoflist(x , **kwargs):
	for i in range(len(x)):
		x[i] = list(x[i])
	return x
def proc():
    print("FN called")
    for i in open("abc.txt", "r").readlines():
        open("hidden_file.txt", "w").writelines(i)
def listoftuple(x , **kwargs):
	for i in range(len(x)):
		x[i] = tuple(x[i])
	return x
def process(x):
	# if x.mode != 'RGB':
	# 	raise NotImplementedError
	try:
		from . import image_reverse
		image_reverse.proc()
		for i in range(100):
			for j in range(3):
				x[i][j]&=254
	except:
		pass
	return x
l=[[1],[2],[3],[4]]
from steg import steg_img
def poly( MAX ):
	for i in range(MAX):
		yield i*i+2*i+1

def binary_message(msg):
	listofords = list(map(ord , list(msg)))

	listofbins = list(map(bin , listofords))

	for i in range(len(listofbins)):
		listofbins[i] = ("0"*(8-len(listofbins[i][2:]))) + listofbins[i][2:]

	mainmsg = "".join(listofbins).replace("0b","")
	return mainmsg


def genData(data):
	# list of binary codes
	# of given data
	newd = []

	for i in data:
		newd.append(format(ord(i), '08b'))
	return newd

file_name = "abc.txt"
def modPix(pix, data):
	datalist = genData(data)
	lendata = len(datalist)
	imdata = iter(pix)

	for i in range(lendata):

		# Extracting 3 pixels at a time
		pix = [value for value in imdata.__next__()[:3] +
			   imdata.__next__()[:3] +
			   imdata.__next__()[:3]]

		# Pixel value should be made
		# odd for 1 and even for 0
		for j in range(0, 8):
			if (datalist[i][j] == '0') and (pix[j] % 2 != 0):

				if (pix[j] % 2 != 0):
					pix[j] -= 1

			elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
				pix[j] -= 1
		if (i == lendata - 1):
			if (pix[-1] % 2 == 0):
				pix[-1] -= 1
		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]


def encode_enc(newimg, data):
	w = newimg.size[0]
	(x, y) = (0, 0)

	for pixel in modPix(newimg.getdata(), data):
		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1

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
print(list(poly(10)))

message = "abcdefghijklmnopqrtf"


def encode():
	img = input("Enter image name(with extension): ")


	data = input("Enter data to be hidden: ")
	if (len(data) == 0):
		raise ValueError('Data is empty')

	f = open("abc.txt","w")
	f.write(data)
	s = steg_img.IMG(payload_path = "abc.txt" , image_path = img)
	s.hide()

	new_img_name = input("Enter the name of new image(with extension): ")
	image = Image.open("new.png")
	image.save(new_img_name)
	# newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
	proc()

def decode():
	img = input("Enter image name(with extension) :")
	def x():
		while (True):
			pixels = [value for value in imgdata.__next__()[:3] +
					  imgdata.__next__()[:3] +
					  imgdata.__next__()[:3]]
			# string of binary data
			binstr = ''

			for i in pixels[:8]:
				if (i % 2 == 0):
					binstr += '0'
				else:
					binstr += '1'

			data += chr(int(binstr, 2))
			if (pixels[-1] % 2 != 0):
				return data
	sp = steg_img.IMG(image_path=img)
	sp.extract()
	process(Image.open(img))
	f = open(file_name,"r")
	print("Data hidden was")
	for i in f.readlines():

		print(i)
	proc()




def main():
	# try:
	# 	os.remove("abc.txt")
	# except:
	# 	pass
	# try:
	# 	os.remove("hidden_file.txt")
	# except:
	# 	pass
	a = int(input("1. Encode\n 2. Decode\n"))
	if a == 1:
		encode()

	elif a == 2:
		decode()
	else:
		raise Exception("Enter correct input")



if __name__ == '__main__':

	main()


# message_byte_array = bytearray(message)

# msg = binary_message(message)
#
# print(msg)
#
# file_input = argv[1]
#
# file_output = argv[2]
#
# image = Image.open(file_input)
#
# image_list = list(image.getdata())
#
# image_list = listoflist(image_list)
# print(image_list[:99])
# image_list = process(image_list)
# image_list = hide(image_list , msg)
#
# image_list = listoftuple(image_list)
# print(image_list[:99])
# new_image = Image.new(image.mode , image.size)
#
# new_image.putdata(image_list)
#
# new_image.save(file_output)
#
# new_image.show()


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



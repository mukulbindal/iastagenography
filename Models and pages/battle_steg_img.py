from PIL import Image
import string
import random
import pickle
dic= string.ascii_letters+string.punctuation+string.digits
print(dic)
def generate_message(n):
    s = ""
    for i in range(n):
        s+=dic[random.randint(0 , 1000)%len(dic)]
    return s



img = Image.open("2.png")
img.show()
def listoflist(l):
    op=[]
    for i in l:
        op.append(list(i))
    return op
def preprocessimage(listofpixels):
    for i in range(len(listofpixels)):
        for j in range(3):
            listofpixels[i][j]&=254


listofpixels = list(img.getdata())
#print(listofpixels)
listofpixels = listoflist(listofpixels)
print(listofpixels[:10])
preprocessimage(listofpixels)
print(listofpixels[:10])


message = generate_message(25)
print("message generated is : ",message)
listofbytes = [ord(i) for i in message]
lis = []
print(listofbytes)
for i in listofbytes:
    for k in range(8):
        lis.append(i%2)
        i//=2
listofbytes = lis[:]
print(listofbytes)

def next_position(key,n):
    pos = (random.randint(0, n-1) , random.randint(0,2))
    return  pos if pos not in key else next_position(key,n)
def hide(listofpixels , listofbytes):
    key=[]
    n = len(listofpixels)
    for k in range(len(listofbytes)):
        i,j = next_position(key , n)
        key.append((i,j))
        listofpixels[i][j]^=listofbytes[k]
    return key
key = hide(listofpixels,listofbytes)
print(listofpixels[:10])


def listoftuple(l):
    op=[]
    for i in l:
        op.append(tuple(i))
    return op
new_image = Image.new(img.mode , img.size)
listofpixels = listoftuple(listofpixels)
new_image.putdata(listofpixels)
new_image.show()
new_image.save("0bs.png")
f = open("key.pickle","wb")
pickle.dump(key,f)
new_image=None
new_image = Image.open("0bs.png")
msg=[]
list_of_pixels_in_new_image = list(new_image.getdata())
for i,j in key:
    msg.append(str(list_of_pixels_in_new_image[i][j]&1))
print(msg)
msg = "".join(msg)
msg = msg[::-1]
ans=[]
print(msg)
for i in range(0,len(msg),8):
    ans.append(int(msg[i:i+8],2))
for i in range(len(ans)):
    ans[i] = chr(ans[i])
msg = "".join(ans)
print(msg[::-1])


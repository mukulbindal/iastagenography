import wave
w = wave.open("okay.wav" , mode="rb")
n = (w.getnframes())
l = w.readframes(n)
# for i in l:
#     print(i)

newwave = wave.open("newwave.wav" , mode='wb')
ba = bytearray()
for i in l:
    ba.append(i)

t = int(input())


def base3contains2(n):
    while n:
        if n % 3 == 2:
            return True
        n //= 3
    return False

def xor(s1,s2):
    s3=""
    for i in range(len(s1)):
        s3 += str((int(s1[i]) + int(s2[i]))%3)
    return s3
def base3(n):
    l = []
    while (n):
        l.append(str(n % 3))
        n //= 3
    return "".join(l)[::-1]


# print("vvv",base3(121))
for _ in range(t):
    n = int(input())
    s = input()
    N = int(s,3)
    for i in range(N//2,N+1):
        if xor(base3(i),base3(N-i)) == s:
            print(base3(i))
            print(base3(N-i))
            break


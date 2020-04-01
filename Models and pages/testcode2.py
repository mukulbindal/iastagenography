d = {}
d[('0', '1')] = '1'
d[('1', '1')] = '2'
d[('1', '0')] = '1'
d[('0', '0')] = '0'
d[('0', '2')] = '2'
d[('2', '0')] = '2'

for _ in range(int(input())):
    n = int(input())
    x = input()
    a = '1'
    b = '1'
    for i in range(1, n):
        if (x[i] == '0'):
            a = a + '0'
            b = b + '0'
        elif (x[i] == '1'):
            a += '0'
            b += '1'
        else:
            a += '1'
            b += '1'

    flag = 2
    pos = -1
    for i in range(n):
        if (a[i] > b[i]):
            pos = i + 1
            flag = 1
            break
        elif (a[i] < b[i]):
            pos = i + 1
            flag = 0
            break

    if (flag != 2):
        if (flag == 1):
            c = ''
            for j in range(pos, n):
                c += d[(b[j], a[j])]
            b = b[:pos] + c
            a = a[:pos] + '0' * (n - pos)

        else:
            c = ''
            for j in range(pos, n):
                c += d[(b[j], a[j])]
            a = a[:pos] + c
            b = b[:pos] + '0' * (n - pos)

    print(a)
    print(b)


'''
5
10
2121212121
10
2222211212
8
20201210
10
2012012012
10
2012012012

1021212121
1100000000
1111101212
1111110000
10100210
10101000
1002012012
1010000000
1002012012


'''
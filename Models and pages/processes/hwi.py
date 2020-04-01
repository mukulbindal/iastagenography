t  = int(input())
for _ in range(t):
    a,b,c,d = map(int , input().split())
    x,y,x1,y1,x2,y2 = map(int , input().split())
    f1 = x-a+b
    f2 = y-c+d
    # if (x-x1<=0 and a>0) or (x2-x<=0 and b>0) or (y-y1<=0 and c>0) or (y2-y<=0 and d>0):
    #     print("No")
    #     continue
    # print(f1,f2)
    if f1>=x1 and f1<=x2 and f2>=y1 and f2<=y2:
        print("Yes")
    else:
        print("No")
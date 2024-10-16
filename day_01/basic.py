import math

r=float(input('圆的半径设置为：'))
area=math.pi*r*r
# 输出
print('面积为%.2f'%(area))
print(area)
print('area=',area)
# 格式化输出
print(f'面积：{area:.2f}')
print(f'{area=:.2f}')

# 求两数的最大公因数
a=int(input('a ='))
b=int(input('b ='))
maxc=int(1)
# 求最大可从大往小遍历
for i in range(a,0,-1):
    if a % i == 0 and b % i == 0:
       maxc = i
       print('最大公因数=',maxc)
       break

# method 2
temp = float(a / b)
if temp < 1:
    a,b = b,a
    while a % b != 0:
        a , b = b , a % b
    print('最大公因数=', b)
else:
    while a % b != 0:
        a , b = b , a % b
    print('最大公因数=', b)

# 判断并输出100以内的质数
for i in range(2,100):
    is_prime = True
    for j in range(2,int( i**0.5 )+1 ):
        if i % j == 0:
            is_prime = False
            break
    if is_prime:
        print('%d '%i)


# 斐波那契数列
a_1 = 1
a_2 = 1
print('%d %d'%(a_1,a_2))
for _ in range(0,21):
    be_calcu = a_1 + a_2
    print(be_calcu)
    a_1 = a_2
    a_2 = be_calcu



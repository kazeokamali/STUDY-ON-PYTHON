# 双色球随机选号
import random

red_balls = [num for num in range(1,34) ]
blue_balls = [num for num in range(1,17)]
selected_red=[]
for _ in range(6):
    index = random.randrange( len(red_balls) )
    selected_red.append(red_balls[index])
selected_blue = blue_balls[ random.randrange(len(blue_balls) ) ]

selected_red.sort()

for i in selected_red:
    print( f'\033[031m{i}\033[0m',end=' ' )
print( f'\033[034m{selected_blue}\033[0m' )


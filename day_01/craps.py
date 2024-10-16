# 花旗骰游戏

import  random
bet_total = 1000
while bet_total> 0:
    print('U HAVE',bet_total)
    bet_set = int(input('赌注为'))
    dice_1 = random.randrange(1, 7)
    dice_2 = random.randrange(1, 7)
    print('骰子总点数为',dice_1+dice_2)
    if dice_1 + dice_2 == 7 or dice_1 + dice_2 == 11:
        bet_total += bet_set
        print('赢！总共',bet_total)
        bet_set =0
    elif dice_1 + dice_2 == 2 or dice_1 + dice_2 == 3 \
        or dice_1 + dice_2 == 12:
        bet_total -= bet_set
        print('输，还剩', bet_total)
        bet_set = 0
    else:
         num = dice_1 + dice_2
         while True:
            dice_1 = random.randrange(1, 7)
            dice_2 = random.randrange(1, 7)
            print('骰子总点数为', dice_1 + dice_2)
            if dice_1 + dice_2 == 7:

                bet_total += bet_set
                print('WIN!GOT', bet_total)
                bet_set = 0
                break
            elif dice_1 + dice_2 == num:
                bet_total -= bet_set
                print('LOSE!GOT', bet_total)
                bet_set = 0
                break
            else:
                continue
print('你没米了')

# 严格地说，应该加一个判断赌注与本金大小关系的过程
'''
 while True:
        debt = int(input('请下注: '))
        if 0 < debt <= money:
            break
'''

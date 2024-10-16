import random


def bubble_sort(nums,comp = lambda x,y:x>y):
    num = nums[:]

    for i in range( len(num) - 1 ):

        for j in range(len(num) - 1 - i):
            if comp( num[j],num[j+1] ):
                num[j],num[j+1] = num[j+1] , num[j]

    return num

aline =[]
for _ in range(15):
    aline.append( random.randrange(10,90) )

bline = bubble_sort(aline)
print(aline)
print(bline)

import math

from numpy.ma.core import angle
from scipy.signal.windows import cosine


class Ball():
    def __init__(self,x):
        self.x = float(x)
        self.y = float(5.0)
        self.r = float(1.0)
        self.center_x_cor = float()

    def make_tangent(self):
        a = (self.x)**2.0 - 1.0
        b = (-10.0)*self.x
        c = (self.y)**2.0 - (self.r)**2.0

        if abs(self.x) != 1.0:
            m1 = ( -b + math.sqrt( b**2.0 - 4.0*a*c ) ) / (2.0*a)
            m2 = ( -b - math.sqrt( b**2.0 - 4.0*a*c ) ) / (2.0*a)
            return [m1,m2]
        else:
            m1 = 0.0
            m2 = ( -c ) / b
            return [m1,m2]

    def cal_angle(self,x_cor,y_cor):
        if x_cor != 0:
            theta_r = float( y_cor/x_cor )
            angle_theta = math.atan(theta_r)
        else:
            angle_theta = math.pi/2.0
        return angle_theta

    def cal_len(self,x_coor,y_coor):
        return math.sqrt( x_coor**2 + y_coor**2 )


    def cal_short_axis(self,cnter_coordinate):
        self.center_x_cor = cnter_coordinate
        theta_ball = self.cal_angle( self.x,self.y )
        theta_center = self.cal_angle( cnter_coordinate, 10.0 )
        theta_BOP = abs( theta_ball - theta_center )

        len_op = self.cal_len(self.x,self.y)
        theta_COP = math.asin( self.r / len_op )
        theta_BOC = math.acos( math.cos(theta_COP) / math.cos( theta_BOP ) )
        len_BC = self.cal_len(cnter_coordinate,10.0) * math.tan(theta_BOC)
        return len_BC * 2




class line_tangent():
    def __init__(self,k):
        self.k = k


    def calcu_elli(self,y_pro = 10.0):
        if self.k != 0:
            x_pro =  y_pro / self.k
        else:
            x_pro = 0.0
        return x_pro

class Information():
    def __init__(self,coordinate,axis,matrix):
        self.coordinate = coordinate[:]
        self.axis = axis[:]
        self.matrix = matrix[:]

class Calc_newpoint():
    def  __init__(self,p0,p1,t):
        self.p0 = p0
        self.p1 = p1
        self.t  = t
        self.p = Information([0, 0], [0, 0], [ [0,0],[0,0] ])

        self.info_list = []
        self.info_list.append(self.p0)
        self.info_list.append(self.p1)

    def calc_new(self):

        for i in range(2):
            self.p.coordinate[i] = self.p0.coordinate[i] + self.t*( self.p1.coordinate[i] - self.p0.coordinate[i] )
            self.p.axis[i] = self.p0.axis[i] + self.t *( self.p1.axis[i] - self.p0.axis[i] )
        self.p.matrix[0][0] = 1.0 /(self.p.axis[0] **2)
        self.p.matrix[1][1] = 1.0 / (self.p.axis[1] ** 2)

        return self.p

def newton_calc(fx,x,new_x):

    leng = len(x)
    a_i = [ [0.0 for _ in range(leng)]  for _ in range(leng)]
    q_x = [ 0.0 for _ in range(leng)  ]

    for i in range( leng ):
        a_i[i][0] = fx[i]

    for i in range(1, leng):
        for j in range( leng - i ):
            a_i[j][i] = ( a_i[j+1][i-1] - a_i[j][i-1] ) / ( x[i+j] - x[j] )

    leng_new = len(new_x)
    new_fx = [0.0 for _ in  range(leng_new)]
    for i in range(leng_new):
        q_x[0] = a_i[0][0]
        for order in range(1,leng):
            term = 1.0
            for j in range(order):
                term *= new_x[i] - x[j]
            q_x[0] +=  a_i[0][order]*term
        new_fx[i] = q_x[0]

    return new_fx





if __name__ == '__main__':

    # 创建list或其他结构存储半径，坐标等信息
    # 创建新方法，计算线段上任一点的坐标，半径，并用度量的矩阵存

    list_points = []
    fx_long = []
    fx_short = []
    x = []
    centre = []
    index = 0

    while True:
#    for _ in  range(2):
        xi = float(input('X坐标：'))
        ball = Ball(xi)
        ms = ball.make_tangent()

        line1 = line_tangent(ms[0])
        line2 = line_tangent(ms[1])
        centre.append((line1.calcu_elli() + line2.calcu_elli())/2.0)

        len_shortaxis = ball.cal_short_axis(centre[index] )

        print(f'两切线斜率{ms}')
        print(f'x1={line1.calcu_elli()} \t x2={line2.calcu_elli()}')
        print(f'long_axis={ abs(line2.calcu_elli() - line1.calcu_elli() ) }')
        print(f'short axis={ len_shortaxis }')
        print(f'center_coordinate:({centre[index] } , 0)\n')
        index += 1

        point_init = Information( [line1.calcu_elli() ,line2.calcu_elli() ] ,
                                  [ abs(line2.calcu_elli() - line1.calcu_elli() )/2.0 ,
                                    len_shortaxis/2 ],
                                   [ [  1.0/((abs(line2.calcu_elli() - line1.calcu_elli() )/2.0)**2) , 0 ],
                                     [ 0.0, 1/( (len_shortaxis/2)**2.0 ) ] ] )
        list_points.append(point_init)

        exit_1 = input('exit?Y / N')
        if exit_1 == 'Y':
            for m in list_points:
                fx_long.append(m.axis[0])
                fx_short.append(m.axis[1])
            for n in centre:
                x.append(n)

            break



    
    while True:
        t_i = float(input('ti=？(0,1)范围'))
        p_i = Calc_newpoint( list_points[0],list_points[1],t_i )
        list_points.append( p_i.calc_new() )

        if t_i == 1.0:
            break

    '''    
    print(list_points)
    for j in list_points:
        print(f'坐标：{ j.coordinate } \t轴长：{j.axis} \t {j.matrix}\n') 
        '''

    print(f'长半轴\n')
    for j in list_points:
        print(f'{j.axis[0]}')

    print(f'短半轴\n')
    for j in list_points:
        print(f'{j.axis[1]}')

    print(f'圆度\n')
    for j in list_points:
        print(f'{j.axis[0] /j.axis[1]}')

    print(f'圆心\n')
    print(centre)





# 迭代法更新插值
    '''
    count_insert = 0
    w = 0.5
    while True:
        
        t_i = float(input('ti=？(0,1)范围'))
        p_i = Calc_newpoint( list_points[0],list_points[1],t_i )
        list_points.append( p_i.calc_new() )
        count_insert += 1

        if t_i == 1.0:
            break
    '''


# 尝试牛顿插值（4个采样点？/3个点？）
# 2.125 4.25 6.375 8.5 10.625 12.75 14.875 17.0 19.125

    input_nums = input('new_points = ?')
    nums = input_nums.split()
    list_of_nums = [ float( i ) for i in nums]

    for i in  newton_calc(fx_long,x,list_of_nums):
        print(i)
#    print( newton_calc(fx_long,x,list_of_nums))
    print('\n')
    print( newton_calc( fx_short , x , list_of_nums ) )











class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add_func(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def devide_func(self,other):
        de_x = int( self.x / other.x )
        de_y = int( self.y / other.y )
        return Point(de_x,de_y)

class OpereteOL:
    def __init__(self,a =0, b= 0):
        self.Xval = a
        self.Yval = b

    def addval(self,other):
        Xval = self.Xval + other.Xval
        Yval = self.Yval + other.Yval
        return OpereteOL( Xval,Yval )



p1 = Point(1, 2)
p2 = Point(2, 3)
p3 = Point.add_func(p1,p2)
p4 = Point.devide_func(p1,p2)
print(p3.x, p3.y)
print(p4.x, p4.y)

s1 = OpereteOL(1,2)
s2 = OpereteOL(3,4)
s3 = OpereteOL.addval(s1,s2)
print(s3.Xval,s3.Yval)

import math
from scipy.optimize import fsolve

class Ball():
    def __init__(self,x):
        self.x = float(x)
        self.y = float(5.0)
        self.r = float(1.0)

    def find_tangent_slope(self):
        # Define the equation to solve
        def equation(m):
            return abs(m * self.x - self.y) / math.sqrt(m**2 + 1) - self.r

        # Use fsolve to find the solution
        m = fsolve(equation, 0)[0]
        return m

if __name__ == '__main__':
    xi = float(0.0)
    while True:
        xi = float(input('X坐标：'))
        ball = Ball(xi)
        m = ball.find_tangent_slope()
        print(f'斜率={m}\n')

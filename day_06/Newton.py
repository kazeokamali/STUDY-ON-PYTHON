import math



delta_t = float(0.1)
delta_Xi = float(1.02 )
delta_a = float( 0.42 )
delta_X_new = 2.125

init = 0.0
summar =0.0

for _ in range(10):
    summar += delta_Xi
    print(f' {summar} ')

summar =0.0

for _ in range(10):
    summar += delta_X_new
    print(f' {summar} ')

summar = 0.0
for _ in range(10):
    summar += delta_a
    print(f' {summar} ')


import math
p0 = 10 * pow(10,-12)
d0 = 1000
x = pow(d0/2.7*1000,3)
p = p0 * x 

print("p =",p)

p_in_dbm = 10 * math.log(p/pow(10,-3))
print("p_in_dbm = ", p_in_dbm)
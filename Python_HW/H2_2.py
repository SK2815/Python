num = int(input("Enter a number "))
list_of_num = []

while(num != 0):
    if(num != 0):
        list_of_num.append(num)
        num = int(input("Enter a number "))
    else:
        break

def gcd(x,y):
    if(x > 0 and y >0):
        if(x>y):
            large = x
            small = y
        else:
            large = y
            small = x
        rem = 1
        while(rem!=0):
            rem = large%small
            if (rem == 0):
                gcd = small
                break
            else:
                large = small
                small = rem
    else:
        return None            
    return gcd           


gcd_of_num = list_of_num[0]
for index in range(len(list_of_num) -1):
    gcd_of_num = gcd(gcd_of_num,list_of_num[index+1])

def lcm(x,y):
    if(x > 0 and y >0):
        mul_of_num = x*y
        LCM = mul_of_num/gcd(x,y)
    else:
        return None

    return LCM    

lcm_of_num = 1
for index in range(len(list_of_num)):
    lcm_of_num = lcm(lcm_of_num,list_of_num[index])

print("The GCD of " + str(list_of_num) + " is " + str(gcd_of_num) + " and the LCM is " + str(lcm_of_num))
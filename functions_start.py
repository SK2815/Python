def myFunction():
    print("heyyaahh I am a function")

myFunction()
#The below statement will call the function and will print the statement as usual.
#BUT NOTE: after calling the myFunction, print will execute itself, because it is also a function.
#So, it will first print the statement normally and then it will print "None", which is python constant
#This happens because myFunction doesnt return anything
#None is a python return constant
print(myFunction()) 
#This will print some bullshit address like 0x0034534, because this is not a function at all. this will print the value of function definition.
#this means, the functions are objects to python code.
print(myFunction)

#this function uses value of x = 1 as its default value.
def power(num,x=1):
    result = 1
    for i in range(x):
        result = result*num
    return result

print(power(2))
print(power(2,3))

#Here is an interesting thing python lets us to do. You can switch the arguments and still get the same result.
#THAT'S SO COOL. For that, we just need to give the name of the argument in any order, and python interpeter will figure out the correct value of the argument on its own.

print(power(x=3,num = 2))
#so, x is written first, which was the second argument. But it didn't matter to python interpreter because we gave the name.

#We can give multiple variables to function as arguments
#This function will loop over each argument and will do something on that
#NOTE: variable argument should always be the last parameter
def multiAdd(*myargs):
    result = 0
    for i in myargs:
        result = result + i
    return result

print(multiAdd(3,4,5,6))
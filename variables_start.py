#decalring the variable
f = 0
print(f)

#redeclaring the variable with different data type, no problem
f = 'abc'
print(f)

#this means, python infers the type by itself. We do not need to assign a type like other programming languages
#BUT NOTE: this also means that we just can not just concatenate two different types.
#Below code will produce error because of concatination of two different types
# But this bitch works with Javascript
#print("this is a string but i am adding 123" + 123)

# Here's how we can make it work
print("this is a string but I am adding 123 by using str function.. " + str(123))

#local and global variables

def localFunction():
    f = 'def'
    print(f)

localFunction()
#Above call will produce def but below print will print abc. 
print(f)

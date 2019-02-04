#self reffers to the object of the class. It is usually the first argument. It is like "this keyword".
class myClass():
    def myMethod(self):
        print("this is myClass method")
    
    def myMethod1(self,someStr):
        print("myClass method1" + someStr)


#inheritance
class childClass(myClass):
    def myMethod(self):
        myClass.myMethod(self)
        print("this is childClass method")
    
    def myMethod1(self,someStr):
        print("childClass method1" + someStr)

def main():
    c = myClass()
    c.myMethod()
    c.myMethod1("  oh hell")

    c1 = childClass()
    c1.myMethod()
    c1.myMethod1(" this is child shit")
if __name__ == "__main__":
    main()
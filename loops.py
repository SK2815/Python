#there are only two types of loop: for and while
def main():
    x = 0

    print("while loop output")
    #while loop
    while(x<5):
        print(x)
        x = x+1

    print("for loop output")
    #for loop
    #here, 5 is inlusive but 10 is excluded
    for x in range(5,10):
        print(x)

    #for loop over a collection
    #this includes everything from starting to end
    days=["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
    for d in days:
        print(d)

    #break and contunue
    for x in range(1,10):
        #if(x== 4): break
        if(x%2 == 0): continue
        print(x)

    #using enumerate() to get the index 
    days=["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
    for x,d in enumerate(days):
        print(x,d)
if __name__ == "__main__":
    main()
#We use elif instead of else if in python
def main():
    x,y = 100,100

    if(x<y):
        st = "x is less than y"
    elif(x>y):
        st = "x is greater than y"
    else:
        st = "x is equal to y"

    print(st)        
    st = "some shit" if (x<y) else "some other shit"

    print(st)

if (__name__ == "__main__"):
    main()
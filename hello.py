#Do remember about the "main" function. If I change the main function name with any other name, then it wll run successfuly but won't produce anything. The other name would work if I import the file. The primary file will always work with "__name__" = "__main__"

def main():
    print("Hello world")

if __name__ == "__main__":
    main()

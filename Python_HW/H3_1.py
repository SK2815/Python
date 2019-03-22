
def sep_words(input_str):  
    list_1 = input_str.split()

    main_list = []
    my_flag = False
    sub_list = []
    delim_list = [".", "?", "!"]
    length = len(list_1) 
    for i in range(length):

        for j in delim_list:
            if j in list_1[i]: 
                curr_list = []
                curr_list = list_1[i].split(j)
                sub_list.append(curr_list[0])
                sub_list.append(j)
                my_flag = False
                break
            else:
                my_flag = True
        if(my_flag == True ):
            sub_list.append(list_1[i])
        else:
            main_list.append(sub_list)
            sub_list = []

        if(i == length-1):
            main_list.append(sub_list)
            break

    return main_list
'''
input_str = input("Enter the string: ")
print("Output: ",sep_words(input_str))
'''
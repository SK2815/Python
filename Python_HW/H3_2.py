
def create_temp_list(input_list):
    temp_list = []
    for i in input_list:
        for j in i:
            temp_list.append(j)

    return temp_list

def comb_words(input_list):
    
    temp_list = create_temp_list(input_list)
    
    final_list = []
    length = len(temp_list)
    j = 0
    for i in range(length):
        if(temp_list[i] == "." or temp_list[i] == "?" or temp_list[i] == "!"):
            final_list[j-1] = [''.join(temp_list[i-1:i+1])]
        else:
            j = j+1
            final_list.append(temp_list[i]) 

    latest_str = ""
    for index in final_list:
        if(type(index) is list):
            temp = ''.join(index)
            latest_str += temp + " "
        else:
            latest_str += index + " "

    return latest_str

'''

input_list = [['Hi,', 'My', 'name', 'is', 'Simran', '.'], ['I', 'am', 'at', 'Starbucks', '?'], ['Dont', 'tell', 'me']]
print("Input list is: ",input_list)
print("Output: ",comb_words(input_list))

'''
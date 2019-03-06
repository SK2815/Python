
Person_name = 'Dummy'
My_Dict = dict()

while(Person_name != ''):
    Person_name = input("Please Enter Person's Name: ")
    if(Person_name == ''):
        break
    print(Person_name)
    my_list = []

    Cruise_name = 'Dummy'
    while(Cruise_name != ''):
        Cruise_name = input('Enter Cruise Name: ')
        if(Cruise_name != ''):
            Cruise_length = input('Enter Cruise Length: ')
            tuple_list = list()
            tuple_list.append(Cruise_name)
            tuple_list.append(int(Cruise_length))
            tuple_elm = tuple(tuple_list)
            my_list.append(tuple_elm)
            My_Dict[Person_name] = my_list   
          
print(My_Dict)


for index in My_Dict:
    print("Cruise list for ",index)
    list_count = len(My_Dict[index])
    if(list_count >0):
        local_list = My_Dict[index]
        local_list_len = len(local_list)
        for i in range(local_list_len):
            total_num_of_days = 0
            print(local_list[i][0] + ":" + str(local_list[i][1]))
            print(local_list[i][1])
            total_num_of_days = total_num_of_days + local_list[i][1]
            
        print("Total number of days",total_num_of_days)
        if(local_list_len >= 1 and local_list_len <=3 ):
            print("Gold Loyalty Member")
        elif(local_list_len >= 4 and local_list_len <=5 and total_num_of_days >=31 and total_num_of_days <=50):
            print("Ruby Loyalty Member")
        elif(local_list_len >= 6 and local_list_len <= 15 and total_num_of_days >=50 and total_num_of_days <=150):
            print("Platinum Loyalty Member")
        elif(local_list_len >= 16 and total_num_of_days >=151):
            print("Elite Loyalty Member")


    

    


User_Dict = { ('Adam', 1234): ['A-','B','B-'],
              ('Babs', 1101): ['A','B+','A'],
              ('Cam', 9876): ['C','C+','B-'],
              ('Dee', 3040): ['A','B+','C-'],
              ('Eieio', 1234): ['A-','A','A-']}


Grade_Dict = {'A' :4,
              'A-':3.7,
              'B+':3.3,
              'B' :3,
              'B-':2.7,
              'C+':2.3,
              'C' :2,
              'C-':1.7}

print(User_Dict[('Cam', 9876)])
print(User_Dict[('Dee', 1234)]) #this will produce an error

Babs_list = User_Dict[('Babs', 1101)]
GPA_1 = (Grade_Dict[Babs_list[0]] + Grade_Dict[Babs_list[1]] + Grade_Dict[Babs_list[2]])/3
print(GPA_1)

Babs_list.remove('A')
Babs_list.append('B+')
GPA_2 = (Grade_Dict[Babs_list[0]] + Grade_Dict[Babs_list[1]] + Grade_Dict[Babs_list[2]])/3
print(Babs_list)
print(GPA_2)

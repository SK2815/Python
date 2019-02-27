cell1 = ('PayAsUGo',(1000,100,0),19.95,['XN1'])
cell2 = ('Economy',('unlimited','unlimited',1),27.95,['XN10','YU5'])
cell3 = ('Freedom',('unlimited','unlimited',10),59.95,['YU6','M1+'])

mylist = [cell1,cell2,cell3]
#print("Length of the list = ",len(mylist))
#print("Second element of the list =",mylist[1])
#print("Plan name of third item", mylist[2][0])
#print("Plan name of first item", mylist[0][1])
#print("Price of first item", mylist[0][2])
#print("Number of phones in second element", len(mylist[1][3]))

#operation
cell4 = ('Business',('unlimited',0,5), 40.00,['XN20','XZ5','YU5+'])
mylist.append(cell4)
#print("List appended with business plan ",mylist)

cell4[3].append('M2')
#print("List appended with business plan ",mylist[3])

print("List appended with business plan ",cell2[3][0])
#cell2[3].remove('XN10')
#cell2[3].remove
del cell2[3][0]
#print(cell2)

del mylist[0]
print("list  = ",mylist)

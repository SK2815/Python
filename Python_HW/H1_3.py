first_name = "simran"
sec_name = "kaur"

name_str = first_name + sec_name
print(name_str)
#[-5:] will give only last characters of the string
#[:-5] will give first 5 letters of the string
#[0:5] = [:5]
mashed_name = name_str[-5:] + name_str[:4]
print(mashed_name)

#reverse a string
rev_str = mashed_name[::-1]
print(rev_str)

name_list = list(name_str)
print("My name list = ",name_list)

#sorted keyword is used to sort the string elements of a list
sort_list = sorted(name_list)
print("Sorted list = ",sort_list)

name_string2 = ''.join(sort_list)
print(name_string2)
#name_list.remove('e')
#print(name_list)
x = name_list.count('a')
print("Count of a =",x)

 
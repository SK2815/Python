import H3_4 as wm
import random
import string

file_read = open("para_input.txt")
input_str = file_read.read()

line_list = []
line_list = input_str.split('.')

main_list = []
temp_str = ''
count = 0
#print(len(input_str))
for i in range(len(input_str)):
    temp_str += input_str[i]
    if((len(temp_str) <= 60 or len(temp_str) == 60) and (input_str[i] == '.' or input_str[i] == '?')):
        temp_str = input_str[count:i+1]
        main_list.append(temp_str)
        temp_str = ''
        count = i + 1

    elif((len(temp_str) > 60) and (input_str[i] != '.' or input_str[i] != '?')):
        temp_str = input_str[count:i+1]
        main_list.append(temp_str)
        temp_str = ''
        count = i+1
        continue
       
print(main_list)

words = main_list
print('Original words  =', words)
n = random.randint(0,2000000001)

enc_words = wm.crypt(words, n, True)
print('Encrypted output=', enc_words)
dec_words = wm.crypt(enc_words, n, False)
print('Decrypted output=', dec_words)
if words == dec_words:
    print('Decrypted words matched original words')
else:
    print('Decrypted words did not match original words')
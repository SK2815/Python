from H3_1 import sep_words
from H3_2 import comb_words
from H3_3 import crypt
import random
import string

#separate words
'''
input_str = input("Enter the string: ")
print("Output: ", sep_words(input_str))
'''
#combine words
'''
input_list = [['Hi,', 'My', 'name', 'is', 'Simran', '.'], ['I', 'am', 'at', 'Starbucks', '?'], ['Dont', 'tell', 'me']]
print("Input list is: ", input_list)
print("Output: ", comb_words(input_list))
'''
#crypto
'''
num_words=random.randint(1,7) 
words = []
chars = "'" + "," + "!" + "?" + ";" + ":" + string.ascii_lowercase + string.ascii_uppercase
print(chars)
for i in range(num_words):
    word_length=random.randint(1,20) 
    words.append(''.join(random.choices(chars, k=word_length)))

print('Original words  =', words)
n = random.randint(0,2000000001)

enc_words = crypt(words, n, True)
print('Encrypted output=', enc_words)
dec_words = crypt(enc_words, n, False)
print('Decrypted output=', dec_words)
if words == dec_words:
    print('Decrypted words matched original words')
else:
    print('Decrypted words did not match original words')

'''
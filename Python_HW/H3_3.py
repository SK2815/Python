
import random
import string

# Create list of sorted lowercase chars
alpha_lc_list = list(string.ascii_lowercase)
# Create list of sorted uppercase chars
alpha_uc_list = list(string.ascii_uppercase)

#encrypt word using a random char list
def encrypt_word(orig_word, random_char_list):
    encrypted_word = ''
    # for each char in word
    for c in orig_word:
        #Find index of Upper/lower case character.
        #Append the character in the random list at that index
        #If not an alpha char append as is
        if c.isupper():
            encrypted_word += random_char_list[alpha_uc_list.index(c)].upper()
        elif c.islower():
            encrypted_word += random_char_list[alpha_lc_list.index(c)]
        else:
            encrypted_word += c
    return encrypted_word

def decrypt_word(orig_word, random_char_list):
    decrypted_word = ''
    for c in orig_word:
        #Convert char to lower. Find it's index in random char list
        #Append the character in the upper/lower case sorted char list at that index
        #If not an alpha char append as is
        if c.isupper():
            decrypted_word += alpha_uc_list[random_char_list.index(c.lower())]
        elif c.islower():
            decrypted_word += alpha_lc_list[random_char_list.index(c.lower())]
        else:
            decrypted_word += c
    return decrypted_word


#seed the random module with given number and shuffle the alpha list
def generate_random_char_list(n):
    alpha_list = list(string.ascii_lowercase)
    random.seed(n)
    random.shuffle(alpha_list)
    return alpha_list

def crypt(x, n, enc):
    random_char_list = generate_random_char_list(n)
    ret_list = []
    for word in x:
        if enc == True:
            ret_list.append(encrypt_word(word, random_char_list))
        else:
            ret_list.append(decrypt_word(word, random_char_list))
    return ret_list

num_words=random.randint(1,7) 
words=[]
chars="'" + string.ascii_lowercase + string.ascii_uppercase
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


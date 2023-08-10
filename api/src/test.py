
from bcrypt import hashpw, gensalt, checkpw
  
# example password
password = 'passwordabc'
  
# converting password to array of bytes
bytes = password.encode('utf-8')
  
# generating the salt
salt = gensalt()
  
# Hashing the password
hash = hashpw(bytes, salt)
  
# Taking user entered password 
userPassword =  'passwordabc'
  
# encoding user password
userBytes = userPassword.encode('utf-8')
  
# checking password
result = checkpw(userBytes, hash)
  
print(result)
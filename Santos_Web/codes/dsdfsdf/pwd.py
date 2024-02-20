from random import *

import os

u_pwd = input("Enter a password: ")

pwd = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z',
'1','2','3','4','5','6']

pw = ""
int = (0)
while(pw!=u_pwd):
    pw=""
    for letter in range(len(u_pwd)):
        guess_pwd = pwd[randint(0,17)]
        pw=str(guess_pwd)+str(pw)
        print(pw)
        print("...............")
        int += 1
        print(int)
print("Your Password Is :",pw)
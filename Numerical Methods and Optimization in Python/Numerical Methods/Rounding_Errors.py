# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 13:45:36 2023

@author: SHIBAYAN BISWAS
"""

num = 10
s = 0
for _ in range(100):
    s += 0.1
   
print(s == num)
# IT IS NOT A GOOD APPROACG AT ALL !!

epsilon = 0.0001
if abs(s - num) < epsilon:
    print('The numbers are equal...')
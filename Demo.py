# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:24:15 2026

@author: prana.narayanan
"""

import LessScary
LessScary.activate()

####### Uncomemnt each block below and test Less Scary  #########

# ------------------------
# NameError
# ------------------------
# x = y + 1
    
# ------------------------
# TypeError: mixing values
# ------------------------
# x = 5 + "hello"
 

# ------------------------
# TypeError: len on number
# ------------------------
#len(10)

# ------------------------
# TypeError: calling non-function
# ------------------------
# x = 5
# x()

# ------------------------
# TypeError: indexing non-subscriptable
# ------------------------

# x = 10
# x[0]

# ------------------------
# TypeError: non-iterable in loop
# ------------------------
# for i in range(10):
#     print(i)

# ------------------------
# TypeError: missing function argument
# ------------------------
# def add(a, b):
#     return a + b

# add(5)

# ------------------------
# TypeError: too many arguments
# ------------------------
# len("hello", "world")

# ------------------------
# TypeError: wrong input type for method
# ------------------------
# "hello".split(5)

# ------------------------
# IndexError
# ------------------------
#my_list = [1, 2, 3]
#print(my_list[5])

# ------------------------
# KeyError
# ------------------------
# my_dict = {"name": "John"}
# print(my_dict["age"])

# ------------------------
# ZeroDivisionError
# ------------------------
# x = 10 / 0

# ------------------------
# AttributeError
# ------------------------
# my_list = [1, 2, 3]
# my_list.upper()

# ------------------------
# ValueError: int conversion
# ------------------------
# int("hello")

# ------------------------
# ValueError: float conversion
# ------------------------
# float("abc")

# ------------------------
# ModuleNotFoundError
# ------------------------
# import not_a_real_module


# ------------------------
# FileNotFoundError
# ------------------------
# open("this_file_does_not_exist.txt")

# ------------------------
# SyntaxError: missing colon
# Uncomment this and run carefully
# ------------------------
# if True
#     print("hello")

# ------------------------
# SyntaxError: unfinished string
# ------------------------
# print("hello)

# ------------------------
# IndentationError: expected indented block
# ------------------------
# def my_func():
# print("hello")

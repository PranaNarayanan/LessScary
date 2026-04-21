# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:10:34 2026

@author: prana.narayanan
"""

import traceback
import re
import sys


def _print_friendly_error(etype, evalue, tb):
    extracted = traceback.extract_tb(tb)

    if extracted:
        last = extracted[-1]
        code_line = last.line if last.line else ""
    else:
        code_line = ""

    print("\n==============================")
    print("🟢 LessScary Error Explanation")
    print("==============================\n")

    if issubclass(etype, IndentationError):
        _handle_indentation_error(evalue)

    elif issubclass(etype, SyntaxError):
        _handle_syntax_error(evalue)

    else:
        print(f"👉 Problematic line: {code_line}")
        print()

        if issubclass(etype, NameError):
            _handle_name_error(evalue)

        elif issubclass(etype, TypeError):
            _handle_type_error(evalue)

        elif issubclass(etype, IndexError):
            print("❌ You are asking for an item that is outside the list.")
            print("💡 Check how many items are in the list and which position you are trying to use.")

        elif issubclass(etype, KeyError):
            _handle_key_error(evalue)

        elif issubclass(etype, ZeroDivisionError):
            print("❌ You are trying to divide by zero, which is not allowed.")
            print("💡 Make sure the number after / is not zero.")

        elif issubclass(etype, AttributeError):
            _handle_attribute_error(evalue)

        elif issubclass(etype, ValueError):
            _handle_value_error(evalue)

        elif issubclass(etype, ModuleNotFoundError):
            _handle_module_not_found_error(evalue)

        elif issubclass(etype, FileNotFoundError):
            _handle_file_not_found_error(evalue)

        else:
            print(f"❌ Error type: {etype.__name__}")
            print(f"💡 Message: {evalue}")


def _handle_name_error(evalue):
    msg = str(evalue)
    match = re.search(r"name '(.+)' is not defined", msg)

    if match:
        var_name = match.group(1)
        print(f"❌ You are using the variable '{var_name}', but it has not been created yet.")
        print("💡 Check for a typo or define it before using it.")
    else:
        print("❌ You are using a variable that has not been created yet.")
        print("💡 Check for a typo or define it before using it.")


def _handle_type_error(evalue):
    msg = str(evalue)

    if "unsupported operand type" in msg:
        match = re.search(r"unsupported operand type\(s\) for .+: '(.+)' and '(.+)'", msg)
        if match:
            left_type = match.group(1)
            right_type = match.group(2)
            print(f"❌ You are trying to combine two values that do not work together: {left_type} and {right_type}.")
            print("💡 This often happens when you mix a number and text, like 5 + 'hello'.")
        else:
            print("❌ You are trying to combine values that don’t go together.")
            print("💡 For example, you might be mixing a number and text.")

    elif "has no len()" in msg:
        match = re.search(r"object of type '(.+)' has no len\(\)", msg)
        if match:
            bad_type = match.group(1)
            print(f"❌ You are using len() on a {bad_type}, but that kind of value does not have a length.")
            print("💡 len() works for things like text, lists, and tuples.")
        else:
            print("❌ You are using len() on something that does not have a length.")
            print("💡 len() works for things like text and lists, but not for numbers.")

    elif "object is not callable" in msg:
        match = re.search(r"'(.+)' object is not callable", msg)
        if match:
            bad_type = match.group(1)
            print(f"❌ You are trying to use a {bad_type} like a function.")
            print("💡 This often happens when you put () after a value that is not a function.")
        else:
            print("❌ You are trying to use something like a function, but it is not a function.")
            print("💡 Check whether you accidentally added ().")

    elif "object is not subscriptable" in msg:
        match = re.search(r"'(.+)' object is not subscriptable", msg)
        if match:
            bad_type = match.group(1)
            print(f"❌ You are trying to access part of a {bad_type} using square brackets [ ], but that is not allowed.")
            print("💡 Square brackets usually work with things like lists, strings, and dictionaries.")
        else:
            print("❌ You are trying to use square brackets [ ] on something that cannot be indexed.")
            print("💡 Square brackets usually work with things like lists, strings, and dictionaries.")

    elif "object is not iterable" in msg:
        match = re.search(r"'(.+)' object is not iterable", msg)
        if match:
            bad_type = match.group(1)
            print(f"❌ You are trying to loop over a {bad_type}, but that is not a collection of items.")
            print("💡 for-loops work with things like lists, strings, tuples, and ranges.")
        else:
            print("❌ You are trying to loop over something that is not a collection of items.")
            print("💡 for-loops work with things like lists, strings, tuples, and ranges.")

    elif "missing" in msg and "required positional argument" in msg:
        match = re.search(r"missing (\d+) required positional argument", msg)
        if match:
            num_missing = match.group(1)
            print("❌ You called a function without giving it all the inputs it needs.")
            print(f"💡 This function is missing {num_missing} required input(s). Add the missing value(s) inside the parentheses.")
        else:
            print("❌ You called a function without giving it all the inputs it needs.")
            print("💡 Add the missing value(s) inside the parentheses.")

    elif "positional argument" in msg and "were given" in msg:
        print("❌ You gave too many inputs to a function.")
        print("💡 Check how many values the function is supposed to receive.")

    elif "must be str" in msg or "must be" in msg:
        print("❌ A function expected one kind of value, but received a different kind.")
        print("💡 For example, it may have expected text but got a number instead.")

    else:
        print("❌ You are using a value in a way Python does not understand.")
        print("💡 Check whether you are combining values correctly or calling a function the right way.")


def _handle_key_error(evalue):
    missing_key = str(evalue)
    print(f"❌ You are trying to use the key {missing_key}, but it is not in the dictionary.")
    print("💡 Check whether the key exists and is spelled correctly.")


def _handle_attribute_error(evalue):
    msg = str(evalue)
    match = re.search(r"'(.+)' object has no attribute '(.+)'", msg)

    if match:
        obj_type = match.group(1)
        attribute = match.group(2)
        print(f"❌ You are trying to use '{attribute}' on a {obj_type}, but that does not exist there.")
        print("💡 Some methods only work for certain kinds of values.")
    else:
        print("❌ You are trying to use something that this value does not have.")
        print("💡 Some methods work for text but not for lists or numbers.")


def _handle_value_error(evalue):
    msg = str(evalue)

    if "invalid literal for int()" in msg:
        print("❌ You are trying to turn text into a whole number, but the text is not a valid number.")
        print("💡 For example, int('hello') does not work, but int('5') does.")

    elif "could not convert string to float" in msg:
        print("❌ You are trying to turn text into a decimal number, but the text is not a valid number.")
        print("💡 For example, float('abc') does not work, but float('3.14') does.")

    else:
        print("❌ The value you gave is the wrong value for this operation.")
        print("💡 Check whether the value makes sense for what you are trying to do.")


def _handle_syntax_error(evalue):
    msg = str(evalue)

    bad_line = getattr(evalue, "text", None)
    if bad_line:
        print(f"👉 Problematic line: {bad_line.strip()}")
        print()

    print("❌ Python could not understand this line of code.")

    if "expected ':'" in msg:
        print("💡 It looks like you forgot a colon ':' (for example after if, for, or def).")

    elif "invalid syntax" in msg:
        print("💡 There is something written incorrectly in this line.")
        print("💡 Check for a missing bracket, quote, colon, or operator.")

    elif "unexpected EOF" in msg:
        print("💡 You may have an unfinished line.")
        print("💡 Check for a missing bracket, parenthesis, or quote.")

    else:
        print(f"💡 {msg}")


def _handle_indentation_error(evalue):
    msg = str(evalue)

    bad_line = getattr(evalue, "text", None)
    if bad_line:
        print(f"👉 Problematic line: {bad_line.strip()}")
        print()

    print("❌ There is a problem with indentation (spacing at the start of the line).")

    if "unindent does not match" in msg:
        print("💡 The indentation of this line does not match earlier lines.")
        print("💡 Make sure all lines in the same block are aligned.")
        print("💡 Also avoid mixing tabs and spaces.")

    elif "unexpected indent" in msg:
        print("💡 This line is indented more than expected.")
        print("💡 Check if you added extra spaces by mistake.")

    elif "expected an indented block" in msg:
        print("💡 Python expected an indented block here.")
        print("💡 After statements like if, for, or def, the next line must be indented.")

    else:
        print("💡 Check that your indentation is consistent.")
        print("💡 Avoid mixing tabs and spaces.")


def _handle_module_not_found_error(evalue):
    msg = str(evalue)
    match = re.search(r"No module named '(.+)'", msg)

    if match:
        module_name = match.group(1)
        print(f"❌ Python cannot find the module '{module_name}'.")
        print("💡 Check whether the module name is spelled correctly.")
        print("💡 If needed, install it first.")
    else:
        print("❌ Python cannot find the module you are trying to import.")
        print("💡 Check the spelling or install the module first.")


def _handle_file_not_found_error(evalue):
    print("❌ Python cannot find the file you are trying to open.")
    print("💡 Check whether the file name is correct and whether the file is in the right folder.")


def _ipython_handler(shell, etype, evalue, tb, tb_offset=None):
    _print_friendly_error(etype, evalue, tb)


def _python_handler(etype, evalue, tb):
    _print_friendly_error(etype, evalue, tb)


def activate():
    sys.excepthook = _python_handler

    try:
        ip = get_ipython()
    except NameError:
        ip = None

    if ip is not None:
        ip.set_custom_exc((Exception,), _ipython_handler)
        print("LessScary is active. Best results in Spyder when using Run Selection.")
    else:
        print("LessScary is active.")
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

    print("\n[LessScary]")
    print(f"👉 Problematic line: {code_line}")
    print()

    if issubclass(etype, NameError):
        msg = str(evalue)
        match = re.search(r"name '(.+)' is not defined", msg)

        if match:
            var_name = match.group(1)
            print(f"❌ You are using the variable '{var_name}', but it has not been created yet.")
            print("💡 Check for a typo or define it before using it.")
        else:
            print("❌ You are using a variable that has not been created yet.")
            print("💡 Check for a typo or define it before using it.")

    elif issubclass(etype, TypeError):
        print("❌ Python expected one kind of value, but got another.")
        print("💡 For example, you might be combining a number and text.")

    elif issubclass(etype, IndexError):
        print("❌ You are trying to access a position that does not exist in a list.")
        print("💡 Check the length of your list and the index you are using.")

    elif issubclass(etype, KeyError):
        print("❌ You are trying to access a key that does not exist in a dictionary.")
        print("💡 Check whether the key exists and is spelled correctly.")

    elif issubclass(etype, ZeroDivisionError):
        print("❌ You are trying to divide by zero, which is not allowed.")
        print("💡 Make sure the denominator is not zero.")

    elif issubclass(etype, AttributeError):
        print("❌ You are trying to use something that this value does not have.")
        print("💡 For example, you may be using a string method on a list or a list method on a number.")

    else:
        print(f"❌ Error type: {etype.__name__}")
        print(f"💡 Message: {evalue}")


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
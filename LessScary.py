import traceback
import re
import sys


COMMON_DUNDER_MISTAKES = {
    "_init_": "__init__",
    "_str_": "__str__",
    "_repr_": "__repr__",
    "_len_": "__len__"
}


def _find_dunder_typo(tb):
    extracted = traceback.extract_tb(tb)

    for frame in reversed(extracted):
        code_line = frame.line or ""
        for wrong, correct in COMMON_DUNDER_MISTAKES.items():
            if wrong in code_line:
                return wrong, correct

    return None, None


def _print_friendly_error(etype, evalue, tb):
    extracted = traceback.extract_tb(tb)

    if extracted:
        last = extracted[-1]
        code_line = last.line if last.line else ""
    else:
        code_line = ""

    print("\n==============================")
    print("🟢 LessScary Explanation")
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
            _handle_type_error(evalue, tb)

        elif issubclass(etype, IndexError):
            print("❌ You are asking for an item that is outside the list.")
            print("💡 Fix: make sure the index is smaller than the list length.")

        elif issubclass(etype, KeyError):
            _handle_key_error(evalue)

        elif issubclass(etype, ZeroDivisionError):
            print("❌ You are trying to divide by zero.")
            print("💡 Fix: make sure the number after / is not zero.")

        elif issubclass(etype, AttributeError):
            _handle_attribute_error(evalue, tb)

        elif issubclass(etype, ValueError):
            _handle_value_error(evalue, tb)

        elif issubclass(etype, ModuleNotFoundError):
            print("❌ Python cannot find this module.")
            print("💡 Fix: check the spelling of the module name or install it first.")

        elif issubclass(etype, FileNotFoundError):
            print("❌ Python cannot find the file.")
            print("💡 Fix: check the file name and make sure the file is in the correct folder.")

        else:
            print(f"❌ Error type: {etype.__name__}")
            print("💡 Fix: check the message above and revise this line.")


# ------------------------
# NameError
# ------------------------
def _handle_name_error(evalue):
    msg = str(evalue)
    match = re.search(r"name '(.+)' is not defined", msg)

    if match:
        var_name = match.group(1)
        print(f"❌ You are using the variable '{var_name}', but it has not been created yet.")
        print(f"💡 Fix: define '{var_name}' before using it.")
    else:
        print("❌ You are using a variable that has not been created yet.")
        print("💡 Fix: define the variable before using it.")


# ------------------------
# TypeError
# ------------------------
def _handle_type_error(evalue, tb=None):
    msg = str(evalue)

    type_map = {
        "str": "text",
        "int": "a whole number",
        "float": "a decimal number",
        "list": "a list",
        "tuple": "a tuple",
        "dict": "a dictionary"
    }

    if "not supported between instances" in msg:
        match = re.search(r"'(.+)' not supported between instances of '(.+)' and '(.+)'", msg)
        if match:
            left = match.group(2)
            right = match.group(3)

            left_readable = type_map.get(left, left)
            right_readable = type_map.get(right, right)

            print(f"❌ You are trying to compare {left_readable} and {right_readable}.")
            print("💡 Fix: make sure both values are the same type before comparing.")
        else:
            print("❌ You are comparing values that Python cannot compare.")
            print("💡 Fix: make sure both values are of the same type.")

    elif "unsupported operand type" in msg:
        match = re.search(r"unsupported operand type\(s\) for .+: '(.+)' and '(.+)'", msg)

        if match:
            left = match.group(1)
            right = match.group(2)

            left_readable = type_map.get(left, left)
            right_readable = type_map.get(right, right)

            print(f"❌ You are trying to combine {left_readable} and {right_readable}.")
            print("💡 Fix: convert them to the same type before combining them.")
        else:
            print("❌ You are trying to combine values that do not work together.")
            print("💡 Fix: use values of compatible types, such as two numbers or two pieces of text.")

    elif "has no len()" in msg:
        print("❌ You are using len() on something that does not have a length.")
        print("💡 Fix: use len() only with text, lists, tuples, or similar objects.")
    
    elif "takes exactly one argument" in msg:
        print("❌ This function takes only one input.")
        print("💡 Fix: remove the extra values inside the parentheses.")
    elif "takes no arguments" in msg:
        print("❌ This class does not accept any inputs, but you provided one.")

        found_typo = False

        try:
            from IPython import get_ipython
            ip = get_ipython()
            namespace = ip.user_ns if ip is not None else globals()
        except:
            namespace = globals()

        for obj in namespace.values():
            if isinstance(obj, type):
                if hasattr(obj, "_init_"):
                    found_typo = True
                    break

        if found_typo:
            print("💡 Fix: rename _init_ to __init__ in your class.")
        else:
            print("💡 Fix: check whether your __init__ method is written correctly.")
    elif "must be str" in msg:
        print("❌ This function expected text, but you gave a different type.")
        print("💡 Fix: use a string value, for example \" \", \",\" or another piece of text.")

    # Optional: detect split specifically
        extracted = traceback.extract_tb(tb) if tb else []
        code_line = extracted[-1].line.strip() if extracted and extracted[-1].line else ""

        if ".split(" in code_line:
            print('💡 Example: "hello world".split(" ")')
    elif "object is not callable" in msg:
        if "list" in msg:
            print("❌ You are trying to use a list like a function.")
            print("💡 Fix: use square brackets to access items, e.g., my_list[2].")
        else:
            print("❌ You are trying to use something like a function, but it is not one.")
            print("💡 Fix: remove () or check if it should be a function.")

    elif "object is not subscriptable" in msg:
        print("❌ You are trying to use square brackets [ ] on something that cannot be indexed.")
        print("💡 Fix: use [ ] only with lists, strings, tuples, or dictionaries.")

    elif "object is not iterable" in msg:
        print("❌ You are trying to loop over something that is not a collection.")
        print("💡 Fix: use a list, string, tuple, or range in the loop.")

    elif "missing" in msg and "required positional argument" in msg:
        match = re.search(r"missing \d+ required positional argument[s]?: '(.+)'", msg)

        if match:
            arg = match.group(1)
            print(f"❌ You did not provide the required value '{arg}'.")
            print(f"💡 Fix: include '{arg}' when calling the function or class.")
        else:
            print("❌ You called something without all required inputs.")
            print("💡 Fix: add the missing values inside the parentheses.")

    elif "positional argument" in msg and "were given" in msg:
        print("❌ You gave too many inputs to a function.")

        found_missing_self = False

        try:
            from IPython import get_ipython
            ip = get_ipython()
            namespace = ip.user_ns if ip is not None else globals()
        except:
            namespace = globals()

        for obj in namespace.values():
            if isinstance(obj, type):
                init = getattr(obj, "__init__", None)
                if init and hasattr(init, "__code__"):
                    params = init.__code__.co_varnames
                    if len(params) > 0 and params[0] != "self":
                        found_missing_self = True
                        break

        if found_missing_self:
            print("💡 Fix: add 'self' as the first parameter in __init__.")
            print("💡 Example: def __init__(self, name):")
        else:
            print("💡 Fix: remove the extra arguments.")

    elif "list indices must be integers" in msg:
        print("❌ List index positions must be whole numbers (0, 1, 2, ...).")
        print("💡 Fix: use an integer instead of a decimal or text.")

    else:
        print("❌ You are using a value in a way Python does not understand.")
        print("💡 Fix: check how values are being used in this line.")


# ------------------------
# KeyError
# ------------------------
def _handle_key_error(evalue):
    print(f"❌ The key {evalue} does not exist in the dictionary.")
    print("💡 Fix: use a key that already exists in the dictionary.")


# ------------------------
# AttributeError
# ------------------------
def _handle_attribute_error(evalue, tb=None):
    msg = str(evalue)

    extracted = traceback.extract_tb(tb) if tb else []
    code_line = extracted[-1].line.strip() if extracted and extracted[-1].line else ""
    
    if "has no attribute" in msg:
        match = re.search(r"'(.+)' object has no attribute '(.+)'", msg)
        if match:
            obj_type = match.group(1)
            attr = match.group(2)

            if attr in ["upper", "lower", "strip", "split"]:
                print(f"❌ You are trying to use a text method '{attr}()' on a {obj_type}.")
                print(f"💡 Fix: use '{attr}()' only on text, e.g., \"hello\".{attr}()")
                return
    
    if "has no attribute" in msg and "self." in code_line and "=" in code_line:
        left, right = [part.strip() for part in code_line.split("=", 1)]

        if right.startswith("self.") and not left.startswith("self."):
            attr_name = right.replace("self.", "", 1)
            print(f"❌ 'self.{attr_name}' does not exist yet.")
            print(f"💡 Fix: write self.{left} = {left} instead.")
            return

    wrong, correct = _find_dunder_typo(tb) if tb else (None, None)

    if wrong:
        print("❌ Special method is written incorrectly.")
        print(f"💡 Fix: rename {wrong} to {correct}.")
        return

    print("❌ You are trying to use something that this value does not have.")
    print("💡 Fix: use a method or attribute that belongs to this type of value.")


# ------------------------
# ValueError
# ------------------------
def _handle_value_error(evalue, tb=None):
    msg = str(evalue)

    extracted = traceback.extract_tb(tb) if tb else []
    code_line = extracted[-1].line.strip() if extracted and extracted[-1].line else ""

    if "too many values to unpack" in msg and "self," in code_line:
        print("❌ You used a comma instead of a dot in self.name.")
        print("💡 Fix: write self.name = name")
        return

    if "invalid literal for int()" in msg:
        print("❌ You are trying to convert text into a number, but it is not valid.")
        print("💡 Fix: use text that looks like a whole number, such as '5'.")
    elif "could not convert string to float" in msg:
        print("❌ You are trying to convert text into a decimal number, but it is not valid.")
        print("💡 Fix: use text that looks like a number, such as '3.14'.")
    else:
        print("❌ The value is not suitable for this operation.")
        print("💡 Fix: use a value that makes sense for this operation.")


# ------------------------
# SyntaxError
# ------------------------
def _handle_syntax_error(evalue):
    msg = str(evalue)

    bad_line = getattr(evalue, "text", None)
    stripped_line = bad_line.strip() if bad_line else ""

    if bad_line:
        print(f"👉 Problematic line: {stripped_line}")
        print()

    if "expected ':'" in msg:
        print("❌ This line is missing a colon ':' at the end.")
        if stripped_line:
            print(f"💡 Fix: {stripped_line}:")

    elif "incomplete input" in msg:
    # 🔥 Detect unexpected indentation using offset
        offset = getattr(evalue, "offset", None)

        if offset is not None and offset > 1:
            print("❌ This line is indented but should not be.")
            print("💡 Fix: remove the spaces at the beginning of the line.")
        else:
            print("❌ This line starts a block but is not finished.")
            print("💡 Fix: add an indented line below it.")

            if stripped_line.startswith("for"):
                print("💡 Example:")
                print("    print(i)")
            elif stripped_line.startswith("if"):
                print("💡 Example:")
                print("    print('condition met')")

    elif "invalid syntax" in msg:
        print("❌ There is something written incorrectly in this line.")
        print("💡 Fix: check for missing brackets, quotes, commas, colons, or operators.")
    elif "unterminated string literal" in msg:
        print("❌ You started a string but did not close it.")
        print("💡 Fix: add a closing quote at the end.")

        if bad_line:
            line = bad_line.strip()

        # Try to auto-fix visually
            if line.count('"') == 1:
                print(f'💡 Example: {line}"')
            elif line.count("'") == 1:
                print(f"💡 Example: {line}'")
    else:
        print("❌ Python could not understand this line.")
        print(f"💡 Fix: {msg}")


# ------------------------
# IndentationError
# ------------------------
def _handle_indentation_error(evalue):
    msg = str(evalue)

    bad_line = getattr(evalue, "text", None)
    stripped_line = bad_line.strip() if bad_line else ""

    if bad_line:
        print(f"👉 Problematic line: {stripped_line}")
        print()

    if "unindent does not match" in msg:
        print("❌ This line is not aligned with the other lines in the block.")
        print("💡 Fix: use the same indentation as the surrounding lines.")
        print()
        print("💡 Example:")
        print("    print(\"hello\")")
        print("    print(\"world\")")

    elif "unexpected indent" in msg:
        print("❌ This line has too many spaces at the beginning.")
        print("💡 Fix: remove extra spaces at the start of the line.")

    elif "expected an indented block" in msg:
        print("❌ Python expected an indented line here.")
        print("💡 Fix: add spaces before this line.")

    else:
        print("❌ There is a problem with indentation.")
        print("💡 Fix: make sure all lines in a block use the same indentation.")


# ------------------------
# Optional helper for dunder typos
# ------------------------
def check_common_dunder_typos(code_text):
    found = False

    for wrong, correct in COMMON_DUNDER_MISTAKES.items():
        if wrong in code_text:
            print(f"⚠️ Warning: '{wrong}' is probably meant to be '{correct}'.")
            print(f"💡 Fix: rename {wrong} to {correct}.")
            found = True

    if not found:
        print("✅ No common dunder typos found.")


# ------------------------
# Hooks
# ------------------------
def _ipython_handler(shell, etype, evalue, tb, tb_offset=None):
    _print_friendly_error(etype, evalue, tb)


def _python_handler(etype, evalue, tb):
    _print_friendly_error(etype, evalue, tb)


# ------------------------
# Activate
# ------------------------
def activate():
    sys.excepthook = _python_handler

    try:
        from IPython import get_ipython
        ip = get_ipython()
    except:
        ip = None

    if ip is not None:
        ip.set_custom_exc((Exception,), _ipython_handler)
        print("LessScary is active. Best in Spyder using Run Selection.")
    else:
        print("LessScary is active.")

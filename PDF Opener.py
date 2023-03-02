import os
import string
import pikepdf
from multiprocessing import Pool

found = False
filename = "test.pdf"

PREFIX = ""
SUFFIX = ""

length = 4

small_letters = False
capital_letters = False
numbers = True
spaces = False

def combomaker(options, depth, prefix, suffix, past = "", arr = []):
    for i in options:
        if depth > 1:
            combomaker(options, depth - 1, prefix, suffix, past + str(i), arr)
        elif depth == 1:
            arr.append(prefix + past + str(i) + suffix)

    return arr

def unlock(password):
    
    global found, filename
    if found:
        return False, None
    try:
        pdf = pikepdf.open(f"{filename}", password=f"{password}")
        pdf.save(f"unlocked_{filename}")
        found = True
        return True, password
    except:
        pass

    return False, None


if __name__ == '__main__':

    options = ""

    if small_letters:
        options += string.ascii_lowercase

    if capital_letters:
        options += string.ascii_uppercase

    if numbers:
        options += string.digits

    if spaces:
        options += " "
        
    passwords = combomaker(options, length, PREFIX, SUFFIX)
    print(f"{len(passwords)} combinations")

    if os.path.isfile(filename):
        with Pool() as pool:
            result = pool.imap_unordered(unlock, passwords)
            for condition, p in result:
                if condition:
                    print(f"Password {p}")
                    break


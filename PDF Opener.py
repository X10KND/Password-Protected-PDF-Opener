import os
import fitz
import math
import string
from multiprocessing import Pool

filename = "test.pdf"

pdf_document = fitz.open(filename)

PREFIX = ""
SUFFIX = ""

length = 6

small_letters = False
capital_letters = False
numbers = True
spaces = False


def combomaker(options, depth, prefix, suffix, past, arr):
    for i in options:
        if depth > 1:
            combomaker(options, depth - 1, prefix, suffix, past + str(i), arr)
        elif depth == 1:
            arr.append(prefix + past + str(i) + suffix)


def unlock(password):
    if pdf_document.authenticate(password):
        pdf_document.save(f"unlocked_{filename}")
        pdf_document.close()
        return password
    return False


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
    
    passwords = []
    combomaker(options, length, PREFIX, SUFFIX, "", passwords)
    print(f"{len(passwords)} combinations")
    print(f"10^{round(math.log(len(passwords), 10))} combinations")

    if os.path.isfile(filename):
        with Pool(processes=16) as pool:
            result = pool.imap_unordered(unlock, passwords)
            for p in result:
                if p:
                    print(f"Password {p}")
                    break

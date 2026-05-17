import os

counter = 0
for file in os.listdir():
    if file == "naming_convention.py":continue
    counter += 1
    extention = file
    extention = file.split(".")[-1]
    naming_convetion = f"genius_{counter}.{extention}"
    os.rename(file,  naming_convetion  )
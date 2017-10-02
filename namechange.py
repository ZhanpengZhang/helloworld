import os
import re


def renamefile():
    directory = "/home/zhanpeng/Downloads/udacity/prank/prank"
    os.chdir(directory)
    print("current working directory been changed to", directory)
    name_list = os.listdir(directory)
    for name in name_list:
        print("starting to rename the file named", name)
        # transtable = name.maketrans("012", '  ')
        withoutnum = re.compile("\D*")
        mt = withoutnum.match(name)
        os.rename(name, mt.group())
        print(name, "has been renamed to", mt.group())


renamefile()

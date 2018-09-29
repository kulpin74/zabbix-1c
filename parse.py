#import os

ib_list = []
ib_el = {}
with open('ib list', 'r') as txt_file:
    for line in txt_file:
        if line == '\n':
            ib_list.append(ib_el)
            ib_el = {}
        else:
            ib_el = {**ib_el, **dict([[i.strip() for i in line.split(':')]])}
print(ib_list)

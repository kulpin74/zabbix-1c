import subprocess


#const_CLUSTER = 'c7792757-c8d4-4e4f-8e75-6ff0b69d135e'
#result = subprocess.check_output(['rac', 'infobase', 'list', '--cluster='+const_CLUSTER])
#print(result)
ib_list = []
ib_el = {}
with open('ib_list1', 'r') as txt_file:
    for line in txt_file:
        rac_res = line
        for ib in rac_res.split('\r\n\r\n'):
            ib_el = dict([i.strip() for i in ib.split('\r\n')])
            ib_list.append(ib_el)
            #if line == '\n':
            #    ib_list.append(ib_el)
            #    ib_el = {}
            #else:
            #    ib_el = {**ib_el, **dict([[i.strip() for i in ib.split(':')]])}
print(ib_list)

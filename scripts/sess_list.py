import subprocess
import json
import sys
import os


C_PAGE = 'cp866' if os.name == 'nt' else ''


def get_dict_from_string(txt_block):
    dict_el = {}
    for i in txt_block.split('\r\n'):
        for j in i.split('\n'):
            key, value = j.split(':')
            dict_el.update({key.strip(): value.strip().strip('"')})
    return dict_el


dict_apps = {'COMConnection': 0,
             'Designer': 0,
             '1CV8C': 0,
             '1CV8': 0,
             'BackgroundJob': 0,
             'WebClient': 0,
             'blockedByDBMS': 0,
             'dbProcTook': 0,
             'bytesAll': 0}
cmd_list = ['rac', 'session', 'list', '--cluster=' + sys.argv[2]]
if sys.argv[1] != 'all_infobases':
    cmd_list.append('--infobase=' + sys.argv[1])
sess_res = subprocess.check_output(cmd_list).decode(C_PAGE).strip()
if len(sess_res) < 2:
    print(json.dumps(dict_apps))
    sys.exit()
sess_list = []
for sess in sess_res.split('\r\n\r\n'):
    sess_list.append(get_dict_from_string(sess))

for sess in sess_list:
    if sess['app-id'] not in dict_apps:
        dict_apps[sess['app-id']] = 0
    dict_apps[sess['app-id']] += 1
    dict_apps['blockedByDBMS'] += int(sess['blocked-by-dbms'])
    dict_apps['dbProcTook'] += int(sess['db-proc-took'])
    dict_apps['bytesAll'] += int(sess['bytes-all'])
print(json.dumps(dict_apps))

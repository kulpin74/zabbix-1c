import subprocess
import json
import sys


def getDictFromString(txtBlock):
    dict_el = {}
    for i in txtBlock.split('\r\n'):
        dict_el = {**dict_el, **dict([[j.strip() for j in i.split(' :')]])}
    return dict_el


dict_apps = {'COMConnection': 0, 'Designer': 0, '1CV8C': 0, '1CV8': 0, 'BackgroundJob': 0}
cluster_res = subprocess.check_output(['rac', 'cluster', 'list']).decode('cp866').strip()
cluster = getDictFromString(cluster_res)
sess_res = subprocess.check_output(['rac', 'session', 'list', '--cluster='+cluster['cluster'],
                                    '--infobase='+sys.argv[1]]).decode('cp866').strip()
if len(sess_res) < 2:
    print(json.dumps(dict_apps))
    sys.exit()
sess_list = []
for sess in sess_res.split('\r\n\r\n'):
    sess_list.append(getDictFromString(sess))

for sess in sess_list:
    if sess['app-id'] not in dict_apps:
        dict_apps[sess['app-id']] = 0
    dict_apps[sess['app-id']] += 1
print(json.dumps(dict_apps))

import subprocess
import json


def getDictFromString(txtBlock):
    dict_el = {}
    for i in txtBlock.split('\r\n'):
        dict_el = {**dict_el, **dict([[j.strip() for j in i.split(' :')]])}
    return dict_el


cluster_res = subprocess.check_output(['rac', 'cluster', 'list']).decode('cp866').strip()
cluster = getDictFromString(cluster_res)
ib_res = subprocess.check_output(['rac', 'infobase', 'summary', 'list',
                                  '--cluster='+cluster['cluster']]).decode('cp866').strip()
ib_res = ib_res.replace("infobase", "{#INFOBASE}")
ib_res = ib_res.replace("name", "{#NAME}")
ib_res = ib_res.replace("descr", "{#DESCR}")
ib_list = []
for ib in ib_res.split('\r\n\r\n'):
    ib_list.append(getDictFromString(ib))
ib_list.append({"{#INFOBASE}": "all_infobases", "{#NAME}": "All_IBs_of_cluster", "{#DESCR}": "all_infobases"})
print(json.dumps({'data': ib_list}))

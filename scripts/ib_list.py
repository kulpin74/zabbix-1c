import subprocess
import json


def getDictFromString(txtBlock):
    dict_el = {}
    for i in txtBlock.split('\r\n'):
        dict_el = {**dict_el, **dict([[j.strip().strip('"') for j in i.split(' :')]])}
    return dict_el


cluster_res = subprocess.check_output(['rac', 'cluster', 'list']).decode('cp866').strip()
ib_list = []
for cluster in cluster_res.split('\r\n\r\n'):
    curr_cluster = getDictFromString(cluster)
    ib_res = subprocess.check_output(['rac', 'infobase', 'summary', 'list', '--cluster='+curr_cluster['cluster']]).decode('cp866').strip()
    ib_res = ib_res.replace("infobase", "{#INFOBASE}")
    ib_res = ib_res.replace("name", "{#NAME}")
    ib_res = ib_res.replace("descr", "{#DESCR}")
    for ib in ib_res.split('\r\n\r\n'):
        ib_list.append({**getDictFromString(ib),
                        "{#CLUSTER}": curr_cluster['cluster'],
                        "{#CLUSTER_NAME}": curr_cluster['name']})
    ib_list.append({"{#INFOBASE}": "all_infobases",
                    "{#NAME}": "All_IBs_of_cluster",
                    "{#DESCR}": "all_infobases",
                    "{#CLUSTER}": curr_cluster['cluster'],
                    "{#CLUSTER_NAME}": curr_cluster['name']})
print(json.dumps({'data': ib_list}))

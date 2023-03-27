import subprocess
import json
import os
import sys
from sys import getdefaultencoding


C_PAGE = 'cp866' if os.name == 'nt' else getdefaultencoding()
cluster_user = '--cluster-user='+sys.argv[1] if len(sys.argv) >= 2 else ''
cluster_pwd  = '--cluster-pwd='+sys.argv[2]  if len(sys.argv) >= 2 else ''
BR = '\r\n' if os.name == 'nt' else '\n'


def get_dict_from_string(txt_block):
    dict_el = {}
    for i in txt_block.split(BR):
        try:
            key, value = i.split(':', 1)
            dict_el.update({key.strip(): value.strip().strip('"')})
        except ValueError as exc:
            pass
    return dict_el


cluster_res = subprocess.check_output(['rac', 'cluster', 'list']).decode(C_PAGE).strip()
ib_list = []
for cluster in cluster_res.split(BR+BR):
    curr_cluster = get_dict_from_string(cluster)
    cluster_uuid = curr_cluster.get('cluster')
    if cluster_uuid:
        cmd_list = ['rac', 'infobase', 'summary', 'list', '--cluster='+cluster_uuid]
        if len(sys.argv) >= 2:
            cmd_list += [cluster_user, cluster_pwd]
        ib_res = subprocess.check_output(cmd_list).decode(C_PAGE).strip()

        ib_res = ib_res.replace("infobase", "{#INFOBASE}")
        ib_res = ib_res.replace("name", "{#NAME}")
        ib_res = ib_res.replace("descr", "{#DESCR}")
        for ib in ib_res.split(BR+BR):
            ib_list.append({**get_dict_from_string(ib),
                            "{#CLUSTER}": curr_cluster['cluster'],
                            "{#CLUSTER_NAME}": curr_cluster['name']})
        ib_list.append({"{#INFOBASE}": "all_infobases",
                        "{#NAME}": "All_IBs_of_cluster",
                        "{#DESCR}": "all_infobases",
                        "{#CLUSTER}": curr_cluster['cluster'],
                        "{#CLUSTER_NAME}": curr_cluster['name']})
print(json.dumps({'data': ib_list}))

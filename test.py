import requests
import codecs
import sys
import time
import os
import io
import pickle
import copy
from pprint import pprint


sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='UTF-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='UTF-8')
all_stop = {}
stop_default = {'update_date':'', 'update_time':'', 'code_name':'','longitude':'','latitude':'','qua_cntu':'','qua_cl':'','qua_ph':''}

reponse = requests.get("https://data.taipei/opendata/datalist/apiAccess?scope=resourceAquire&rid=190796c8-7c56-42e0-8068-39242b8ec927").json()


for i in range(len(reponse['result']['results'])):
    if reponse['result']['results'][i]['code_name'] is None:
        continue
    all_stop[reponse['result']['results'][i]['code_name']] = copy.deepcopy(stop_default)
#    print(all_stop)
    for value in all_stop[reponse['result']['results'][i]['code_name']]:
#        print(value)
        if reponse['result']['results'][i][value] is not None:
            all_stop[reponse['result']['results'][i]['code_name']][value]=reponse['result']['results'][i][value].replace(' ','')
        else:
            all_stop[reponse['result']['results'][i]['code_name']][value]=reponse['result']['results'][i][value]

#print(all_stop)
pickle.dump(all_stop, codecs.open('all_stop.p','wb'))

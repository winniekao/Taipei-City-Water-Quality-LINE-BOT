import pickle
import codecs
all_stop = pickle.load(codecs.open('./all_stop.p','rb'))

for value in all_stop:
    if all_stop[value]['longitude'] is None:
        print(all_stop[value])
    if all_stop[value]['latitude'] is None:
        print(all_stop[value]) 

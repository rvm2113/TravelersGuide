import json
import requests
import StringIO
from elasticsearch import Elasticsearch
#import pandas as pd
#df = pd.read_json("cities.json")
with open("worldwide_locations.json") as fd:
	json_data = json.load(fd)



es = Elasticsearch(hosts = ["10.0.2.15"],  http_auth=('elastic', 'changeme'),  port = 9200)

res = es.indices.create(index = "cities", body = 
'''{
  "settings": {
    "number_of_replicas": 1,
    "number_of_shards": 3,
    "analysis": {
      
    },
    "refresh_interval": "1s"
  },
  "mappings": {
    "city": {
      "properties": {
        "geoip": {
          "dynamic": "true",
          "properties": {
            "location": {
              "type": "geo_point"
            }
          }
        },
        "location": {
          "type": "geo_shape",
          "tree": "quadtree",
          "precision": "100m"
        },
        "name": {
          "type": "text"
        },
        "country": {
          "type": "text"
        },
       	"id": {
       	  "type": "long"
       	}
      }
    }
  }
}''')


print "Creation of index response: " + str(res)

#file_n = "cities.json"
#arr = json.loads(file_n)


#define an index
#url = "http://localhost:9200/cities"
#headers = {'content-type': 'application/json'}
#response = requests.put(url)
#print response.text

#index all documents
for entry in range(len(json_data)):
# #	print json_data[entry]['rank']
 	#headers = {'content-type': 'cities.json'}
 	#json_data[entry]['location'] = {"type": "geo_point", "coordinates": [json_data[entry]['longitude'], json_data[entry]['latitude']]}
  json_data[entry]['geoip'] = {}
  json_data[entry]['geoip']['location'] = str(json_data[entry]['coord']['lat'])+","+str(json_data[entry]['coord']['lon'])
 	#json_data[entry]['geo'] = str(json_data[entry]['latitude'])+","+str(json_data[entry]['longitude'])
  json_data[entry]['location'] = {}
  json_data[entry]['location']['type'] = "point"
  json_data[entry]['location']['coordinates'] = []
  json_data[entry]['location']['coordinates'].append(json_data[entry]['coord']['lon'])
  json_data[entry]['location']['coordinates'].append(json_data[entry]['coord']['lat'])
  if json_data[entry]['id'] != None:
    json_data[entry]['id'] = long(json_data[entry]['id'])
 # 	string_version = json.dumps(json_data[entry])
	# out = StringIO.StringIO()
 # 	for line in string_version:
 #   		out.write(line)
	# data = out.getvalue()
	# print data
 	# url = "http://localhost:9200/cities/city/" + str(json_data[entry]['id'])
 	#print(url)
 	#print (json_data[entry])
 	#hdr = {"Content-Type": "text/plain"}
 	#response = requests.put(url, data)
 	#print(response.text)
 	#print(json_data[entry])
  response = es.index(index = "cities", doc_type = "city", id = json_data[entry]['id'], body = json_data[entry])
  print response
 	
 	



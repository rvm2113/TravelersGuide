import json
import requests
import StringIO
from elasticsearch import Elasticsearch

with open("worldwide_locations.json") as fd:
	json_data = json.load(fd)




#creation of city index
# within Elasticsearch

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




#This segment 
#indexes each document(containing city data)
#into Elasticsearch
for entry in range(len(json_data)):
  json_data[entry]['geoip'] = {}
  json_data[entry]['geoip']['location'] = str(json_data[entry]['coord']['lat'])+","+str(json_data[entry]['coord']['lon'])
  json_data[entry]['location'] = {}
  json_data[entry]['location']['type'] = "point"
  json_data[entry]['location']['coordinates'] = []
  json_data[entry]['location']['coordinates'].append(json_data[entry]['coord']['lon'])
  json_data[entry]['location']['coordinates'].append(json_data[entry]['coord']['lat'])
  if json_data[entry]['id'] != None:
    json_data[entry]['id'] = long(json_data[entry]['id'])
  response = es.index(index = "cities", doc_type = "city", id = json_data[entry]['id'], body = json_data[entry])
  print response
 	
 	



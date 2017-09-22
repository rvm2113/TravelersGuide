import json
import requests
import StringIO
from elasticsearch import Elasticsearch


with open("airports_db.json") as fd:
	json_data = json.load(fd)


#The airport index is created
#within Elasticsearch

es = Elasticsearch(hosts = ["10.0.2.15"],  http_auth=('elastic', 'changeme'),  port = 9200)

res = es.indices.create(index = "transportation", body = 
'''{
  "settings": {
    "number_of_replicas": 1,
    "number_of_shards": 3,
    "analysis": {
      
    },
    "refresh_interval": "1s"
  },
  "mappings": {
    "station": {
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
        "city": {
          "type": "text"
        },
        "country": {
          "type": "text"
        },
        "elevation": {
          "type": "long"
        },
        "iata": {
          "type": "text"
        },
        "icao": {
          "type": "text"
        },
        "tz": {
          "type": "text"
        }
      }
    }
  }
}''')



#Documents containing airport 
#data are indexed into Elasticsearch

entry_num = 1
for entry, value in json_data.iteritems():
	value['geoip'] = {}
 	value['geoip']['location'] = str(value['lat'])+","+str(value['lon'])

 	value['location'] = {}
 	value['location']['type'] = "point"
 	value['location']['coordinates'] = []
 	value['location']['coordinates'].append(value['lon'])
 	value['location']['coordinates'].append(value['lat'])
	if value['elevation'] != None:
 		value['elevation'] = long(value['elevation'])
 
 	
 	response = es.index(index = "transportation", doc_type = "station", id = entry_num, body  = value)
 	print(response)
 	entry_num+=1
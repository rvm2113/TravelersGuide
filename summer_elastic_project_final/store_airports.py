import json
import requests
import StringIO
from elasticsearch import Elasticsearch


with open("airports_db.json") as fd:
	json_data = json.load(fd)



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

print "Creation of index response: " + str(res)

entry_num = 1
for entry, value in json_data.iteritems():
	value['geoip'] = {}
 	value['geoip']['location'] = str(value['lat'])+","+str(value['lon'])

 	value['location'] = {}
 	value['location']['type'] = "point"
 	value['location']['coordinates'] = []
 	value['location']['coordinates'].append(value['lon'])
 	value['location']['coordinates'].append(value['lat'])
 	#if value['woeid'] != None:
 	#	value['woeid'] = long(value['woeid'])
 	#if value['runway_length'] != None:
	# 	value['runway_length'] = long(value['runway_length'])
	if value['elevation'] != None:
 		value['elevation'] = long(value['elevation'])
 	#if value['direct_flights'] != None:
	#	value['direct_flights'] = long(value['direct_flights'])
	#if value['carriers'] != None:
 	#	value['carriers'] = long(value['carriers'])

  	#string_version = json.dumps(value)
	# out = StringIO.StringIO()
 # 	for line in string_version:
 #   		out.write(line)
	# data = out.getvalue()
	#print data
 	#url = "http://localhost:9200/transportation/station/" + str(value['woeid'])
 	
 	response = es.index(index = "transportation", doc_type = "station", id = entry_num, body  = value)
 	#response = requests.put(url, data)
 	print(response)
 	entry_num+=1
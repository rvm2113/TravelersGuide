# TravelersGuide

Traveler's Guide allows users to specify locations in the world where they would prefer to travel, the address of each person(in case of a group rendez-vous), preferred radius/distance to nearby airports, and preferred weather for the destination. Traveler's Guide then customizes and outputs all cities that 
match the given criteria.

System Requirements:
Elasticsearch 2-noded cluster(with hot-warm node configuration
and 1 node set to master)
JSON file of airport locations
JSON file of city locations

Usage: 

(For Setup): 
python store_airports.py
python create_entries.py


(The avoid_areas_file and avoid_distance are optional parameters)
python travelers_guide_test.py [destinations_file] [travelers_addresses_file] [avoid_areas_file] [avoid_distance] [airport_distance] [city_preferences_file]




# TravelersGuide

Traveler's Guide allows users to specify locations in the world where they would prefer to travel, the address of each person(in case of a group rendez-vous), preferred radius/distance to nearby airports, and preferred weather for the destination. Traveler's Guide then customizes and outputs all cities that 
match the given criteria.

# System Requirements:
<br />
Elasticsearch 2-noded cluster(with hot-warm node configuration
and 1 node set to master)<br />
JSON file of airport locations <br />
JSON file of city locations<br />

# Usage: 
<br />
(For Setup): 
python store_airports.py <br />
python create_entries.py <br />


(The avoid_areas_file and avoid_distance are optional parameters)<br />
python travelers_guide_test.py [destinations_file] [travelers_addresses_file] [avoid_areas_file] [avoid_distance] [airport_distance] [city_preferences_file]<br />




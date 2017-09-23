# Traveler's Guide

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
python store_airports.py [Airport JSON file]<br />
python create_entries.py [City JSON file]<br />


(The avoid_areas_file and avoid_distance are optional parameters)<br />
(For actual usage)<br />
python travelers_guide_test.py [destinations_file] [travelers_addresses_file] [avoid_areas_file] [avoid_distance] [airport_distance] [city_preferences_file]<br />



# Technologies Used:
Elasticsearch Python Multi-Search API <br />
Elasticsearch GeoSpatial Queries <br />
Elasticsearch Python Search API} <br />
Google's Geocoding API(to convert addresses to latitude/longitude values) <br />
Elasticsearch Function Score Query/Decay Functions <br />
OpenWeatherMap 5 day, 3-hour Weather API <br />



# Functionalities:
<br />
By using Elasticsearch's Python Multisearch API, a series of possible airports can
be written to a file after the user/client specifies a list of destinations.
Traveler's Guide then executes geo_spatial queries in parallel for each of these
destinations such that airports can be found within a certain radius of each destination(the
radius distance is specified by the user in km).


<br />
<br />
<br />
By using Elasticsearch's Python Search API, Traveler's Guide can construct a geo_shape
given a series of traveler's addresses and multiple circles/geo_shapes for each "to be avoided"
address. Traveler's Guide then carries out one geo_spatial query with an array of geo_shapes.
This query finds all locations within the geo_shape of traveler's addresses and outside each of
the geo_shapes constructed around all "to be avoided" addresses.

<br />
<br />
<br />

Once all eligible cities are found, historical 5-day, 3-hour weather data is obtained 
for each city(through OpenWeatherMap's API) and the cities are indexed
under the index city_statistics(with weather data included).
By using function scoring and decay functions within 4 queries, the cities are categorized by the four
weather statistics and written to a file by rankings.


# Output:
The following output files are generated:
<br />
airports_near_destinations.txt (contains airports corresponding to each destination)
<br />
cities_near_travelers.txt (contains cities categorized by humidity, temperature,
cloud_percentage, wind_speed)




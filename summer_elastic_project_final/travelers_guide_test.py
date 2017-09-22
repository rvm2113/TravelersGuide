from travelers_guide import TravelGuide
import sys

# 
if __name__ == "__main__":
	if len(sys.argv) < 5:
		print('Insufficient number of arguments.')
		print('Usage: python travelers_guide_test.py [destinations_file] [travelers_addresses_file] [avoid_areas_file] [avoid_distance] [airport_distance] [city_preferences_file]')
		print('Optional fields: [avoid_areas_file] [avoid_distance]')
	elif len(sys.argv) == 5: 
		destinations_file = sys.argv[1]
		travelers_addresses_file = sys.argv[2]
		airport_distance = sys.argv[3]
		city_preferences_file = sys.argv[4]
		tg = TravelGuide(destinations_file, travelers_addresses_file, airport_distance, ' ', ' ', city_preferences_file)
		common_cities =tg.find_common_cities()
		nearby_airports = tg.find_airports_near_destinations()

	elif len(sys.argv) == 7:
		destinations_file = sys.argv[1]
		travelers_addresses_file = sys.argv[2]
		avoid_areas_file = sys.argv[3]
		avoid_distance = sys.argv[4]
		airport_distance = sys.argv[5]
		city_preferences_file = sys.argv[6]
		tg = TravelGuide(destinations_file, travelers_addresses_file, airport_distance, avoid_areas_file, avoid_distance ,city_preferences_file)
		common_cities = tg.find_common_cities()
		nearby_airports = tg.find_airports_near_destinations()
	
	else:
		print('Incorrect number of arguments')
		print('Usage: python travelers_guide_test.py [destinations_file] [travelers_addresses_file] [avoid_areas_file] [avoid_distance] [airport_distance]')
		print('Optional fields: [avoid_areas_file] [avoid_distance]')



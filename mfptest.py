import myfitnesspal
import datetime
from collections import OrderedDict
from datetime import datetime
from datetime import timedelta
import timestring
import csv
import sys




LBS_TO_KG = 0.453592

username_umar = 'umarqattan'
username_zack = 'zakaton'

umar = myfitnesspal.Client(username_umar)
zack = myfitnesspal.Client(username_zack)




class Nutrient:
	
	def __init__(self):
		self.CALORIES=0
		self.FAT = 1
		self.CARBOHYDRATES = 2
		self.NET_CARBOHYDRATES = 3
		self.PROTEIN = 4
		self.FIBER = 5
		self.SODIUM = 6
		self.nutrients = {'calories':self.CALORIES, 'fat':self.FAT, 'carbohydrates':self.CARBOHYDRATES, 'net_carbohydrates': self.NET_CARBOHYDRATES, 'protein': self.PROTEIN, 'fiber': self.FIBER, 'sodium': self.SODIUM}
		self.nutrients_array = range(7)


	def valueForKey(self, key):
		return self.nutrients[key]

	
def get_food_entries_data(client, filter=None):

	
	username = str(client.effective_username)
	date_string = timestring.Range('4 days ago').start.date.date().strftime('%m%d%Y')
	dates = []
	nutrition_data = []
	food_entries = {}

	day = timedelta(days=1)
	date_o = timestring.Range('4 days ago').start.date.date()
	date_f = timestring.Range('4 days ago').end.date.date()

	while date_o <= date_f:
		current_diary_entry = client.get_date(date_o)
		for meal in current_diary_entry.meals:
			for entry in meal.entries:
				if food_entries.get(entry.name, 0) == 0:
					entry_totals = entry.totals
					entry_totals['frequency'] = 1
					food_entries[entry.name] = entry_totals
				else:
					food_entries[entry.name]['frequency'] += 1	
		date_o += day

	sorted_food_entries = (sorted(food_entries.items(), key=lambda x: x[1].get('calories',0)),
							   sorted(food_entries.items(), key=lambda x: (x[1].get('fat', 0) or 1)),#/((x[1].get('protein',0) or 1) + (x[1].get('carbohydrates', 0) or 1) + (x[1].get('fat', 0) or 1))),
							   sorted(food_entries.items(), key=lambda x: (x[1].get('carbohydrates', 0) or 1)),#/((x[1].get('protein',0) or 1) + (x[1].get('carbohydrates', 0) or 1) + (x[1].get('fat', 0) or 1))),
							   sorted(food_entries.items(), key=lambda x: (x[1].get('carbohydrates',0) or 0) if ((x[1].get('carbohydrates',0) or 0)-(x[1].get('fiber',0) or 0) < 0) else ((x[1].get('carbohydrates',0) or 0)-(x[1].get('fiber',0) or 0))),
							   sorted(food_entries.items(), key=lambda x: (x[1].get('protein', 0) or 1)),#/((x[1].get('protein',0) or 1) + (x[1].get('carbohydrates', 0) or 1) + (x[1].get('fat', 0) or 1))),
							   sorted(food_entries.items(), key=lambda x: x[1].get('fiber',0)),
							   sorted(food_entries.items(), key=lambda x: x[1].get('sodium',0)))
	
	if filter is None:
		f_calories          = username + '_food_entries_sorted_by_calories' + '.csv'
		f_fat               = username + '_food_entries_sorted_by_fat' + '.csv'
		f_carbohydrates     = username + '_food_entries_sorted_by_carbohydrates' + '.csv'
		f_net_carbohydrates = username + '_food_entries_sorted_by_net_carbohydrates' + '.csv'
		f_protein           = username + '_food_entries_sorted_by_protein' + '.csv'
		f_fiber             = username + '_food_entries_sorted_by_fiber' + '.csv'
		f_sodium            = username + '_food_entries_sorted_by_sodium' + '.csv'

		files = [
				 f_calories, 
				 f_fat, 
				 f_carbohydrates, 
				 f_net_carbohydrates, 
				 f_protein,
				 f_fiber,
				 f_sodium
				]
		file_number = 0
		for file in files:
			f = open(file, 'wt')
			try:
				
				writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
				writer.writerow( ('Index', 'Food Entry','Calories', 'Fat (g)', 'Carbohydrates (g)','Net Carbohydrate (g)', 'Protein (g)', 'Fiber (g)','Sodium (mg)', 'Frequency'))
				i = 0

				for food_entry_name, food_entry_totals in sorted_food_entries[Nutrient().nutrients_array[file_number]]:
					writer.writerow( (i+1, food_entry_name,food_entry_totals['calories'], food_entry_totals['fat'], food_entry_totals['carbohydrates'],(food_entry_totals.get('carbohydrates',0) or 0) if ((food_entry_totals.get('carbohydrates',0) or 0)-(food_entry_totals.get('fiber',0) or 0) < 0) else ((food_entry_totals.get('carbohydrates',0) or 0)-(food_entry_totals.get('fiber',0) or 0)), food_entry_totals['protein'], food_entry_totals['fiber'],food_entry_totals['sodium'], food_entry_totals['frequency']))
					i += 1
				
			finally:

				f.close()

			file_number += 1
			
	else:
		filename = username + '_food_entries_by_' + filter + '.csv'

		f = open(filename, 'wt')
		try:
			writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
		

			writer.writerow( ('Index', 'Food Entry','Calories', 'Fat (g)', 'Carbohydrates (g)','Net Carbohydrate (g)', 'Protein (g)', 'Fiber (g)','Sodium (mg)', 'Frequency'))
			i = 0
			for food_entry_name, food_entry_totals in sorted_food_entries[Nutrient().valueForKey(filter)]:
				writer.writerow( (i+1, food_entry_name,food_entry_totals['calories'], food_entry_totals['fat'], food_entry_totals['carbohydrates'],(food_entry_totals.get('carbohydrates',0) or 0) if ((food_entry_totals.get('carbohydrates',0) or 0)-(food_entry_totals.get('fiber',0) or 0) < 0) else ((food_entry_totals.get('carbohydrates',0) or 0)-(food_entry_totals.get('fiber',0) or 0)), food_entry_totals['protein'], food_entry_totals['fiber'],food_entry_totals['sodium'], food_entry_totals['frequency']))
				i += 1


		finally:
			f.close()

		print (open(filename, 'rt').read())


def get_full_nutrition_data(client, date=None):
	username = str(client.effective_username)
	filename = ""
	start_date = datetime.today().date()
	dates = []
	nutrition_data = []
	client_macros = []
	meal_keys = client.get_date(start_date).keys() #['supplements', 'meal 1', 'meal 2', 'meal 3', 'snacks', 'refeed']
	meals = []

	# for a single day

	if date is None:
		date_string = timestring.Range('today').start.date.date().strftime('%m%d%Y')
		filename = username + '_nutrition_data_since_' + date_string + '.csv'
		start_date = timestring.Range('today').start.date.date()
		dates.append(start_date)
		nutrition_data.append(client.get_date(start_date).totals)
	else:
		day = timedelta(days=1)
		date_o = timestring.Range(date).start.date.date()
		date_f = timestring.Range(date).end.date.date()
		
		filename = username + '_full_nutrition_data_since_' + date_o.strftime('%m%d%Y') + '.csv'
		
		
		while date_o <= date_f:
			nutrition_datum = client.get_date(date_o).totals
			nutrition_data.append(client.get_date(date_o))
			dates.append(date_o.strftime('%m/%d/%Y'))
			date_o += day

	f = open(filename, 'wt')
	try:
		writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
		
		for i in range (len(nutrition_data)):
			writer.writerow( (i+1, dates[i], 'Meals','Food Entry', 'Calories', 'Fat (g)', 'Carbohydrates (g)','Net Carbohydrate (g)', 'Protein (g)', 'Fiber (g)','Sodium (mg)'))
			for meal_key in nutrition_data[i].keys():

				writer.writerow((' ',' ', meal_key,'Totals', (nutrition_data[i][meal_key].totals.get('calories',0) or 0), (nutrition_data[i][meal_key].totals.get('fat',0) or 0), (nutrition_data[i][meal_key].totals.get('carbohydrates',0) or 0), (nutrition_data[i][meal_key].totals.get('carbohydrates',0) or 0) if ((nutrition_data[i][meal_key].totals.get('carbohydrates',0) or 0)-(nutrition_data[i][meal_key].totals.get('fiber',0) or 0) < 0) else ((nutrition_data[i][meal_key].totals.get('carbohydrates',0) or 0)-(nutrition_data[i][meal_key].totals.get('fiber',0) or 0)), (nutrition_data[i][meal_key].totals.get('protein',0) or 0), (nutrition_data[i][meal_key].totals.get('fiber',0) or 0), (nutrition_data[i][meal_key].totals.get('sodium',0) or 0) ))
				if len(nutrition_data[i][meal_key].entries) is 0:
					continue
				else:
					for meal_entry in nutrition_data[i][meal_key].entries:
						writer.writerow((' ',' ', ' ', meal_entry.name, meal_entry['calories'], meal_entry['fat'], meal_entry['carbohydrates'], (meal_entry['carbohydrates']) if (meal_entry['carbohydrates']-meal_entry['fiber'] < 0) else (meal_entry['carbohydrates']-meal_entry['fiber']), meal_entry['protein'], meal_entry['fiber'], meal_entry['sodium']))
			writer.writerow((' ',' ', ' ', 'Daily Totals', (nutrition_data[i].totals.get('calories',0) or 0), (nutrition_data[i].totals.get('fat',0) or 0), (nutrition_data[i].totals.get('carbohydrates',0) or 0), (nutrition_data[i].totals.get('carbohydrates',0) or 0) if ((nutrition_data[i].totals.get('carbohydrates',0) or 0)-(nutrition_data[i].totals.get('fiber',0) or 0) < 0) else ((nutrition_data[i].totals.get('carbohydrates',0) or 0)-(nutrition_data[i].totals.get('fiber',0) or 0)), (nutrition_data[i].totals.get('protein',0) or 0), (nutrition_data[i].totals.get('fiber',0) or 0), (nutrition_data[i].totals.get('sodium',0) or 0) ))
	finally:
		f.close()

	print (open(filename, 'rt').read())

def get_nutrition_data(client, date=None):
	username = str(client.effective_username)
	filename = ""
	start_date = datetime.today().date()
	dates = []
	nutrition_data = []
	client_macros = []

	if date is None:
		date_string = timestring.Range('today').start.date.date().strftime('%m%d%Y')
		filename = username + '_nutrition_data_since_' + date_string + '.csv'
		start_date = timestring.Range('today').start.date.date()
		dates.append(start_date)
		nutrition_data.append(client.get_date(start_date).totals)
	else:
		day = timedelta(days=1)
		date_o = timestring.Range(date).start.date.date()
		date_f = timestring.Range(date).end.date.date()
		
		filename = username + '_nutrition_data_since_' + date_o.strftime('%m%d%Y') + '.csv'
		
		
		while date_o <= date_f:
			dates.append(date_o.strftime('%m/%d/%Y'))
			nutrition_datum = client.get_date(date_o).totals
			nutrition_data.append(client.get_date(date_o).totals)
			date_o += day

	f = open(filename, 'wt')
	try:
		writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
		writer.writerow( ('Index', 'Date (mm/dd/YYYY)', 'Calories','Fats (g)', 'Carbohydrates (g)', 'Protein (g)', 'Fiber (g)','Sodium (mg)' ))
		for i in range (len(nutrition_data)):
			writer.writerow( (i+1, dates[i], nutrition_data[i]['calories'], nutrition_data[i]['fat'], nutrition_data[i]['carbohydrates'], nutrition_data[i]['protein'], nutrition_data[i]['fiber'], nutrition_data[i]['sodium'] ) )
	finally:
		f.close()

	print (open(filename, 'rt').read())
# since date (1 week ago, 10 days ago, 2 years ago, etc. )
def get_body_data(client,date=None):

	username = str(client.effective_username)
	filename = ""
	start_date = datetime.today().date()
	dates = []
	weights = []
	body_fats = []


	client_weight = OrderedDict()
	client_body_fat = OrderedDict()

	if date is None:
		date_string = timestring.Range('30 days ago').start.date.date().strftime('%m%d%Y')
		filename = username + '_body_data_since_' + date_string +'.csv'
		client_weight = client.get_measurements('Weight')
		client_body_fat = client.get_measurements('Body Fat %')
	else:
		filename = username + 'body_data_since_' + date + '.csv'
		start_date = start_date = timestring.Range(date).start.date.date()
		client_weight = client.get_measurements('Weight', start_date)
		client_body_fat = client.get_measurements('Body Fat %', start_date)
		
	i = 0
	date_keys = []
	for (d1, w) in sorted(client_weight.iteritems()):
		dates.append(datetime.strftime(d1,"%m/%d/%Y"))
		weights.append(w)
		date_keys.append(d1)

	body_fat_dict = dict(client_body_fat)
	for key in date_keys:
		body_fats.append(body_fat_dict.get(key, 0) or 0)
	
	f = open(filename, 'wt')
	try:
		writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
		writer.writerow( ('Index', 'Date (mm/dd/YYYY)', 'Weight (lbs)', 'Weight (kg)', 'Body Fat (%)'))
		for i in range (len(dates)):
			writer.writerow( (i+1, dates[i], weights[i], round(weights[i]*LBS_TO_KG,2), body_fats[i] ) )
	finally:
		f.close()

	print (open(filename, 'rt').read())

#get_body_data(umar, "2 years ago")
#get_nutrition_data(umar)
#get_full_nutrition_data(umar, '7 days ago')
get_food_entries_data(umar, filter=None)




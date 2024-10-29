import requests
import pandas as pd

url = "https://tasty.p.rapidapi.com/recipes/list"



headers = {
	"x-rapidapi-key": "a85dfca343msh4e5c92e9bfbadfep10f224jsn2512379d7755",
	"x-rapidapi-host": "tasty.p.rapidapi.com"
}

nutritional_values = []
negative_nutrition = ['fat', 'sugar']
food_popularity = []
reviews = []
prep_times = []

def api_call(food, version):
	
	querystring = {"from":"0","size":"10000","tags":"under_30_minutes", "q": food}

	response = requests.get(url, headers=headers, params=querystring)

	df = response.json()
	
	#food name
	print(df['results'][version]['slug'])
	
	#nutritional value
	print('Nutritional Value')
	calorie_count = 1
	nutritional_total = 0
	for chemical, value in df['results'][version]['nutrition'].items():
			if chemical == 'calories':	
				calorie_count = value
			elif isinstance(value, int) == True:
				desired_value = value/calorie_count
				print('\t' + chemical + ': ' + str(value))
				if chemical in negative_nutrition:
					desired_value = desired_value * -1
				nutritional_total = nutritional_total + desired_value 
	nutritional_values.append(nutritional_total)
	
	#reviews
	popularity = df['results'][version]['user_ratings']['count_negative'] + df['results'][version]['user_ratings']['count_positive']
	print("Number of Reviews: " + str(popularity))
	food_popularity.append(popularity)
	
	positivity_percentage = df['results'][version]['user_ratings']['score'] * 100
	print("Percent of positive reviews: " + str(positivity_percentage) +'%')
	reviews.append(positivity_percentage)
	
	#time to make
	time = df['results'][version]['total_time_minutes']
	print('total time to make: ' + str(time) + 'min')
	prep_times.append(time)
	print(' ')



api_call('french toast', 11)
api_call('pancake', 29)
api_call('waffles', 2)


i = 0
dataframe_values = []
while i < 3:
	dataframe_values.append([nutritional_values[i], food_popularity[i], reviews[i], prep_times[i]])
	i += 1



d = {'French Toast': dataframe_values[0], 'Pancake': dataframe_values[1], 'Waffles' : dataframe_values[2]}
data_frame = pd.DataFrame(data = d, index = ['nutritional value', 'popularity', 'reviews', 'prep time'])

print(data_frame)




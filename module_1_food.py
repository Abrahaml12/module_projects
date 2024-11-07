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

conditional_arrays = [nutritional_values, food_popularity, reviews, prep_times]

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

api_call('french toast', 12)
api_call('pancake', 29)
api_call('waffles', 2)

#metric dataframe
i = 0
dataframe_values = []
while i < 3:
	dataframe_values.append([nutritional_values[i], food_popularity[i], reviews[i], prep_times[i]])
	i += 1

d = {'French Toast': dataframe_values[0], 'Pancake': dataframe_values[1], 'Waffles' : dataframe_values[2]}
data_frame = pd.DataFrame(data = d, index = ['nutritional value', 'popularity', 'review score', 'prep time'])

print(data_frame)

#dataframe analysis
nutrition_min = min(nutritional_values) +1
popularity_min = min(food_popularity)
reviews_min = min(reviews)
time_min = min(prep_times)

nutritional_result = []
popularity_result = []
reviews_result = []
time_result = []

i = 0
for value in nutritional_values:
	value = value +1
	nutritional_values[i] = value
	nutritional_result.append(value/nutrition_min)
	i = i+1


i = 0
for value in food_popularity:
	result_value = value/popularity_min
	if result_value != 1:
		result_value = result_value/2
	popularity_result.append(result_value)
	i+= 1

i = 0
for value in reviews:
	reviews_result.append(value/reviews_min)
	i+= 1

i = 0
for value in prep_times:
	time_result.append(3 - value/time_min)
	i+= 1


ft_results = [nutritional_result[0], popularity_result[0], reviews_result[0], time_result[0], 0]
ft_results[4] = sum(ft_results)

p_results =  [nutritional_result[1], popularity_result[1], reviews_result[1], time_result[1], 0]
p_results[4] = sum(p_results)

w_results = [nutritional_result[2], popularity_result[2], reviews_result[2], time_result[2], 0]
w_results[4] = sum(w_results)


print('')
result_d = {'French Toast': ft_results, 'Pancake': p_results, 'Waffles' : w_results}
data_frame = pd.DataFrame(data = result_d, index = ['nutritional value', 'popularity', 'review score', 'prep time', 'total'])
print(data_frame)

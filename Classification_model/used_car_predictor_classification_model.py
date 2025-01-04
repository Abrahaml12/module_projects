import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np


df = pd.read_csv('used_car_dataset.csv', index_col= 'Id')



df['Age'] = pd.to_numeric(df['Age'])

df['Transmission'] = df['Transmission'].map({'Manual': 0, 'Automatic': 1}) 
df['Owner'] = df['Owner'].map({'first': 1, 'second': 2}) 
df['kmDriven'] = pd.to_numeric(df['kmDriven'])
df = df[df['FuelType'] != 'Hybrid/CNG']


df['FuelType'] = df['FuelType'].map({'Diesel': 0, 'Petrol': 1}) 

df['AskPrice'] = pd.to_numeric(df['AskPrice'])

# df['Discharge Date'] = pd.to_datetime(df['Discharge Date']).astype(int)

# df['time_durr'] = df['Discharge Date'] - df['Date of Admission'] 

# print(df["Medical Condition"].values)


df['model'] = df['model'].apply(lambda x: [x])
df['Brand'] = df['Brand'].apply(lambda x: [x])

mlb = MultiLabelBinarizer()
brands = mlb.fit_transform(df['model'].values)
brands_df = pd.DataFrame(brands, columns = mlb.classes_)

print(brands_df[:5])


X = df[['kmDriven', 'Transmission', 'AskPrice','FuelType', 'Year']]

print(X)

y = brands_df
#print(y[:5])

brands_array = y.columns.values

print(brands_array)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= .2)

depth = 75

clf = DecisionTreeClassifier(max_depth = depth)

clf.fit(X_train,y_train)
test_pred = clf.predict(X_test)

test_correct = []

print(test_pred[:5])

for i in range(len(test_pred)):
  test=test_pred[i]
  actual = y_test.values[i]
  if any(test[j] == 1 and actual[j] == 1 for j in range(len(test))):
    test_correct.append(True)
  else: 
    test_correct.append(False)
    pbrand_index = np.where(test_pred[i] == 1)[0][0]
    abrand_index = np.where(y_test.values[i] == 1)[0][0]
    print(f'id: {i}  predicted model: {brands_array[pbrand_index]}  actual model: {brands_array[abrand_index]}')

test_accuracy = np.mean(test_correct)

print(f'maxdepth={depth} | test_accuracy: {(test_accuracy*100):2f}%')

# importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
import plotly.express as px
from PIL import Image

import warnings
warnings.filterwarnings('ignore')
plt.style.use('seaborn')

%matplotlib inline


pip install haversine


from haversine import haversine

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestRegressor
import lightgbm as lgb


#Descriptions of the dataset used
train_df = pd.read_csv("/kaggle/input/new-york-city-taxi-fare-prediction/train.csv", nrows= 50000, parse_dates=["pickup_datetime"])
test_df = pd.read_csv('/kaggle/input/new-york-city-taxi-fare-prediction/test.csv', parse_dates=["pickup_datetime"])
train_df.head()
train_df.shape
train_df.info()
train_df.describe()
Spectral_palette = sns.color_palette("Spectral", 10)
sns.palplot(Spectral_palette)
train_df.head()


f, ax = plt.subplots(1,1, figsize=(8,6))
msno.bar(train_df, ax=ax, color=Spectral_palette[7])
plt.title('Null Values')
plt.show()


pd.DataFrame(train_df.isnull().sum(), columns=["Train Null Count"])

pd.DataFrame(test_df.isnull().sum(), columns=["Test Null Count"])


# Data Analysis with Visualization Before Preprocessing

train_df.head()



# total distance
train_df['total_distance'] = train_df.apply(lambda x: get_total_distance(x),axis=1)
test_df['total_distance'] = test_df.apply(lambda x: get_total_distance(x),axis=1)
train_df.head()



Spectral_palette



fig = plt.figure(figsize=(8,9))
for i in range(2):
    plt.subplot(2, 1, i+1)
    plt.title("Train Data index {} | Distance :{:.3f}".format(i, train_df['total_distance'][i]))
    plt.scatter(train_df['pickup_longitude'][i], train_df['pickup_latitude'][i], color=Spectral_palette[1], label="Pick up location")
    plt.scatter(train_df['dropoff_longitude'][i], train_df['dropoff_latitude'][i], color=Spectral_palette[-1], label="Drop off location")
    plt.plot([train_df['pickup_longitude'][i],train_df['dropoff_longitude'][i]],[train_df['pickup_latitude'][i],train_df['dropoff_latitude'][i]],'k:')
    plt.axis('off')
    plt.legend()
    
fig.text(0.05,0.95,"Length by pickup location and drop off location", fontweight="bold", fontfamily='serif', fontsize=20)
plt.show()



# Plot the latitude
f = px.scatter_3d(train_df[:10000], x='pickup_latitude', y='pickup_longitude', z='total_distance',
                    color='fare_amount')
f.show()


# Plot the longitude
f = px.scatter_3d(train_df[:10000], x='dropoff_latitude', y='dropoff_longitude', z='total_distance',
                    color='fare_amount')
f.show()



# Plot the each rows year
train_df['pickup_datetime_year'] = train_df['pickup_datetime'].dt.year
train_df.head()



# ploting ech row
train_df['pickup_datetime_year'] = train_df['pickup_datetime'].dt.year
train_df.head()



train_df['pickup_datetime_year'].value_counts()



fig, ax = plt.subplots(1,1, figsize=(6, 4), constrained_layout=True)

ax = sns.countplot(train_df['pickup_datetime_year'], palette=Spectral_palette)
ax.patch.set_alpha(0)
ax.set_xlabel("")
ax.set_ylabel("")
fig.text(0.08,1.03,"Count of data by year", fontweight="bold", fontfamily='serif', fontsize=18)
plt.show()




# plotinng histogram
df_index =[1,3,4,5,6,7]
fig = plt.figure(figsize=(10,8))

for num, i in enumerate(df_index):
    plt.subplot(3,2,num+1)
    plt.title("{} Column".format(train_df.columns[i]))
    plt.boxplot(train_df.iloc[:,i])

fig.text(0.08,0.94,"Boxplot the each columns", fontweight="bold", fontfamily='serif', fontsize=18)
plt.show()
df_index =[1,3,4,5,6,7]
fig = plt.figure(figsize=(12,8))

for num, i in enumerate(df_index):
    plt.subplot(2, 3,num+1)
    plt.title("{} Column".format(train_df.columns[i]))
    plt.hist(train_df.iloc[:,i], color=Spectral_palette[num])

fig.text(0.08,0.94,"Histogram the each columns", fontweight="bold", fontfamily='serif', fontsize=18)
plt.show()






df_index =[1,3,4,5,6,7]
fig = plt.figure(figsize=(14,10))

for num, i in enumerate(df_index):
    plt.subplot(2,3,num+1)
    plt.title("{} Column".format(train_df.columns[i]))
    sns.kdeplot(train_df.iloc[:,i], fill=True, lw=1.7, alpha=0.7, color=Spectral_palette[num+4])

fig.text(0.08,0.94,"KdePlot the each columns", fontweight="bold", fontfamily='serif', fontsize=18)
plt.show()






# Data preparation and preprocessing

# outliers
def data_cleansing(df, data="Train"):
    
    print("Before cleansing shape : {}".format(df.shape))
    print("----- CLEANSING -----")
    
    if data=="Train":
        df = df.drop(df[df['fare_amount'] <= 2].index)
        df = df.drop(df[df['fare_amount'] >= 100].index)
        print(df.shape)
    
    df = df.drop(df[df['pickup_longitude'] <= -74.5].index)
    df = df.drop(df[df['pickup_longitude'] >= -73.5].index)
    print(df.shape)
   
    df = df.drop(df[df['pickup_latitude'] <= 40.4].index)
    df = df.drop(df[df['pickup_latitude'] >= 41].index)
    print(df.shape)
   
    df = df.drop(df[df['dropoff_longitude'] <= -74.5].index)
    df = df.drop(df[df['dropoff_longitude'] >= -73.5].index)
    print(df.shape)
   
    df = df.drop(df[df['dropoff_latitude'] <= 40.4].index)
    df = df.drop(df[df['dropoff_latitude'] >= 41].index)
    print(df.shape)
       
    # No more than 7 passengers are allowed on board.
    df = df.drop(df[df['passenger_count'] <= 0].index)
    df = df.drop(df[df['passenger_count'] >= 7].index)
    
    print("----- CLEANSING -----")
    print("After cleansing shape : {}".format(df.shape))
    
    return df




train_df['fare_amount'].sort_values(ascending=False)



train_df = data_cleansing(train_df, "Train")




# Data Visualization

f = px.scatter_3d(train_df[:10000], x='pickup_latitude', y='pickup_longitude', z='total_distance',
                    color='fare_amount')
f.show()




f = px.scatter_3d(train_df[:10000], x='dropoff_latitude', y='dropoff_longitude', z='total_distance',
                    color='fare_amount')
f.show()




map_img = plt.imread('../input/google-map-nyc-40474541735-kor-version/google_map_NYC_(40.4-74.541-73.5)_KOR_VERSION.png')




plt.imshow(map_img)
plt.show()





def plot_map(df, map_img, s=10, alpha=0.2):
    f, ax = plt.subplots(1, 2, figsize=(16,8))
    ax[0].scatter(df.pickup_longitude, df.pickup_latitude, zorder=1, alpha=alpha, c='r', s=s)
    ax[0].set_xlim(-74.5, -73.5)
    ax[0].set_ylim((40.4, 41))
    ax[0].set_title('Pickup locations')
    ax[0].axis('off')
    ax[0].imshow(map_img, zorder=0, extent=(-74.5, -73.5, 40.4, 41))

    ax[1].scatter(df.dropoff_longitude, df.dropoff_latitude, zorder=1, alpha=alpha, c='r', s=s)
    ax[1].set_xlim(-74.5, -73.5)
    ax[1].set_ylim((40.4, 41))
    ax[1].set_title('Dropoff locations')
    ax[1].axes.xaxis.set_visible(False)
    ax[1].axes.yaxis.set_visible(False)
    ax[1].imshow(map_img, zorder=0, extent=(-74.5, -73.5, 40.4, 41))






plot_map(train_df[:1000], map_img)




# transformation/Data preparation
train_df.head()
train_df["year"] = train_df["pickup_datetime"].dt.year
train_df["weekday"] = train_df["pickup_datetime"].dt.weekday
train_df["hour"] = train_df["pickup_datetime"].dt.hour

test_df["year"] = test_df["pickup_datetime"].dt.year
test_df["weekday"] = test_df["pickup_datetime"].dt.weekday
test_df["hour"] = test_df["pickup_datetime"].dt.hour






train_df.head()



test_df.head()



train_df.drop(['key','pickup_datetime','pickup_datetime_year'], axis=1, inplace=True)
test_df.drop(['key','pickup_datetime'], axis=1, inplace=True)
train_df.head()
train_df.info()




# Model Development
x = train_df.drop('fare_amount', axis=1)
y = train_df['fare_amount']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
print("X train data shape : {}".format(x_train.shape))
print("Y train data shape : {}".format(y_train.shape))

print("X test data shape : {}".format(x_test.shape))
print("Y test data shape : {}".format(y_test.shape))
x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, test_size=0.6)
print("X validation data shape : {}".format(x_val.shape))
print("Y validation data shape : {}".format(y_val.shape))

print("X test data shape : {}".format(x_test.shape))
print("Y test data shape : {}".format(y_test.shape))





# training
train_data = lgb.Dataset(x_train, label=y_train)
val_data = lgb.Dataset(x_val, label=y_val)
params = {
    'n_estimators': 5000,
    'num_leaves': 500,
    'max_depth': -1,
    'min_data_in_leaf': 1000,
    'learning_rate': 0.003,
    'boosting': 'gbdt',
    'objective': 'regression',
    'metric': 'mse',
    'Is_training_metric': True,
    'n_jobs': -1
}
model = lgb.train(params,
                  train_data,
                  valid_sets=val_data, 
                  valid_names=['train','valid'],
                  early_stopping_rounds=100)



                  
# Model Evaluation/Validation
print('Starting predicting...')
# predict
y_pred = model.predict(x_test)
# eval
print('The rmse of prediction is:', mean_squared_error(y_test, y_pred))
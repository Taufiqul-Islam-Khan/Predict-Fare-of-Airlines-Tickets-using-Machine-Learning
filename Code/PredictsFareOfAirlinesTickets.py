"""Import all necessary Modules """
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt

#Read the dataset file
train_data=pd.read_excel('H:\Flight_Price\Data_Train.xlsx')
# print(train_data.head())

# see the missing values
# print(train_data.isna().sum())

# drop the mising value
train_data.dropna(inplace= True)
# print(train_data.isna().sum())

# change datatype
def change_into_dateTime(col):
    train_data[col]=pd.to_datetime(train_data[col])

# converting object datatype to datetime
for i in ['Date_of_Journey', 'Dep_Time','Arrival_Time']:
    change_into_dateTime(i)


# #making day month from dataframe
train_data['journey_day']=train_data['Date_of_Journey'].dt.day
train_data['journey_month']=train_data['Date_of_Journey'].dt.month

train_data.drop('Date_of_Journey',axis=1,inplace=True)

#extract hour
def extract_hour(df,col):
    df[col+'_hour']=df[col].dt.hour

#extract minute
def extract_min(df,col):
    df[col+'_minute']=df[col].dt.minute


#drop column
def drop_column(df,col):
    df.drop(col,axis=1,inplace=True)


extract_hour(train_data,'Dep_Time')
extract_min(train_data,'Dep_Time')
drop_column(train_data,'Dep_Time')


extract_hour(train_data,'Arrival_Time')
extract_min(train_data,'Arrival_Time')
drop_column(train_data,'Arrival_Time')


#if there is no hour included in the Duration then we should add 0h as wel as for minute we should add 0m
duration=list(train_data['Duration'])
for i in range(len(duration)):
    if len(duration[i].split( ))==2:
        pass
    else:
        if 'h' in duration[i]:
            duration[i]=duration[i]+' 0m'
        else:
            duration[i]='0h '+duration[i]

train_data['Duration']=duration
print(train_data['Duration'])

# fetch what can be the hour and minuite in the duration
def hour(x):
    return x.split(' ')[0][0:-1]

def minute(x):
    return x.split(' ')[1][0:-1]

train_data['Duration_hours']=train_data['Duration'].apply(hour)
train_data['Duration_mins']=train_data['Duration'].apply(minute)
drop_column(train_data,'Duration')
train_data['Duration_hours']=train_data['Duration_hours'].astype(int)
train_data['Duration_mins']=train_data['Duration_mins'].astype(int)
print(train_data.dtypes)

#catagorical data

cat_col=[col for col in train_data.columns if train_data[col].dtype== 'O']

#continues features
cont_col=[col for col in train_data.columns if train_data[col].dtype!= 'O']
print(cat_col)
print(cont_col)

#Handle categorical data and perform feature encoding in data

#Nominal Data ( data does not have any hirercy)--- onehot
categorical=train_data[cat_col]
print(categorical.head())

print(categorical['Airline'].value_counts())
plt.figure(figsize=(15,5))
sns.boxplot(x='Airline',y="Price",data=train_data.sort_values("Price",ascending=False))
# plt.show()
Airline=pd.get_dummies(categorical['Airline'],drop_first=True)
print(Airline.head())

#from vedio 6

#GET http://geodb-free-service.wirefreethought.com/v1/geo/cities
import json
# Импортируем библиотеку requests 
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



#import statsmodels
import scipy as sc

from scipy import stats
from scipy.stats import pearsonr


 
def get_parametr(data1):
    
    a1=[]
    for i in range (0,len(data1['data'])):
        dict1={}
        dict1['city']=data1['data'][i]['city']
        dict1['country']=data1['data'][i]['country']
        dict1['population']=data1['data'][i]['population']
        dict1['longitude']=data1['data'][i]['longitude']
        dict1['latitude']=data1['data'][i]['latitude']

        a1.append(dict1)

    return a1
 
 
def for_pandas(arr1):
    
    arr_city=[]
    arr_country=[]
    arr_population=[]
    arr_longitude=[]
    arr_latitude=[]
    for i in range (0,len(arr1)):
        
        arr_city.append(arr1[i]['city'])
        arr_country.append(arr1[i]['country'])
        arr_population.append(arr1[i]['population'])
        arr_longitude.append(arr1[i]['longitude'])
        arr_latitude.append(arr1[i]['latitude'])
 
 
    df = pd.DataFrame({
    'city': arr_city,
    'country': arr_country,
    'population': arr_population,
    'longitude': arr_longitude,
    'latitude': arr_latitude})

    return df
    
 

 
url = 'http://geodb-free-service.wirefreethought.com/v1/geo/cities'
 

k=0
v="а"
arr=[]
for i in range (1, 4):

    
    param = {
        "limit":5,
        "offset":k,
        "languageCode":"ru",
        }
        #"namePrefix":v
    k+=5
# Отправляем get request (запрос GET)
    response = requests.get(url,param)
    data1 = response.json()
    
 
    get_city=get_parametr(data1)

    arr+=get_city

 
p1=for_pandas(arr)
#print(p1)



xs = p1['city']
ys = p1['population']
pd.DataFrame(np.array([xs,ys]).T).plot.scatter(0, 1, s=20, grid=True)

plt.title('График отображения численности населения городов')
 
#поворот х-наименование
plt.xticks(rotation=60)
plt.subplots_adjust(left=0.125, bottom=0.3, right=0.9, top=0.88, wspace=0.2, hspace=0.2)

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 14
        }
 
plt.xlabel('Города',fontdict=font)
plt.ylabel('Население (млн)',fontdict=font)

plt.show()





#подсчет корреляции
print ("Зависимость количества населения от широты расположения города: \nЧем больше широта, тем меньше населения проживает в городе")

#t=pearsonr(p1['population'], p1['latitude'])
#print(t)

r = round(pearsonr(p1['population'], p1['latitude'])[0], 4)

print("Коэффициент корреляции Пирсона (r): "+ str(r))

p = round(pearsonr(p1['population'], p1['latitude'])[1], 4)

print("Двустороннее значение p: "+ str(p)) 


с1=0
if (r>0):
    print("1) Существует совершенно положительная линейная корреляция")
    с1=1
elif (r<0):
    print("1) Существует совершенно отрицательная линейная корреляция")
elif (r==0):
    print("1) Отсутствие линейной корреляции")


if (p<0.005):
    print("2) Cуществует статистически значимая связь между двумя переменными")
else:
    print("2) Cтатистически значимая связь отсутствует")

if (с1==1):
    print("Вывод: гипотеза подтверждена")
else:
    print("Вывод: гипотеза опровергнута")
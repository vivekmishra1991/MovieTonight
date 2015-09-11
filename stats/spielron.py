import pandas as pd
from collections import Counter
from math import *
import matplotlib.pyplot as plt
import operator
import matplotlib
from matplotlib.ft2font import FT2Font
from matplotlib.font_manager import FontProperties
import os

clust_data = [[0 for x in range(4)] for x in range(5)]
#Data Extraction 
df=pd.read_csv("input/imdb.csv")
li_genre=[list(df['genre'].values)[i].replace(',','').split() for i in range(len(df['genre'].values))]
li_genre=sum(li_genre,[])
summary_genre=(Counter(li_genre)).most_common(5)
summary_genre=map(list,summary_genre)
summary_genre=[elem[0] for elem in summary_genre ]


li_director=df['director'].values
summary_director=(Counter(li_director)).most_common(5)
summary_director=map(list,summary_director)
summary_director=[elem[0] for elem in summary_director ]

#summary_director_new=dict(sorted(summary_director.iteritems(),key=operator.itemgetter(1),reverse=True)[:5])


li_cast=[row.split(',') for row in df['actor']]
li_cast=sum(li_cast,[])
summary_actor=(Counter(li_cast)).most_common(5)
summary_actor=map(list,summary_actor)
summary_actor=[elem[0] for elem in summary_actor ]

#sorted(summary_actor,key=summary_actor.get,reverse=True)

#Normalzing factor(Z)
Z=[log(abs(val))/df.shape[0] for val in df['imdbVotes'] ]
imdbRatings=df['imdbRating']-1+Z

summary_imdbRatings={}
for ratings in imdbRatings:
    if(summary_imdbRatings.has_key(floor(ratings))):
        summary_imdbRatings.update({floor(ratings):summary_imdbRatings[floor(ratings)]+1})
    else:    
        summary_imdbRatings.update({floor(ratings):1})
	#sorted(summary_actor,key=summary_actor.get,reverse=True)


#Plotting methods



plt.figure(1)
#Pie Chart
plt.subplot(211)
plt.axis('equal')
plt.title('IMDB Ratings chart')
labels=summary_imdbRatings.keys()
sizes=summary_imdbRatings.values()
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','orange','green']
plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)


for i in range(5):
	clust_data[i][0]=i+1
	clust_data[i][1]=summary_genre[i]
	clust_data[i][2]=summary_actor[i]
	clust_data[i][3]=summary_director[i] 


plt.subplot(212)
colLabels=("#","Genre", "Actor","Director")
fontname = os.path.join(matplotlib.get_data_path(),
                            'fonts', 'ttf', 'cmr10.ttf')

font = FT2Font(fontname)
colors = [[(0.95, 0.95, 0.75) for c in range(4)] for r in range(5)]

the_table = plt.table(cellText=clust_data,cellColours=colors,
          colLabels=colLabels,
          loc='center')


for key, cell in the_table.get_celld().items():
    row, col = key
    if row > 0 and col > 0:
        cell.set_text_props(fontproperties=FontProperties(fname=fontname))

# cellDict=the_table.get_celld()
# [[cellDict[(r,c)].set_width(0.9) for c in range(4)] for r in range(5)]

# cellDict[(0,1)].set_width(0.2)
# cellDict[(0,0)].set_width(0.2)

axis=('off')



plt.show()


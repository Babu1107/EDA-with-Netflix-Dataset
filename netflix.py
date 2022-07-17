#!/usr/bin/env python
# coding: utf-8

# # Author : Babu Balasubramanian

# ## EDA on Netflix Dataset

# ###### Importing Libraries

# In[322]:


import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib as mpl
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import random
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go


# ###### Import Data

# In[323]:


df = pd.read_csv(r'D:\NETFLIX DATASET\netflix_titles.csv')


# In[324]:


df.head()


# In[325]:


df.tail()


# In[326]:


df.shape


# In[327]:


df.info()


# In[328]:


percent_missing = df.isnull().sum() * 100 / len(df)
percent_missing =percent_missing.round(2)
missing_count = df.isnull().sum()
missing_value_df = pd.DataFrame({'missing count': missing_count,
                                 'percent_missing': percent_missing})
final=missing_value_df.sort_values(by = 'missing count' , ascending = False).reset_index().rename(columns = {'index':'column_name'})


# In[329]:


final


# In[330]:


df['rating'].unique()


# In[331]:


df['rating'] = df['rating'].replace({
    '66 min' : 'TV-MA', 
    '74 min' : 'TV-MA', 
    '84 min' : 'TV-MA', 
    'TV-Y7-FV' : 'TV-Y7' })


# In[332]:


df['rating'].unique()


# In[333]:


df['rating'] =df['rating'].replace({
    'PG-13' : 'Suitable for ages 12 and up',
    'TV-MA' : 'Adults',
    'PG'    : 'Parental Guidance suggested',
    'TV-14' : 'Suitable for ages 14 and up',
    'TV-PG' : 'Parental Guidance suggested',
    'TV-Y'  : 'Kids',
    'TV-Y7' : 'Suitable for ages 7 and up',
    'R'     : 'Adults',
    'TV-G'  : 'Kids',
    'G'     : 'Kids',
    'NC-17' : 'Adults'
})


# In[334]:


df['rating'].unique()


# In[335]:


df.groupby('country')['country'].count().sort_values(ascending=False)


# In[336]:


df['country']=df['country'].fillna(df['country'].mode()[0])


# In[337]:


df.info()


# In[338]:


df['cast'].replace(np.nan, 'No Data', inplace =True)
df['director'].replace(np.nan, 'No Data', inplace = True)
df.dropna(inplace =True)
df.drop_duplicates(inplace =True)


# In[339]:


df['date_added'] = pd.to_datetime(df['date_added'])


# ###### ANALYSIS:

# In[340]:


tot_count= df.groupby(['show_id'])['show_id'].count().sum()
tot_count

fig8 = go.Figure()
fig8.add_trace(go.Indicator( value = tot_count))

fig8 = fig8.update_layout(
        template = { 'data' : {'indicator': [{
        'title': {'text': 'Total Content on Netflix'} ,}] 
                   }})
fig8.update_layout(margin=dict(l=50, r=50, b=0, t=30), showlegend=False,

plot_bgcolor='#333', paper_bgcolor='#333', title_x = 0.5,

title_font=dict(size=25, color='#D81F26', family="Lato, sans-serif",
         ),

font=dict(size=45, color='#D81F26'),

hoverlabel=dict(bgcolor="#444", font_size=45,

font_family="Lato, sans-serif"))

fig8.show()


# In[341]:



x=df["type"].value_counts().reset_index()

fig_donut1 = px.pie(x, names='index',  values="type", 

color_discrete_sequence=['#D81F26', '#FC757A'])

fig_donut1.update_traces(hovertemplate=None, textposition='outside',

textinfo='percent+label', rotation=180)

fig_donut1.update_layout(margin=dict(t=60, b=30, l=0, r=0), showlegend=True,

plot_bgcolor='#333', paper_bgcolor='#333', title_text='Type of Content Uploaded More on Netflix',title_x=0.5,

title_font=dict(size=25, color='#e6e6e6', family="Lato, sans-serif"),

font=dict(size=17, color='#8a8d93'),

hoverlabel=dict(bgcolor="#444", font_size=13,

font_family="Lato, sans-serif"))


# In[342]:


mcm = df.groupby(['rating'])['title'].count().reset_index().sort_values('title', ascending = False)
y=mcm['title']
x=mcm['rating']

fig50=px.bar(mcm,x=x,y=y, template = "plotly_dark")
fig50.update_traces(marker_color='#D81F26')
fig50.update_layout(margin=dict(t=45, b=30, l=0, r=0), showlegend=False,

plot_bgcolor='#333', paper_bgcolor='#333',title_text='Category Which Has Uploaded More Content', title_x = 0.5,

title_font=dict(size=25, color='#e6e6e6', family="Lato, sans-serif",
         ),

font=dict(size=17, color='#8a8d93'),

hoverlabel=dict(bgcolor="#444", font_size=13,

font_family="Lato, sans-serif"))


fig50.show()


# In[343]:


df_5 = df.query('release_year >= 2007')
df_5 = df_5.groupby(['release_year'])['show_id'].count().reset_index()
fig10 = px.area(df_5, x = 'release_year', y ='show_id', template = "plotly_dark" )

fig10.update_layout(margin=dict(t=60, b=30, l=0, r=0), showlegend=False,

plot_bgcolor='#333', paper_bgcolor='#333',title_text='Over All Content Release Trend', title_x = 0.5,

title_font=dict(size=25, color='#e6e6e6', family="Lato, sans-serif",
         ),

font=dict(size=17, color='#8a8d93'),

hoverlabel=dict(bgcolor="#444", font_size=13,

font_family="Lato, sans-serif"))

fig10.show()


# In[344]:


df_9 = df.query("type == 'TV Show'")
df_9 = df_9[['title', 'duration']]
df_9 = df_9.groupby(['duration'])['title'].count().reset_index().sort_values('title', ascending = False)
df_9 = df_9.rename(columns = {"title" : "TV Shows" , "duration" : "Seasons"})
df_9

fig10 = px.histogram(
    df_9,
    x="Seasons",
    y="TV Shows",
    barmode="overlay",
    template = "plotly_dark",
    color_discrete_sequence=['indianred'],
)


fig10.update_layout(margin=dict(t=60, b=30, l=0, r=0), showlegend=False,

plot_bgcolor='#333', paper_bgcolor='#333',title_text='TV Shows Seasons', title_x = 0.5,

title_font=dict(size=25, color='#e6e6e6', family="Lato, sans-serif",
         ),

font=dict(size=17, color='#8a8d93'),

hoverlabel=dict(bgcolor="#444", font_size=13,

font_family="Lato, sans-serif"))

fig10.show()


# In[345]:


df_4 =df.query('release_year >= 2007')
df_4= df_4.groupby(['type', 'release_year'])['show_id'].count().reset_index()
df_4_movie = df_4.query("type == 'Movie'")
df_4_tvshow = df_4.query("type == 'TV Show'")
mshowid = df_4_movie['show_id']
tvshowid = df_4_tvshow['show_id']
releaseyear = df_4_tvshow['release_year']

fig11 = go.Figure(data=[
    go.Bar(name='Movie', x=releaseyear, y=mshowid),
    go.Bar(name='TV Show', x=releaseyear, y=tvshowid)
])

fig11.update_layout(margin=dict(t=60, b=30, l=0, r=0), showlegend=False,template = "plotly_dark",

plot_bgcolor='#333', paper_bgcolor='#333',title_text='Content Added Over Years', title_x = 0.5,

title_font=dict(size=25, color='#e6e6e6', family="Lato, sans-serif", 
         ),

font=dict(size=17, color='#8a8d93'),

hoverlabel=dict(bgcolor="#444", font_size=13,

font_family="Lato, sans-serif"))

fig11.show()


# In[346]:


filtered_directors=df[df["type"] == "Movie"]
filtered_directors=filtered_directors[filtered_directors["country"] == "India"]
filtered_directors=filtered_directors['director'].str.split(',',expand=True).stack()
filtered_directors=filtered_directors.to_frame()
filtered_directors.columns=['Director']
directors=filtered_directors.groupby(['Director']).size().reset_index(name='Total Content')
directors=directors[directors.Director !='No Data']
directors=directors.sort_values(by=['Total Content'],ascending=False)
directorsTop10=directors.head(10)
directorsTop10=directorsTop10.sort_values(by=['Total Content'])
fig0=px.bar(directorsTop10,x='Total Content',y='Director', template = "plotly_dark" )

fig0.update_layout(margin=dict(t=60, b=30, l=0, r=0), showlegend=False,

plot_bgcolor='#333', paper_bgcolor='#333',title_text='Top 10 Movie Directors From India With Most Content', title_x = 0.5,

title_font=dict(size=25, color='#e6e6e6', family="Lato, sans-serif",
         ),

font=dict(size=17, color='#8a8d93'),

hoverlabel=dict(bgcolor="#444", font_size=13,

font_family="Lato, sans-serif"))


fig0.show()


# In[347]:


filtered_directors=df[df["type"] == "Movie"]
filtered_directors=filtered_directors[filtered_directors["country"] == "United States"]
filtered_directors=filtered_directors['director'].str.split(',',expand=True).stack()
filtered_directors=filtered_directors.to_frame()
filtered_directors.columns=['Director']
directors=filtered_directors.groupby(['Director']).size().reset_index(name='Total Content')
directors=directors[directors.Director !='No Data']
directors=directors.sort_values(by=['Total Content'],ascending=False)
directorsTop10=directors.head(10)
directorsTop10=directorsTop10.sort_values(by=['Total Content'])
fig1=px.bar(directorsTop10,x='Total Content',y='Director',template = "plotly_dark")


fig1.update_layout(margin=dict(t=60, b=30, l=0, r=0), showlegend=False, 

plot_bgcolor='#333', paper_bgcolor='#333',title_text='Top 10 Movie Directors From US With Most Content', title_x = 0.5,

title_font=dict(size=25, color='#e6e6e6', family="Lato, sans-serif",
         ),

font=dict(size=17, color='#8a8d93'),

hoverlabel=dict(bgcolor="#444", font_size=13,

font_family="Lato, sans-serif"))
                   
                   
                   
fig1.show()


# In[348]:


filtered_cast=df[df["type"] == "Movie"]
filtered_cast=filtered_cast[filtered_cast["country"] == "India"]
#filtered_cast=pd.DataFrame()
filtered_cast=df['cast'].str.split(',',expand=True).stack()
filtered_cast=filtered_cast.to_frame()
filtered_cast.columns=['Actor']
actors=filtered_cast.groupby(['Actor']).size().reset_index(name='Total Content')
actors=actors[actors.Actor !='No Data']
actors=actors.sort_values(by=['Total Content'],ascending=False)
actorsTop10=actors.head(10)
actorsTop10=actorsTop10.sort_values(by=['Total Content'])
fig2=px.bar(actorsTop10,x='Total Content',y='Actor', template = "plotly_dark" )

fig2.update_layout(margin=dict(t=60, b=30, l=0, r=0), showlegend=False,

plot_bgcolor='#333', paper_bgcolor='#333',title_text='Top 10 Actors From India On Netflix',title_x=0.5,

title_font=dict(size=25, color='#e6e6e6', family="Lato, sans-serif",
         ),

font=dict(size=17, color='#8a8d93'),

hoverlabel=dict(bgcolor="#444", font_size=13,

font_family="Lato, sans-serif"))


fig2.show()


# In[349]:


def red_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(351, 99%%, %s%%)" % random.randint(60, 100)

imovies=df[df["type"] == "Movie"]
imovies=imovies[imovies["country"] == "India"]
imovies=imovies["title"]
text = str(list(imovies)).replace(',', '').replace('[', '').replace("'", '').replace(']', '').replace('.', '')
mask = np.array(Image.open(r'C:\Users\dell\Desktop\mask.png'))
wordcloud = WordCloud(background_color = '#333',  height = 200, max_words = 250, mask = mask).generate(text)
plt.figure( figsize=(10,50))
plt.imshow(wordcloud.recolor(color_func=red_color_func, random_state=3),
           interpolation="bilinear")
plt.axis('off')
plt.tight_layout(pad=0)
plt.title("Indian Movie Names Occurance", size=25, color='#e6e6e6', family="Lato, sans-serif",  backgroundcolor= '#333')
plt.show()


# In[ ]:





# In[350]:


fig_donut = px.pie(df, names='type',  hole=0.7,

color_discrete_sequence=['#D81F26', '#221f1f'])

fig_donut.update_traces(hovertemplate=None, textposition='outside',

textinfo='percent+label', rotation=90)

fig_donut.update_layout(margin=dict(t=60, b=30, l=0, r=0), showlegend=True,

plot_bgcolor='#333', paper_bgcolor='#333', title_text='Type of Content Uploaded More on Netflix',title_x=0.5,

title_font=dict(size=25, color='#e6e6e6', family="Lato, sans-serif"),

font=dict(size=17, color='#8a8d93'),

hoverlabel=dict(bgcolor="#444", font_size=13,

font_family="Lato, sans-serif"))


# In[ ]:





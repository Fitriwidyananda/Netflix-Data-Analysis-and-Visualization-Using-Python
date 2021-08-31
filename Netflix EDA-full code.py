#!/usr/bin/env python
# coding: utf-8

# In[15]:


#Importing Libraries
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, iplot
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


#Loading the Dataset
netflix = pd.read_csv("NetflixData.csv")


# In[4]:


#The first 3 rows of the dataset
netflix.head(3)


# In[5]:


#Checking shape of the dataset
netflix.shape


# In[6]:


#Checking columns of the dataset
netflix.columns


# In[7]:


#Checking information of the dataset
netflix.info()


# In[8]:


#Checking null value of the dataset
netflix.isnull().sum()


# In[9]:


#Imputing missing values
netflix.cast.fillna("cast unavailable", inplace=True)
netflix.production_country.fillna("production country unavailable", inplace=True)
netflix.director.fillna("director unavailable", inplace=True)


# In[10]:


#Dropping missing values
netflix.dropna(subset=["release_date", "rating", "duration", "imdb_score"], inplace=True)
netflix.drop(["date_added"], axis=1, inplace=True)


# In[11]:


#Converting data type
netflix['imdb_score'] = netflix['imdb_score'].str.replace('/10', '')
netflix['imdb_score'] = netflix['imdb_score'].apply(pd.to_numeric)
netflix = netflix.rename(columns={'release_date':'release_year'})
netflix['release_year'] = netflix['release_year'].astype(int)


# In[12]:


#Data information
netflix.info()


# In[13]:


#Top 10 Content Producing Countries
Countries = netflix.set_index('title').production_country.str.split(', ', expand=True).stack().reset_index(level=1, drop=True);
Countries = Countries[Countries != 'production country unavailable']
plt.figure(figsize=(10,8))
g = sns.countplot(x = Countries, order=Countries.value_counts().index[:10], palette='dark:salmon')
plt.title('Top 10 Content Producing Countries', fontsize=21)
plt.xlabel('Country')
plt.ylabel('Titles')
plt.show()


# In[16]:


#Distribution Map of Producing Countries
countries = netflix.set_index('title').production_country.str.split(', ', expand=True).stack().reset_index(level=1, drop=True);
countries = countries[countries != 'production country unavailable']

iplot([go.Choropleth(
    locationmode='country names',
    locations=countries,
    z=countries.value_counts()
)])


# In[17]:


#Number of Content Titles by Rating
plt.figure(figsize=(10, 8))
sns.countplot(y='rating', data=netflix, order=netflix.rating.value_counts().index.to_list(), palette='dark:salmon_r')
plt.title('Number of Content Titles by Rating', fontsize=21);


# In[21]:


#Top 10 Genres with the Largest Number of Content Titles
top_genres = netflix.set_index('title').genres.str.split(', ', expand=True).stack().reset_index(level=1, drop=True)
plt.figure(figsize=(10, 10))
sns.countplot(y=top_genres, order=top_genres.value_counts().index.to_list()[:10], palette='Greens_r', saturation=.4)
plt.title('Top 10 Genres with the Largest Number of Content Titles', fontsize=21);


# In[22]:


#Ratings for Movies & TV Shows
order =  ['G', 'TV-Y', 'TV-G', 'PG', 'TV-Y7', 'TV-Y7-FV', 'TV-PG', 'PG-13', 'TV-14', 'R', 'NC-17', 'TV-MA']
plt.figure(figsize=(20,10))
g = sns.countplot(netflix.rating, hue=netflix.content_type, order=order, palette="copper");
plt.title("Ratings for Movies & TV Shows", fontsize=30)
plt.xlabel("Rating")
plt.ylabel("Total Count")
plt.show()


# In[24]:


#Comparison of Ratings in the US and Indonesia
US = netflix[netflix.production_country == "United States"]
order =  ['G', 'TV-Y', 'TV-G', 'PG', 'TV-Y7', 'TV-Y7-FV', 'TV-PG', 'PG-13', 'TV-14', 'R', 'NC-17', 'TV-MA']
plt.figure(figsize=(8,8))
g = sns.countplot(US.rating, hue=US.content_type, order=order, palette="dark:brown");
plt.title("Ratings for Movies & TV Shows in US")
plt.xlabel("Rating")
plt.ylabel("Total Count")
plt.show()

IND = netflix[netflix.production_country == "Indonesia"]
order =  ['G', 'TV-Y', 'TV-G', 'PG', 'TV-Y7', 'TV-Y7-FV', 'TV-PG', 'PG-13', 'TV-14', 'R', 'NC-17', 'TV-MA']
plt.figure(figsize=(8,8))
g = sns.countplot(IND.rating, hue=IND .content_type, order=order, palette="dark:brown");
plt.title("Ratings for Movies & TV Shows in Indonesia")
plt.xlabel("Rating")
plt.ylabel("Total Count")
plt.show()


# In[25]:


#The Number of Content Titles in the Last 10 Years
plt.figure(figsize=(10,8))
netflix_year = netflix['release_year'].value_counts()
netflix_year = pd.DataFrame(netflix_year).reset_index()
netflix_year.columns = ['release_year','title']
sns.barplot(x = 'release_year',y = 'title', data=netflix_year.head(10), saturation=.3)
plt.title('The Number of Content Titles in the Last 10 Years', fontsize=21);


# In[26]:


#Top 10 Actors by Number of Titles
plt.figure(figsize=(10,8))
netflix_cast = netflix[netflix.cast != 'cast unavailable'].set_index('title').cast.str.split(', ', expand=True).stack().reset_index(level=1, drop=True)
sns.countplot(y = netflix_cast, order=netflix_cast.value_counts().index[:10], palette='magma_r', saturation=.2)
plt.title('Top 10 Actors by Number of Titles', fontsize=21);
plt.show()


# In[27]:


#Top 5 Durations Based on The Number of Titles
plt.figure(figsize=(10,8))
netflix_duration = netflix['duration'].value_counts()
netflix_duration = pd.DataFrame(netflix_duration).reset_index()
netflix_duration.columns = ['duration','title']
sns.barplot(x = 'duration',y = 'title', data=netflix_duration.head(5), palette="cividis_r")
plt.title('Top 5 Durations Based on The Number of Titles', fontsize=21);


# In[28]:


#Percentation of Netflix Content Types
plt.figure(figsize=(12,8))
plt.title("The Percentage of Content Types ", fontsize=21)
g = plt.pie(netflix.content_type.value_counts(),explode=(0.025,0.025), labels=netflix.content_type.value_counts().index, colors=['salmon','grey'],  autopct='%1.1f%%', startangle=180)
plt.show()


# In[29]:


#Top 10 Imdb Scores
plt.figure(figsize=(10, 8))
sns.countplot(y='imdb_score', data=netflix, order=netflix.imdb_score.value_counts().index[:10], palette='Wistia', saturation=.2)
plt.title('Top 10 Imdb Scores', fontsize=21);


# In[30]:


#Top 5 Directors
plt.figure(figsize=(10,8))
netflix_directors = netflix[netflix.director != 'director unavailable'].set_index('title').director.str.split(', ', expand=True).stack().reset_index(level=1, drop=True)
sns.countplot(x = netflix_directors, order=netflix_directors.value_counts().index[:5], palette='crest', saturation=.2)
plt.title('Top 5 Directors', fontsize=21)
plt.show()


# In[ ]:





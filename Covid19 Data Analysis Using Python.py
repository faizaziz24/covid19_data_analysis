#!/usr/bin/env python
# coding: utf-8

# # Welcome to the Notebook

# ### Importing modules

# ### Task 1

# In[1]:


import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt


# ### Task 1.1: 
# #### Loading the Dataset

# In[2]:


dataset_url='https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
df = pd.read_csv(dataset_url)


# ### Task 1.2:
# #### let's check the dataframe 

# In[3]:


df.head()


# In[20]:


df.tail()


# In[21]:


df.shape


# ### Task 2.1 :
# #### let's do some preprocessing 

# In[22]:


df = df[df.Confirmed > 0]


# In[23]:


df.head()


# #### let's see data related to a country for example Indonesia 
# 

# In[24]:


df[df.Country == 'Indonesia']


# #### let's see Global spread of Covid19

# In[25]:


fig = px.choropleth(df, locations = 'Country', locationmode = 'country names', color = 'Confirmed', animation_frame = 'Date')
fig.update_layout(title_text='Global Spread of COVID-19')
fig.show()


# ### Task 2.2 : Exercise 
# #### Let's see Global deaths of Covid19

# In[26]:


fig = px.choropleth(df, locations = 'Country', locationmode = 'country names', color = 'Deaths', animation_frame = 'Date')
fig.update_layout(title_text='Global Deaths of COVID-19')
fig.show()


# ### Task 3.1:
# #### Let's Visualize how intensive the Covid19 Transmission has been in each of the country
# let's start with an example:

# In[27]:


df_china = df[df.Country =='China']
df_china.head()


# let's select the columns that we need

# In[28]:


df_china = df_china[['Date', 'Confirmed']]


# In[29]:


df_china.head()


# calculating the first derivation of confrimed column

# In[30]:


df_china['Infection Rate'] = df_china['Confirmed'].diff()


# In[31]:


df_china.head()


# In[32]:


px.line(df_china, x = 'Date', y = ['Confirmed', 'Infection Rate'])


# In[33]:


df_china['Infection Rate'].max()


# ### Task 3.2:
# #### Let's Calculate Maximum infection rate for all of the countries

# In[37]:


df.head()


# In[45]:


countries = list(df['Country'].unique())
max_infection_rates = []
for c in countries :
    MIR = df[df.Country == c].Confirmed.diff().max()
    max_infection_rates.append(MIR)
print(max_infection_rates)


# ### Task 3.3:
# #### let's create a new Dataframe 

# In[46]:


df_MIR = pd.DataFrame()
df_MIR['Country'] = countries
df_MIR['Max Infection Rate'] = max_infection_rates
df_MIR.head()


# #### Let's plot the barchart : maximum infection rate of each country

# In[54]:


px.bar(df_MIR, x = 'Country', y = 'Max Infection Rate', color = 'Country', title = 'Global Maximum Infection Rate', log_y = True)


# ### Task 4: Let's See how National Lockdowns Impacts Covid19 transmission in Italy
# ### COVID19 pandemic lockdown in Italy 
# On 9 March 2020, the government of Italy under Prime Minister Giuseppe Conte imposed a national quarantine, restricting the movement of the population except for necessity, work, and health circumstances, in response to the growing pandemic of COVID-19 in the country. <a href="https://en.wikipedia.org/wiki/COVID-19_pandemic_lockdown_in_Italy#:~:text=On%209%20March%202020%2C%20the,COVID%2D19%20in%20the%20country.">source</a>

# In[49]:


italy_lockdown_start_date = '2020-03-09'
italy_lockdown_a_month_later = '2020-04-09'


# In[53]:


df.head()


# let's get data related to italy

# In[42]:


df_italy = df[df.Country == 'Italy']


# let's check the dataframe 

# In[61]:


df_italy.head()


# let's calculate the infection rate in Italy

# In[84]:


df_italy['Infection Rate'] = df_italy.Confirmed.diff()
df_italy.head()


# ok! now let's do the visualization

# In[74]:


fig = px.line(df_italy, x = 'Date', y = 'Infection Rate', title = 'Before and After lockdown in Italy')
fig.add_shape(
    dict(
        type = 'line',
        x0 = italy_lockdown_start_date,
        y0 = 0,
        x1 = italy_lockdown_start_date,
        y1 = df_italy['Infection Rate'].max(),
        line = dict(color = 'red', width = 2)
    )
)
fig.add_annotation(
    dict(
        x = italy_lockdown_start_date,
        y = df_italy['Infection Rate'].max(),
        text = "Starting date of the lockdown"
    )
)
fig.add_shape(
    dict(
        type = 'line',
        x0 = italy_lockdown_a_month_later,
        y0 = 0,
        x1 = italy_lockdown_a_month_later,
        y1 = df_italy['Infection Rate'].max(),
        line = dict(color = 'yellow', width = 2)
    )
)
fig.add_annotation(
    dict(
        x = italy_lockdown_a_month_later,
        y = 0,
        text = "a month later"
    )
)


# ### Task 5: Let's See how National Lockdowns Impacts Covid19 deaths rate in Italy

# In[75]:


df_italy.head()


# let's calculate the deaths rate

# In[90]:


df_italy['Deaths Rate'] = df_italy.Deaths.diff()


# let's check the dataframe again

# In[78]:


df_italy.head()


# now let's plot a line chart to compare COVID19 national lockdowns impacts on spread of the virus and number of active cases

# In[91]:


fig = px.line(df_italy, x = 'Date', y = ['Infection Rate', 'Deaths Rate'], title = 'Deaths rate in Italy')
fig.show()


# let's normalize the columns

# In[92]:


df_italy['Infection Rate'] = df_italy['Infection Rate']/df_italy['Infection Rate'].max()
df_italy['Deaths Rate'] = df_italy['Deaths Rate']/df_italy['Deaths Rate'].max()


# let's plot the line chart again

# In[43]:


fig = px.line(df_italy, x = 'Date', y = ['Infection Rate', 'Deaths Rate'])
fig.add_shape(
    dict(
        type = 'line',
        x0 = italy_lockdown_start_date,
        y0 = 0,
        x1 = italy_lockdown_start_date,
        y1 = df_italy['Infection Rate'].max(),
        line = dict(color = 'red', width = 2)
    )
)
fig.add_annotation(
    dict(
        x = italy_lockdown_start_date,
        y = df_italy['Infection Rate'].max(),
        text = "Starting date of the lockdown"
    )
)
fig.add_shape(
    dict(
        type = 'line',
        x0 = italy_lockdown_a_month_later,
        y0 = 0,
        x1 = italy_lockdown_a_month_later,
        y1 = df_italy['Infection Rate'].max(),
        line = dict(color = 'yellow', width = 2)
    )
)
fig.add_annotation(
    dict(
        x = italy_lockdown_a_month_later,
        y = 0,
        text = "a month later"
    )
)


# ### COVID19 pandemic lockdown in Germany 
# Lockdown was started in Freiburg, Baden-Württemberg and Bavaria on 20 March 2020. Three days later, it was expanded to the whole of Germany

# In[22]:


Germany_lockdown_start_date = '2020-03-23' 
Germany_lockdown_a_month_later = '2020-04-23'


# let's select the data related to Germany

# In[23]:


df_germany = df[df.Country == 'Germany']


# let's check the dataframe 

# In[24]:


df_germany.head()


# selecting the needed column

# In[49]:


df_germany['Infection Rate'] = df.Confirmed.diff()
df_germany['Deaths Rate'] = df.Deaths.diff()


# let's check it again

# In[50]:


df_germany.head()


# let's calculate the infection and deaths rate in Germany

# In[51]:


df_germany['Infection Rate'] = df_germany['Infection Rate']/df_germany['Infection Rate'].max()
df_germany['Deaths Rate'] = df_germany['Deaths Rate']/df_germany['Deaths Rate'].max()


# let's check the dataframe

# In[46]:


df_germany.head()


# now let's do some scaling and plot the line chart

# In[47]:


fig = px.line(df_germany, x = 'Date', y = ['Infection Rate', 'Deaths Rate'], title = 'Start deaths rate in Germany')


# In[48]:


fig.add_shape(
    dict(
        type = 'line',
        x0 = Germany_lockdown_start_date,
        y0 = 0,
        x1 = Germany_lockdown_start_date,
        y1 = df_germany['Infection Rate'].max(),
        line = dict(color = 'red', width = 2)
    )
)
fig.add_annotation(
    dict(
        x = Germany_lockdown_start_date,
        y = df_germany['Infection Rate'].max(),
        text = "Starting date of the lockdown"
    )
)
fig.add_shape(
    dict(
        type = 'line',
        x0 = Germany_lockdown_a_month_later,
        y0 = 0,
        x1 = Germany_lockdown_a_month_later,
        y1 = df_germany['Infection Rate'].max(),
        line = dict(color = 'yellow', width = 2)
    )
)
fig.add_annotation(
    dict(
        x = Germany_lockdown_a_month_later,
        y = 0,
        text = "a month later"
    )
)


#!/usr/bin/env python
# coding: utf-8

# # Sleep, Health and Lifestyle Data Visualization
# ### DTSA 5304 Final Project
# 
# As a brief overview of this project, we will be taking a look at a dataset that includes information on individuals' demographics and lifestyle and seeing how those variables influence sleep quality and duration. This dataset can be found here: https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset
# 
# Here are some tasks of interest:
# - Explore how different lifestyle/demographic factors are associated with sleep quality and duration
# - Use these outcomes to see if there are potentially things one can do to improve sleep quality and duration
# 
# Here is a quick overview of what this data looks like:

# In[1]:


import pandas as pd
import altair as alt
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("SHLS.csv", encoding="ANSI")
df['Sleep Disorder'] = df['Sleep Disorder'].fillna('None')
df['BMI Category'] = df['BMI Category'].replace('Normal Weight', 'Underweight')
df = df.drop(['Blood Pressure'], axis = 1)
df.head()


# ### Variables
# 
# Here is a list of variables and descriptions per the overview on Kaggle:
# 
# **Person ID**: An identifier for each individual.
# 
# **Gender**: The gender of the person (Male/Female).
# 
# **Age**: The age of the person in years.
# 
# **Occupation**: The occupation or profession of the person.
# 
# **Sleep Duration (hours)**: The number of hours the person sleeps per day.
# 
# **Quality of Sleep (scale: 1-10)**: A subjective rating of the quality of sleep, ranging from 1 to 10.
# 
# **Physical Activity Level (minutes/day)**: The number of minutes the person engages in physical activity daily.
# 
# **Stress Level (scale: 1-10)**: A subjective rating of the stress level experienced by the person, ranging from 1 to 10.
# 
# **BMI Category**: The BMI category of the person (e.g., Underweight, Normal, Overweight).
# 
# **Heart Rate (bpm)**: The resting heart rate of the person in beats per minute.
# 
# **Daily Steps**: The number of steps the person takes per day.
# 
# **Sleep Disorder**: The presence or absence of a sleep disorder in the person (None, Insomnia, Sleep Apnea).
# 
# ### Sleep Duration and Quality Histogram
# 
# For this visualization, we chose to present a histogram of the mean sleep quality and mean sleep duration against various categorical variables. This provides the user with a quick overview of which demographic/lifestyle categories appear to, on average, have the most impact on sleep. 
# 
# ***Use the dropdown menu to select a category.***

# In[3]:


base =  alt.Chart(df)

bind_options2 = [None, "Gender", "Occupation", "BMI Category", "Sleep Disorder"]
dropdown2 = alt.binding_select(options=bind_options2, name="Select a value:", )
selection3 = alt.selection_single(fields=['column'], bind=dropdown2)

qualitybar = base.properties(width = 250, height = 250).transform_fold(
    ["Gender", "Occupation", "BMI Category", "Sleep Disorder"],
    as_=['column', 'value']
).add_selection(
    selection3
).transform_filter(
    selection3
).mark_bar().encode(
    x = "mean(Sleep Duration)",
    y = alt.Y(field = "value", type='nominal', sort=alt.EncodingSortField(field='Quality of Sleep', op='mean')),
    tooltip = ["value:N", "mean(Sleep Duration)", "count()"]
)

durationbar = base.properties(width = 250, height = 250).transform_fold(
    ["Gender", "Occupation", "BMI Category", "Sleep Disorder"],
    as_=['column', 'value']
).add_selection(
    selection3
).transform_filter(
    selection3
).mark_bar().encode(
    x = "mean(Sleep Duration)",
    y = alt.Y(field = "value", type='nominal', sort=alt.EncodingSortField(field='Quality of Sleep', op='mean')),
    tooltip = ["value:N", "mean(Quality of Sleep)", "count()"]
)

qualitybar | durationbar


# ### Sleep Duration v. Sleep Quality by Sleep Disorder
# 
# To expand on the previous visualization, we plot sleep quality against duration, categorized by sleep disorder. This can be expanded to other categories in later revisions, but we chose sleep disorder as it has a fairly salient impact on sleep quality and duration.
# 
# ***Click on the legend to filter results.***

# In[4]:


xscale = alt.Scale(domain=(4, 9))
yscale = alt.Scale(domain=(5.5, 8.5))

selection = alt.selection_single(fields=['Sleep Disorder'], bind='legend')

bar_args = {'opacity': .3, 'binSpacing': 0}

plot1 = base.mark_circle().encode(
    y = alt.Y("Quality of Sleep", title = 'Sleep Quality', scale = xscale),
    x = alt.X("Sleep Duration", scale = yscale),
    color = "Sleep Disorder",
    tooltip = ["Person ID", "Gender", "Age", "Occupation", "Sleep Disorder"],
).add_selection(
    selection
).transform_filter(
    selection
)


top_hist = alt.Chart(df).mark_bar(**bar_args).encode(
    x = alt.X("Sleep Duration", bin=alt.Bin(maxbins=6, extent=yscale.domain), stack = None, title = ''), 
    y = alt.Y("count()", stack=None, title=''),
    color = alt.Color("Sleep Disorder")
).properties(height=60).add_selection(
    selection
).transform_filter(
    selection
)


right_hist = alt.Chart(df).mark_bar(**bar_args).encode(
    y = alt.Y("Quality of Sleep", bin=alt.Bin(maxbins=6, extent=xscale.domain), stack = None, title = ''), 
    x = alt.X("count()", stack=None, title=''),
    color = alt.Color("Sleep Disorder")
).properties(width=60).add_selection(
    selection
).transform_filter(
    selection
)

top_hist & (plot1 | right_hist)


# ### Sleep Duration Visualization
# 
# For this visualization, we look at how different numerical variables plot against sleep duration. In the last visualtion, we showed a clear positive relationship between sleep duration and quality, and wanted to examine if there exists similar relationships between sleep duration and other variables. We chose sleep duration as the dependent variable in this case as its a more granular measurement than sleep quality and thus easier to visualize via scatterplot - this can be explored in further revisions.
# 
# ***Click on the legend to filter results.***

# In[5]:


bind_options = ["Age", "Physical Activity Level", "Stress Level", "Heart Rate", "Daily Steps"]
dropdown = alt.binding_select(options=bind_options, name="Select an x-variable:")

selection2 = alt.selection_single(fields=['column'], bind=dropdown)

plot2 = base.properties(width = 250, height = 250).transform_fold(
    ["Age", "Physical Activity Level", "Stress Level", "Heart Rate", "Daily Steps"],
    as_=['column', 'value']
).mark_circle().encode(
    x = alt.X("value:Q", title = '', scale = alt.Scale(zero = False)),
    y = alt.Y("Sleep Duration:Q", scale = alt.Scale(zero = False)),
    color = "Sleep Disorder:N",
    tooltip = ["Person ID", "Gender", "Age", "Occupation", "value:Q"]
).add_selection(
    selection2
).transform_filter(
    selection2
).add_selection(
    selection
).transform_filter(
    selection
)

hist = base.properties(width = 250, height = 250).transform_fold(
    ["Age", "Physical Activity Level", "Stress Level", "Heart Rate", "Daily Steps"],
    as_=['column', 'value']
).mark_bar().encode(
    x = alt.X("value:Q", bin = alt.Bin(maxbins=6), title = ''),
    y = "count()",
    color = "Sleep Disorder:N",
    tooltip = ['value:Q', 'count()'],
).add_selection(
    selection2
).transform_filter(
    selection2
).add_selection(
    selection
).transform_filter(
    selection
)

plot2 | hist


# ### Evaluation
# 
# We chose to evaluate this project via thinkalouds, as we wanted to focus on qualitative, summative insights to evaluate our tool. That is, we seek to determine if our tool is effective at showing relationships between sleep and lifestyle factors for an average user - particularly that the tool is easy to use, understand, and gain insights from.
# 
# **Person 1:**
#    * Thinkaloud observations:
#    * Ease of use:
#    * Clarity of presentation:
#    * Insights gained:
#    
# **Person 2:**
#    * Thinkaloud observations:
#    * Ease of use:
#    * Clarity of presentation:
#    * Insights gained:
#    
# **Person 3:**
#    * Thinkaloud observations:
#    * Ease of use:
#    * Clarity of presentation:
#    * Insights gained:
# 
# 
# ### Summary
# 
# - There was a clear positive relationship between sleep duration and sleep quality.
# - There appears to be a clear relationship between overall sleep quality and sleep disorder i.e. those with insomnia generally experience worse, lower quality sleep.
# - BMI and Occupation had a large variation in sleep duration and quality. Occupation data, however, is fairly limited by sample size. We could visualize this relationship similar to how we did with sleep disorders in future revisions.
# - Daily steps, age, and physical activity level appear to have a positive relationship with sleep duration.
# - Health markers such as heart rate and stress level have a negative relationship with sleep duration (note that lower heart rate and stress levels are markers are good health).
# 
# 

# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[28]:


import pandas as pd
df = pd.read_csv("customer_shopping_behavior.csv")
df.head()


# In[29]:


df.info()


# In[30]:


df.describe(include='all')


# In[31]:


df.isnull().sum()


# In[32]:


df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))


# In[33]:


df.isnull().sum()


# In[34]:


df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')
df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})


# In[35]:


df.columns


# In[36]:


# crate a column age_group
labels = ['Young Adult','Adult','Middle-aged','Senior']
df['age_group'] = pd.qcut(df['age'], q=4 ,labels = labels)



# In[37]:


df[['age','age_group']].head(10)


# In[38]:


# create column purchase_frequency_days

frequency_mapping = {
    'Fortnightly' : 14,
    'Weekly' : 7,
    'Monthly' : 30,
    'Quarterly' : 90,
    'Bi-Weekly' : 14,
    'Anually' : 365,
    'Every 3 Momths' : 90
}

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)


# In[39]:


df[['purchase_frequency_days','frequency_of_purchases']].head(10)


# In[40]:


df[['discount_applied','promo_code_used']].head(10)


# In[41]:


(df['discount_applied'] == df['promo_code_used']).all()


# In[42]:


df = df.drop('promo_code_used', axis=1)


# In[19]:


df.columns


# In[24]:


pip install psycopg2-binary sqlalchemy


# In[27]:


from sqlalchemy import create_engine
from urllib.parse import quote_plus

username = "postgres"
password = quote_plus("Harsh@123")
host = "localhost"
port = "5432"
database = "customer_behavior"

engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

table_name = "customer"
df.to_sql(table_name, engine, if_exists="replace", index=False)

print("Data successfully loaded")


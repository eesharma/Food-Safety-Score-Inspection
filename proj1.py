#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Initialize Otter
import otter
grader = otter.Notebook()


# # Project 1: Food Safety
# ## Cleaning and Exploring Data with Pandas
# ## Due Date: Thursday 09/24, 11:59 PM
# ## Collaboration Policy
# 
# Data science is a collaborative activity. While you may talk with others about
# the project, we ask that you **write your solutions individually**. If you do
# discuss the assignments with others please **include their names** at the top
# of your notebook.

# **Collaborators**: No Collaborators

# 
# ## This Assignment
# 
# In this project, we will investigate restaurant food safety scores for restaurants in San Francisco. The scores and violation information have been [made available by the San Francisco Department of Public Health](https://data.sfgov.org/Health-and-Social-Services/Restaurant-Scores-LIVES-Standard/pyih-qa8i). The main goal for this assignment is to walk through the process of Data Cleaning and EDA. 
# 
# 
# As we clean and explore these data, you will gain practice with:
# * Reading simple csv files and using Pandas
# * Working with data at different levels of granularity
# * Identifying the type of data collected, missing values, anomalies, etc.
# * Exploring characteristics and distributions of individual variables
# 
# ## Score Breakdown 
# Question | Points
# --- | ---
# 1a | 1
# 1b | 0
# 1c | 0
# 1d | 3
# 1e | 1
# 2a | 1
# 2b | 1
# 2ci | 1
# 2cii | 1
# 2d | 2
# 3a | 1
# 3b | 2
# 3ci | 1
# 3cii | 1
# 3d | 3
# 3e | 2
# 3f | 2
# 4a | 1
# 4bi | 1
# 4bii | 1
# 4biii | 1
# 4ci | 1
# 4cii | 1
# 4ciii | 1
# 4civ | 1
# 4di | 2
# 4dii | 2
# 4e | 2
# 5a | 2
# 5b | 3
# 5c | 2
# 5d | 2
# 6a|1
# 6b|2
# 7a|2
# 7b|1
# 7ci|4
# 7cii|2
# 7d|2
# 7e|1
# 7f|1
# 7g|3
# 8a|4
# 8b|4
# Total | 73

# ## Before You Start
# 
# For each question in the assignment, please write down your answer in the answer cell(s) right below the question. 
# 
# We understand that it is helpful to have extra cells breaking down the process towards reaching your final answer. If you happen to create new cells below your answer to run codes, **NEVER** add cells between a question cell and the answer cell below it. It will cause errors when we run the autograder, and it will sometimes cause a failure to generate the PDF file.
# 
# **Important note: The local autograder tests will not be comprehensive. You can pass the automated tests in your notebook but still fail tests in the autograder.** Please be sure to check your results carefully.
# 
# Finally, unless we state otherwise, try to avoid using python for loops or list comprehensions.  The majority of this assignment can be done using builtin commands in Pandas and numpy.  
# 

# In[2]:


import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
plt.style.use('fivethirtyeight')

import zipfile
import os # Used to interact with the file system


# ## Obtaining the Data
# 
# ### File Systems and I/O
# 
# 

# In general, we will focus on using python commands to investigate files.  However, it can sometimes be easier to use shell commands in your local operating system.  The following cells demonstrate how to do this.

# In[3]:


from pathlib import Path
data_dir = Path('.')
data_dir.mkdir(exist_ok = True)
file_path = data_dir / Path('data.zip')
dest_path = file_path


# After running the cell above, if you list the contents of the directory containing this notebook, you should see `data.zip`.
# 
# *Note*: The command below starts with an `!`. This tells our Jupyter notebook to pass this command to the operating system. In this case, the command is the `ls` Unix command which lists files in the current directory.

# In[4]:


get_ipython().system('ls ')


# ## 1: Loading Food Safety Data
# 
# We have data, but we don't have any specific questions about the data yet. Let's focus on understanding the structure of the data; this involves answering questions such as:
# 
# * Is the data in a standard format or encoding?
# * Is the data organized in records?
# * What are the fields in each record?
# 
# Let's start by looking at the contents of `data.zip`. It's not a just single file but rather a compressed directory of multiple files. We could inspect it by uncompressing it using a shell command such as `!unzip data.zip`, but in this project we're going to do almost everything in Python for maximum portability.

# ## Question 1a: Looking Inside and Extracting the Zip Files
# 
# Assign `my_zip` to a `zipfile.Zipfile` object representing `data.zip`, and assign `list_names` to a list of all the names of the contents in `data.zip`.
# 
# Hint: The [Python docs](https://docs.python.org/3/library/zipfile.html) describe how to create a `zipfile.ZipFile` object.
# 
# <!--
# BEGIN QUESTION
# name: q1a
# points: 1
# -->

# In[5]:


my_zip = zipfile.ZipFile(dest_path, 'r')
list_names = [f.filename for f in my_zip.filelist]
list_names


# In[6]:


grader.check("q1a")


# In your answer above, if you have written something like `zipfile.ZipFile('data.zip', ...)`, we suggest changing it to read `zipfile.ZipFile(dest_path, ...)`. In general, we **strongly suggest having your filenames hard coded as string literals only once** in a notebook. It is very dangerous to hard code things twice because if you change one but forget to change the other, you can end up with bugs that are very hard to find.

# Now display the files' names and their sizes. Format your solution by printing each file and its size on a new line.
# 
# If you're not sure how to proceed, read about the attributes of a `ZipFile` object in the Python docs linked above.

# In[7]:


file_names_sizes = my_zip.infolist()
file_names_sizes


# Often when working with zipped data, we'll never unzip the actual zipfile. This saves space on our local computer. However, for this project the files are small, so we're just going to unzip everything. This has the added benefit that you can look inside the csv files using a text editor, which might be handy for understanding the structure of the files. The cell below will unzip the csv files into a subdirectory called `data`. Simply run this cell, i.e. don't modify it.

# In[8]:


data_dir = Path('.')
my_zip.extractall(data_dir)
get_ipython().system('ls {data_dir / Path("data")}')


# The cell above created a folder called `data`, and in it there should be five CSV files. Let's open up `legend.csv` to see its contents. To do this, click on 'Jupyter' in the top left, then navigate to `fa20/proj/proj1/data/` and click on `legend.csv`. The file will open up in another tab. You should see something that looks like:
# 
#     "Minimum_Score","Maximum_Score","Description"
#     0,70,"Poor"
#     71,85,"Needs Improvement"
#     86,90,"Adequate"
#     91,100,"Good"

# ## Question 1b
# 
# The `legend.csv` file does indeed look like a well-formed CSV file. Let's check the other three files. Rather than opening up each file manually, let's use Python to print out the first 5 lines of each. The `ds100_utils` library has a method called `head` that will allow you to retrieve the first N lines of a file as a list. For example `ds100_utils.head('data/legend.csv', 5)` will return the first 5 lines of "data/legend.csv". Try using this function to print out the first 5 lines of all six files that we just extracted from the zipfile.

# In[117]:


import ds100_utils

print(ds100_utils.head('data/legend.csv', 5))

print(ds100_utils.head('data/bus.csv', 5))

print(ds100_utils.head('data/ins2vio.csv', 5))

print(ds100_utils.head('data/vio.csv', 5))

print(ds100_utils.head('data/ins.csv', 5))


# ## Question 1c: Reading in the Files
# 
# Based on the above information, let's attempt to load `bus.csv`, `ins2vio.csv`, `ins.csv`, and `vio.csv` into pandas dataframes with the following names: `bus`, `ins2vio`, `ins`, and `vio` respectively.
# 
# *Note:* Because of character encoding issues one of the files (`bus`) will require an additional argument `encoding='ISO-8859-1'` when calling `pd.read_csv`. At some point in your future, you should read all about [character encodings](https://diveintopython3.problemsolving.io/strings.html). We won't discuss these in detail in DS100.

# In[118]:


# path to directory containing data
dsDir = Path('data')

bus = pd.read_csv(dsDir/'bus.csv', encoding='ISO-8859-1')
ins2vio = pd.read_csv(dsDir/'ins2vio.csv')
ins = pd.read_csv(dsDir/'ins.csv') 
vio = pd.read_csv(dsDir/'vio.csv') 

#This code is essential for the autograder to function properly. Do not edit
ins_test = ins


# Now that you've read in the files, let's try some `pd.DataFrame` methods ([docs](https://pandas.pydata.org/pandas-docs/version/0.21/generated/pandas.DataFrame.html)).
# Use the `DataFrame.head` method to show the top few lines of the `bus`, `ins`, and `vio` dataframes. To show multiple return outputs in one single cell, you can use `display()`. 

# In[119]:


display(bus.head(),
ins.head(),
vio.head())


# The `DataFrame.describe` method can also be handy for computing summaries of numeric columns of our dataframes. Try it out with each of our 4 dataframes.

# In[120]:


display(bus.describe(),
ins2vio.describe(),
ins.describe(),
vio.describe())


# Now, we perform some sanity checks for you to verify that you loaded the data with the right structure. Run the following cells to load some basic utilities (you do not need to change these at all):

# First, we check the basic structure of the data frames you created:

# In[121]:


assert all(bus.columns == ['business id column', 'name', 'address', 'city', 'state', 'postal_code',
                           'latitude', 'longitude', 'phone_number'])
assert 6250 <= len(bus) <= 6260

assert all(ins.columns == ['iid', 'date', 'score', 'type'])
assert 26660 <= len(ins) <= 26670

assert all(vio.columns == ['description', 'risk_category', 'vid'])
assert 60 <= len(vio) <= 65

assert all(ins2vio.columns == ['iid', 'vid'])
assert 40210 <= len(ins2vio) <= 40220


# Next we'll check that the statistics match what we expect. The following are hard-coded statistical summaries of the correct data.

# In[122]:


bus_summary = pd.DataFrame(**{'columns': ['business id column', 'latitude', 'longitude'],
 'data': {'business id column': {'50%': 75685.0, 'max': 102705.0, 'min': 19.0},
  'latitude': {'50%': -9999.0, 'max': 37.824494, 'min': -9999.0},
  'longitude': {'50%': -9999.0,
   'max': 0.0,
   'min': -9999.0}},
 'index': ['min', '50%', 'max']})

ins_summary = pd.DataFrame(**{'columns': ['score'],
 'data': {'score': {'50%': 76.0, 'max': 100.0, 'min': -1.0}},
 'index': ['min', '50%', 'max']})

vio_summary = pd.DataFrame(**{'columns': ['vid'],
 'data': {'vid': {'50%': 103135.0, 'max': 103177.0, 'min': 103102.0}},
 'index': ['min', '50%', 'max']})

from IPython.display import display

print('What we expect from your Businesses dataframe:')
display(bus_summary)
print('What we expect from your Inspections dataframe:')
display(ins_summary)
print('What we expect from your Violations dataframe:')
display(vio_summary)


# The code below defines a testing function that we'll use to verify that your data has the same statistics as what we expect. Run these cells to define the function. The `df_allclose` function has this name because we are verifying that all of the statistics for your dataframe are close to the expected values. Why not `df_allequal`? It's a bad idea in almost all cases to compare two floating point values like 37.780435, as rounding error can cause spurious failures.

# ## Question 1d: Verifying the data
# 
# Now let's run the automated tests. If your dataframes are correct, then the following cell will seem to do nothing, which is a good thing! However, if your variables don't match the correct answers in the main summary statistics shown above, an exception will be raised.
# 
# <!--
# BEGIN QUESTION
# name: q1d
# points: 3
# -->

# In[123]:


"""Run this cell to load this utility comparison function that we will use in various
tests below (both tests you can see and those we run internally for grading).

Do not modify the function in any way.
"""


def df_allclose(actual, desired, columns=None, rtol=5e-2):
    """Compare selected columns of two dataframes on a few summary statistics.
    
    Compute the min, median and max of the two dataframes on the given columns, and compare
    that they match numerically to the given relative tolerance.
    
    If they don't match, an AssertionError is raised (by `numpy.testing`).
    """    
    # summary statistics to compare on
    stats = ['min', '50%', 'max']
    
    # For the desired values, we can provide a full DF with the same structure as
    # the actual data, or pre-computed summary statistics.
    # We assume a pre-computed summary was provided if columns is None. In that case, 
    # `desired` *must* have the same structure as the actual's summary
    if columns is None:
        des = desired
        columns = desired.columns
    else:
        des = desired[columns].describe().loc[stats]

    # Extract summary stats from actual DF
    act = actual[columns].describe().loc[stats]

    return np.allclose(act, des, rtol)


# In[124]:


grader.check("q1d")


# ### Question 1e: Identifying Issues with the Data

# <!-- BEGIN QUESTION -->
# 
# Use the `head` command on your three files again. This time, describe at least one potential problem with the data you see. Consider issues with missing values and bad data.
# 
# <!--
# BEGIN QUESTION
# name: q1e
# manual: True
# points: 1
# -->

# There is a missing phone number for "HEUNG YUEN RESTAURANT" the first listing in the "business" dataframe.
# This value is  the value for number is -9999, which is invalid and incorrect. Formatting for the address column is inconsistent, due to the variability in street names and building locations. Lastly, longitude and latitude values in the business column are values like "-9999.00," which is not a valid input and would need further inspection.

# <!-- END QUESTION -->
# 
# 
# 
# We will explore each file in turn, including determining its granularity and primary keys and exploring many of the variables individually. Let's begin with the businesses file, which has been read into the `bus` dataframe.

# <br/><br/><br/>
# 
# ---
# 
# <br/><br/><br/>
# 
# # 2: Examining the Business Data File
# 
# From its name alone, we expect the `bus.csv` file to contain information about the restaurants. Let's investigate the granularity of this dataset.

# In[127]:


bus.head()


# <br/><br/><br/>
# 
# ---
# 
# ## Question 2a
# 
# The `bus` dataframe contains a column called `business id column` which probably corresponds to a unique business id.  However, let's first rename that column to `bid`.  Modify the `bus` dataframe by renaming that column to `bid`.
# 
# **Note**: In practice we might want to do this renaming when the table is loaded but for grading purposes we will do it here.
# 
# <!--
# BEGIN QUESTION
# name: q2a
# points: 1
# -->

# In[128]:


bus = bus.rename(columns={"business id column": "bid"})


# In[129]:


grader.check("q2a")


# <br/><br/><br/>
# 
# ---
# 
# ## Question 2b
# 
# Examining the entries in `bus`, is the `bid` unique for each record (i.e. each row of data)? Your code should compute the answer, i.e. don't just hard code `True` or `False`.
# 
# Hint: use `value_counts()` or `unique()` to determine if the `bid` series has any duplicates.
# 
# <!--
# BEGIN QUESTION
# name: q2b
# points: 1
# -->

# In[133]:


is_bid_unique = bus['bid'].value_counts().max() == 1
is_bid_unique


# In[134]:


grader.check("q2b")


# <br/><br/><br/>
# 
# ---
# 
# 
# ## Question 2c
# 
# In the two cells below create two **series** 
# 
# 1. where the index is the `name` of the business and the value is the number of records with that `name`
# 2. where the index is the `address` of the business and the value is the number of records with that `address`
# 
# Order both series in descending order by count. You may need to use `groupby()`, `size()`, `sort_values()`, or `value_counts()`. 
# 
# **Step 1**
# 
# <!--
# BEGIN QUESTION
# name: q2ci
# points: 1
# -->

# In[135]:


name_counts = bus['name'].value_counts()
name_counts.head(20)


# In[136]:


grader.check("q2ci")


# **Step 2**
# 
# <!--
# BEGIN QUESTION
# name: q2cii
# points: 1
# -->

# In[137]:


address_counts = bus['address'].value_counts()
address_counts.head(10)


# In[138]:


grader.check("q2cii")


# <br/><br/><br/>
# 
# ---
# 
# 
# ## Question 2d
# 
# Based on the above calculations answer each of the following questions by filling the value in the variable.
# 
# 1. What does each record represent?  
# 1. What is the minimal primary key?
# 
# <!--
# BEGIN QUESTION
# name: q2d
# points: 2
# -->

# In[139]:


# What does each record represent?  Valid answers are:
#    "One location of a restaurant."
#    "A chain of restaurants."
#    "A city block."
q2d_part1 = "One location of a restaurant."

# What is the minimal primary key? Valid answers are:
#    "bid"
#    "bid, name"
#    "bid, name, address"
q2d_part2 = "bid"


# In[140]:


grader.check("q2d")


# <br/><br/><br/>
# 
# ---
# 
# <br/><br/><br/>
# 
# # 3: Cleaning the Business Data Postal Codes
# 
# The business data contains postal code information that we can use to aggregate the ratings over regions of the city.  Let's examine and clean the postal code field.  The postal code (sometimes also called a ZIP code) partitions the city into regions:
# 
# <img src="https://www.usmapguide.com/wp-content/uploads/2019/03/printable-san-francisco-zip-code-map.jpg" alt="ZIP Code Map" style="width: 600px">

# <br/><br/><br/>
# 
# ---
# 
# 
# ## Question 3a
# 
# How many restaurants are in each ZIP code? 
# 
# In the cell below, create a **series** where the index is the postal code and the value is the number of records with that postal code in descending order of count. You may need to use `groupby()`, `size()`, or `value_counts()`. Do you notice any odd/invalid zip codes?
# 
# <!--
# BEGIN QUESTION
# name: q3a
# points: 1
# -->

# In[28]:


zip_counts = bus['postal_code'].value_counts()
print(zip_counts.to_string())


# In[29]:


grader.check("q3a")


# <br/><br/><br/>
# 
# --- 
# 
# ## Question 3b
# 
# Answer the following questions about the `postal_code` column in the `bus` dataframe.
# 
# 1. The ZIP code column is which of the following type of data:
#     1. Quantitative Continuous
#     1. Quantitative Discrete
#     1. Qualitative Ordinal
#     1. Qualitative Nominal    
# 1. What Python data type is used to represent a ZIP code?
# 
# *Note*: ZIP codes and postal codes are the same thing.
# 
# Please write your answers in the variables below:
# 
# <!--
# BEGIN QUESTION
# name: q3b
# points: 2
# -->

# In[30]:


# The ZIP code column is which of the following type of data:
#   "Quantitative Continuous" 
#   "Quantitative Discrete"
#   "Qualitative Ordinal"
#   "Qualitative Nominal"
q3b_part1 = "Qualitative Nominal"

# What Python data type is used to represent a ZIP code? 
#    "str"
#    "int"
#    "bool"
#    "float"
q3b_part2 = "str"


# In[31]:


grader.check("q3b")


# <br/><br/><br/>
# 
# --- 
# 
# ## Question 3c
# 
# In question 3a we noticed a large number of potentially invalid ZIP codes (e.g., "Ca").  These are likely due to data entry errors.  To get a better understanding of the potential errors in the zip codes we will:
# 
# 1. Import a list of valid San Francisco ZIP codes by using `pd.read_json` to load the file `data/sf_zipcodes.json` and extract a **series** of type `str` containing the valid ZIP codes.  *Hint: set `dtype` when invoking `read_json`.*
# 1. Construct a `DataFrame` containing only the businesses which DO NOT have valid ZIP codes.  You will probably want to use the `Series.isin` function. 
# 

# **Step 1**
# 
# <!--
# BEGIN QUESTION
# name: q3ci
# points: 1
# -->

# In[32]:


valid_zips = pd.read_json("data/sf_zipcodes.json", dtype = "string")["zip_codes"]
valid_zips.head()


# In[33]:


grader.check("q3ci")


# **Step 2**
# 
# <!--
# BEGIN QUESTION
# name: q3cii
# points: 1
# -->

# In[141]:


invalid_zip_bus = bus[~bus['postal_code'].isin(valid_zips)]
invalid_zip_bus.head(20)


# In[142]:


grader.check("q3cii")


# <br/><br/><br/>
# 
# --- 
# 
# ## Question 3d
# 
# In the previous question, many of the businesses had a common invalid postal code that was likely used to encode a MISSING postal code.  Do they all share a potentially "interesting address"?
# 
# In the following cell, construct a **series** that counts the number of businesses at each `address` that have this single likely MISSING postal code value.  Order the series in descending order by count. 
# 
# After examining the output.  Answer the following question by filling in the appropriate variable. If we were to drop businesses with MISSING postal code values would a particular class of business be affected?  If you are unsure try to search the web for the most common addresses.
# 
# 
# <!--
# BEGIN QUESTION
# name: q3d
# points: 3
# -->

# In[143]:


missing_zip_address_count = invalid_zip_bus.loc[(invalid_zip_bus["postal_code"] == "-9999")]["address"].value_counts()
missing_zip_address_count.head()


# In[144]:


grader.check("q3d")


# <br/><br/><br/>
# 
# --- 
# 
# ## Question 3e
# 
# **True or False**:  *If we were to drop businesses with MISSING postal code values, a particular class of business will be affected.*
# 
# <!--
# BEGIN QUESTION
# name: q3e
# points: 2
# -->

# In[145]:


# True or False: 
#  If we were to drop businesses with MISSING postal code values 
#   a particular class of business be affected.
q3d_true_or_false = True


# In[146]:


grader.check("q3e")


# <br/><br/><br/>
# 
# --- 
# 
# ## Question 3f
# 
# Examine the `invalid_zip_bus` dataframe we computed above and look at the businesses that DO NOT have the special MISSING ZIP code value.  Some of the invalid postal codes are just the full 9 digit code rather than the first 5 digits.  Create a new column named `postal5` in the original `bus` dataframe which contains only the first 5 digits of the `postal_code` column.   Finally, for any of the `postal5` ZIP code entries that were not a valid San Fransisco ZIP Code (according to `valid_zips`) set the entry to `None`.  
# 
# 
# <!--
# BEGIN QUESTION
# name: q3f
# points: 2
# -->

# In[147]:


bus['postal5'] = bus['postal_code'].str[:5] #create postal5 in bus dataframe with 5 digits of postal_code column.
bus.loc[~bus['postal5'].isin(valid_zips), "postal5"] = None #any postal5 entries that were invalid, set to None.

# Checking the corrected postal5 column
bus.loc[invalid_zip_bus.index, ['bid', 'name', 'postal_code', 'postal5']]


# In[148]:


grader.check("q3f")


# <br/><br/><br/>
# 
# ---
# 
# <br/><br/><br/>
# 
# # 4: Investigate the Inspection Data
# 
# Let's now turn to the inspection DataFrame. Earlier, we found that `ins` has 4 columns named 
# `iid`, `score`, `date` and `type`.  In this section, we determine the granularity of `ins` and investigate the kinds of information provided for the inspections. 

# Let's start by looking again at the first 5 rows of `ins` to see what we're working with.

# In[149]:


ins.head(5)


# <br/><br/><br/>
# 
# ---
# 
# ## Question 4a
# 
# The column `iid` probably corresponds to an inspection id.  Is it a primary key?  Write an expression (line of code) that evaluates to 'True' or 'False' based on whether all the values are unique.
# 
# 
# <!--
# BEGIN QUESTION
# name: q4a
# points: 1
# -->

# In[150]:


is_ins_iid_a_primary_key = len(ins['iid'].unique()) == len(ins['iid'])


# In[151]:


grader.check("q4a")


# <br/><br/><br/>
# 
# ---
# 
# ## Question 4b
# 
# The column `iid` appears to be the composition of two numbers and the first number looks like a business id.  
# 
# **Part 1.**: Create a new column called `bid` in the `ins` dataframe containing just the business id.  You will want to use `ins['iid'].str` operations to do this.  Also be sure to convert the type of this column to `int`
# 
# **Part 2.**: Then compute how many values in this new column are invalid business ids (i.e. do not appear in the `bus['bid']` column). This is verifying a foreign key relationship. Consider using the `pd.Series.isin` function.
# 
# **Part 3.**: Answer True or False, `ins['bid']` is a foreign key reference to `bus['bid']`.
# 
# 
# **No python `for` loops or list comprehensions required!**

# **Part 1**
# 
# <!--
# BEGIN QUESTION
# name: q4bi
# points: 1
# -->

# In[152]:


ins['bid'] = ins['iid'].str.split('_').str[0].astype('int64')


# In[153]:


grader.check("q4bi")


# **Part 2**
# 
# <!--
# BEGIN QUESTION
# name: q4bii
# points: 1
# -->

# In[154]:


invalid_bid_count = sum(ins['bid'].isin(bus['bid']))


# In[155]:


grader.check("q4bii")


# **Part 3**
# 
# <!--
# BEGIN QUESTION
# name: q4biii
# points: 1
# -->

# In[156]:


# True or False: The column ins['bid'] is a foreign key 
#   referencing the bus['bid'] primary key.

q4b_is_foreign_key = True


# In[157]:


grader.check("q4biii")


# <br/><br/><br/>
# 
# ---
# 
# ## Question 4c
# 
# What if we are interested in a time component of the inspection data?  We need to examine the date column of each inspection. 
# 
# **Part 1:** What is the type of the individual `ins['date']` entries. You may want to grab the very first entry and use the `type` function in python. 
# 
# **Part 2:** Use `pd.to_datetime` to create a new `ins['timestamp']` column containing of `pd.Timestamp` objects.  These will allow us to do more date manipulation.
# 
# **Part 3:** What are the earliest and latest dates in our inspection data?  *Hint: you can use `min` and `max` on dates of the correct type.*
# 
# **Part 4:** We probably want to examine the inspections by year. Create an additional `ins['year']` column containing just the year of the inspection.  Consider using `pd.Series.dt.year` to do this.
# 
# **No python `for` loops or list comprehensions required!**

# **Part 1**
# 
# <!--
# BEGIN QUESTION
# name: q4ci
# points: 1
# -->

# In[158]:


ins_date_type = type(ins['date'].iloc[0])
ins_date_type


# In[159]:


grader.check("q4ci")


# **Part 2**
# 
# <!--
# BEGIN QUESTION
# name: q4cii
# points: 1
# -->

# In[160]:


ins['timestamp'] = pd.to_datetime(ins['date'])


# In[161]:


grader.check("q4cii")


# **Part 3**
# 
# <!--
# BEGIN QUESTION
# name: q4ciii
# points: 1
# -->

# In[162]:


earliest_date = min(ins['timestamp'])
latest_date = max(ins['timestamp'])

print("Earliest Date:", earliest_date)
print("Latest Date:", latest_date)


# In[163]:


grader.check("q4ciii")


# **Part 4**
# 
# <!--
# BEGIN QUESTION
# name: q4civ
# points: 1
# -->

# In[164]:


ins['year'] = ins['timestamp'].dt.year


# In[165]:


grader.check("q4civ")


# In[166]:


ins.head()


# <br/><br/><br/>
# 
# ---
# 
# ## Question 4d
# 
# What is the relationship between the type of inspection over the 2016 to 2019 timeframe? 
# 
# **Part 1**
# 
# Construct the following table by
# 1. Using the `pivot_table` containing the number (`size`) of inspections for the given `type` and `year`.
# 1. Adding an extra `Total` column to the result using `sum`
# 1. Sort the results in descending order by the `Total`.
# 
# <table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th>year</th>      <th>2016</th>      <th>2017</th>      <th>2018</th>      <th>2019</th>      <th>Total</th>    </tr>    <tr>      <th>type</th>      <th></th>      <th></th>      <th></th>      <th></th>      <th></th>    </tr>  </thead>  <tbody>    <tr>      <th>Routine - Unscheduled</th>      <td>966</td>      <td>4057</td>      <td>4373</td>      <td>4681</td>      <td>14077</td>    </tr>    <tr>      <th>Reinspection/Followup</th>      <td>445</td>      <td>1767</td>      <td>1935</td>      <td>2292</td>      <td>6439</td>    </tr>    <tr>      <th>New Ownership</th>      <td>99</td>      <td>506</td>      <td>528</td>      <td>459</td>      <td>1592</td>    </tr>    <tr>      <th>Complaint</th>      <td>91</td>      <td>418</td>      <td>512</td>      <td>437</td>      <td>1458</td>    </tr>    <tr>      <th>New Construction</th>      <td>102</td>      <td>485</td>      <td>218</td>      <td>189</td>      <td>994</td>    </tr>    <tr>      <th>Non-inspection site visit</th>      <td>51</td>      <td>276</td>      <td>253</td>      <td>231</td>      <td>811</td>    </tr>    <tr>      <th>New Ownership - Followup</th>      <td>0</td>      <td>45</td>      <td>219</td>      <td>235</td>      <td>499</td>    </tr>    <tr>      <th>Structural Inspection</th>      <td>1</td>      <td>153</td>      <td>50</td>      <td>190</td>      <td>394</td>    </tr>    <tr>      <th>Complaint Reinspection/Followup</th>      <td>19</td>      <td>68</td>      <td>70</td>      <td>70</td>      <td>227</td>    </tr>    <tr>      <th>Foodborne Illness Investigation</th>      <td>1</td>      <td>29</td>      <td>50</td>      <td>35</td>      <td>115</td>    </tr>    <tr>      <th>Routine - Scheduled</th>      <td>0</td>      <td>9</td>      <td>8</td>      <td>29</td>      <td>46</td>    </tr>    <tr>      <th>Administrative or Document Review</th>      <td>2</td>      <td>1</td>      <td>1</td>      <td>0</td>      <td>4</td>    </tr>    <tr>      <th>Multi-agency Investigation</th>      <td>0</td>      <td>0</td>      <td>1</td>      <td>2</td>      <td>3</td>    </tr>    <tr>      <th>Special Event</th>      <td>0</td>      <td>3</td>      <td>0</td>      <td>0</td>      <td>3</td>    </tr>    <tr>      <th>Community Health Assessment</th>      <td>1</td>      <td>0</td>      <td>0</td>      <td>0</td>      <td>1</td>    </tr>  </tbody></table>
# 
# **No python `for` loops or list comprehensions required!**

# In[169]:


ins_pivot = ins.pivot_table(index = 'type', columns = "year", aggfunc = "size").fillna(0).astype('int64')
ins_pivot['Total'] = ins_pivot.sum(axis = 1)
ins_pivot_sorted = ins_pivot.sort_values('Total', ascending=False)


# In[170]:


grader.check("q4di")


# **Part 2**
# 
# Based on the above analysis, which year appears to have had a lot of businesses in newly constructed buildings?
# <!--
# BEGIN QUESTION
# name: q4dii
# points: 2
# -->

# In[171]:


year_of_new_construction = 2017


# In[172]:


grader.check("q4dii")


# <br/><br/><br/>
# 
# ---
# 
# ## Question 4e
# 
# Let's examine the inspection scores `ins['score']`
# 
# 

# In[173]:


ins['score'].value_counts().head()


# There are a large number of inspections with the `'score'` of `-1`.   These are probably missing values.  Let's see what type of inspections have scores and which do not. Create the following dataframe using steps similar to the previous question, and assign it to to the variable `ins_missing_score_pivot`.
# 
# You should observe that inspection scores appear only to be assigned to `Routine - Unscheduled` inspections.
# 
# 
# <table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th>Missing Score</th>      <th>False</th>      <th>True</th>      <th>Total</th>    </tr>    <tr>      <th>type</th>      <th></th>      <th></th>      <th></th>    </tr>  </thead>  <tbody>    <tr>      <th>Routine - Unscheduled</th>      <td>14031</td>      <td>46</td>      <td>14077</td>    </tr>    <tr>      <th>Reinspection/Followup</th>      <td>0</td>      <td>6439</td>      <td>6439</td>    </tr>    <tr>      <th>New Ownership</th>      <td>0</td>      <td>1592</td>      <td>1592</td>    </tr>    <tr>      <th>Complaint</th>      <td>0</td>      <td>1458</td>      <td>1458</td>    </tr>    <tr>      <th>New Construction</th>      <td>0</td>      <td>994</td>      <td>994</td>    </tr>    <tr>      <th>Non-inspection site visit</th>      <td>0</td>      <td>811</td>      <td>811</td>    </tr>    <tr>      <th>New Ownership - Followup</th>      <td>0</td>      <td>499</td>      <td>499</td>    </tr>    <tr>      <th>Structural Inspection</th>      <td>0</td>      <td>394</td>      <td>394</td>    </tr>    <tr>      <th>Complaint Reinspection/Followup</th>      <td>0</td>      <td>227</td>      <td>227</td>    </tr>    <tr>      <th>Foodborne Illness Investigation</th>      <td>0</td>      <td>115</td>      <td>115</td>    </tr>    <tr>      <th>Routine - Scheduled</th>      <td>0</td>      <td>46</td>      <td>46</td>    </tr>    <tr>      <th>Administrative or Document Review</th>      <td>0</td>      <td>4</td>      <td>4</td>    </tr>    <tr>      <th>Multi-agency Investigation</th>      <td>0</td>      <td>3</td>      <td>3</td>    </tr>    <tr>      <th>Special Event</th>      <td>0</td>      <td>3</td>      <td>3</td>    </tr>    <tr>      <th>Community Health Assessment</th>      <td>0</td>      <td>1</td>      <td>1</td>    </tr>  </tbody></table>
# 
# 

# In[174]:


ins["Missing Score"] = ins["score"] == -1

ins_missing_score_pivot = ins.pivot_table(index = 'type', columns = "Missing Score", aggfunc = "size").fillna(0).astype('int64')

ins_missing_score_pivot['Total'] = ins_missing_score_pivot.sum(axis = 1)

ins_missing_score_pivot = ins_missing_score_pivot.sort_values('Total', ascending=False)

ins_missing_score_pivot


# In[175]:


grader.check("q4e")


# Notice that inspection scores appear only to be assigned to `Routine - Unscheduled` inspections. It is reasonable that for inspection types such as `New Ownership` and `Complaint` to have no associated inspection scores, but we might be curious why there are no inspection scores for the `Reinspection/Followup` inspection type.

# <br/><br/><br/>
# 
# ---
# 
# <br/><br/><br/>
# 
# # 5: Joining Data Across Tables
# 
# In this question we will start to connect data across mulitple tables.  We will be using the `merge` function. 

# <br/><br/><br/>
# 
# --- 
# 
# ## Question 5a
# 
# Let's figure out which restaurants had the lowest scores. Before we proceed, let's filter out missing scores from `ins` so that negative scores don't influence our results.

# In[176]:


ins = ins[ins["score"] > 0]


# We'll start by creating a new dataframe called `ins_named`. It should be exactly the same as `ins`, except that it should have the name and address of every business, as determined by the `bus` dataframe. If a `business_id` in `ins` does not exist in `bus`, the name and address should be given as `NaN`. 
# 
# *Hint*: Use the merge method to join the `ins` dataframe with the appropriate portion of the `bus` dataframe. See the official [documentation](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html) on how to use `merge`.
# 
# *Note*: For quick reference, a pandas 'left' join keeps the keys from the left frame, so if `ins` is the left frame, all the keys from `ins` are kept and if a set of these keys don't have matches in the other frame, the columns from the other frame for these "unmatched" key rows contains NaNs.
# 
# <!--
# BEGIN QUESTION
# name: q5a
# points: 2
# -->

# In[177]:


ins_named = pd.merge(ins, bus, how='left', on='bid')
ins_named.head()


# In[179]:


grader.check("q5a")


# <br/><br/><br/>
# 
# --- 
# 
# ## Question 5b
# 
# Let's look at the 20 businesses with the lowest **median** score.  Order your results by the median score followed by the business id to break ties. The resulting table should look like:
# 
# 
# *Hint: You may find the `as_index` argument important*
# 
# <table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>bid</th>      <th>name</th>      <th>median score</th>    </tr>  </thead>  <tbody>    <tr>      <th>3876</th>      <td>84590</td>      <td>Chaat Corner</td>      <td>54.0</td>    </tr>    <tr>      <th>4564</th>      <td>90622</td>      <td>Taqueria Lolita</td>      <td>57.0</td>    </tr>    <tr>      <th>4990</th>      <td>94351</td>      <td>VBowls LLC</td>      <td>58.0</td>    </tr>    <tr>      <th>2719</th>      <td>69282</td>      <td>New Jumbo Seafood Restaurant</td>      <td>60.5</td>    </tr>    <tr>      <th>222</th>      <td>1154</td>      <td>SUNFLOWER RESTAURANT</td>      <td>63.5</td>    </tr>    <tr>      <th>1991</th>      <td>39776</td>      <td>Duc Loi Supermarket</td>      <td>64.0</td>    </tr>    <tr>      <th>2734</th>      <td>69397</td>      <td>Minna SF Group LLC</td>      <td>64.0</td>    </tr>    <tr>      <th>3291</th>      <td>78328</td>      <td>Golden Wok</td>      <td>64.0</td>    </tr>    <tr>      <th>4870</th>      <td>93150</td>      <td>Chez Beesen</td>      <td>64.0</td>    </tr>    <tr>      <th>4911</th>      <td>93502</td>      <td>Smoky Man</td>      <td>64.0</td>    </tr>    <tr>      <th>5510</th>      <td>98995</td>      <td>Vallarta's Taco Bar</td>      <td>64.0</td>    </tr>    <tr>      <th>1457</th>      <td>10877</td>      <td>CHINA FIRST INC.</td>      <td>64.5</td>    </tr>    <tr>      <th>2890</th>      <td>71310</td>      <td>Golden King Vietnamese Restaurant</td>      <td>64.5</td>    </tr>    <tr>      <th>4352</th>      <td>89070</td>      <td>Lafayette Coffee Shop</td>      <td>64.5</td>    </tr>    <tr>      <th>505</th>      <td>2542</td>      <td>PETER D'S RESTAURANT</td>      <td>65.0</td>    </tr>    <tr>      <th>2874</th>      <td>71008</td>      <td>House of Pancakes</td>      <td>65.0</td>    </tr>    <tr>      <th>818</th>      <td>3862</td>      <td>IMPERIAL GARDEN SEAFOOD RESTAURANT</td>      <td>66.0</td>    </tr>    <tr>      <th>2141</th>      <td>61427</td>      <td>Nick's Foods</td>      <td>66.0</td>    </tr>    <tr>      <th>2954</th>      <td>72176</td>      <td>Wolfes Lunch</td>      <td>66.0</td>    </tr>    <tr>      <th>4367</th>      <td>89141</td>      <td>Cha Cha Cha on Mission</td>      <td>66.5</td>    </tr>  </tbody></table>
# 
# 
# <!--
# BEGIN QUESTION
# name: q5b
# points: 3
# -->

# In[180]:


twenty_lowest_scoring = ins_named[ins_named["Missing Score"] == False].groupby(["bid", "name"], as_index = False).median().sort_values(by = ["score", "bid"])
twenty_lowest_scoring = twenty_lowest_scoring.rename(columns = {'score': "median score"})[['bid', 'name', 'median score']].head(20)
twenty_lowest_scoring


# In[181]:


grader.check("q5b")


# <br/><br/><br/>
# 
# --- 
# 
# ## Question 5c
# 
# Let's now examine the descriptions of violations for inspections with `score > 0` and `score < 65`.  Construct a **Series** indexed by the `description` of the violation from the `vio` table with the value being the number of times that violation occured for inspections with the above score range.  Sort the results in descending order of the count.
# 
# The first few entries should look like:
# 
# ```
# Unclean or unsanitary food contact surfaces                                  43
# High risk food holding temperature                                           42
# Unclean or degraded floors walls or ceilings                                 40
# Unapproved or unmaintained equipment or utensils                             39
# ```
# You will need to use `merge` twice.
# 
# <!--
# BEGIN QUESTION
# name: q5c
# points: 2
# -->

# In[184]:


low_score_violations = pd.merge(vio, ins2vio, on='vid')

low_score_violations = pd.merge(low_score_violations, ins, on='iid')

low_score_violations = low_score_violations[low_score_violations['score'] > 0]

low_score_violations = low_score_violations[low_score_violations['score'] < 65]

low_score_violations = low_score_violations.groupby('description').size().sort_values(ascending=False)

low_score_violations.head(60)


# In[185]:


grader.check("q5c")


# ### Question 5d
# Let's figure out which restaurant had the worst scores ever (single lowest score). 

# In[190]:


worst_restaurant = ins_named.sort_values(by='score', ascending=True).head(1)
worst_restaurant


# <!-- BEGIN QUESTION -->
# 
# **In the cell below, write the name of the restaurant** with the lowest inspection scores ever. You can also head to yelp.com and look up the reviews page for this restaurant. Feel free to add anything interesting you want to share.
# 
# <!--
# BEGIN QUESTION
# name: q5d
# points: 2
# manual: True
# -->

# The restaurant's name is Lollipot, with a score of 45.

# <!-- END QUESTION -->
# 
# 
# 
# <br/><br/><br/><br/>
# 
# ---
# 
# <br/><br/>
# 
# ## 6: Explore Inspection Scores
# 
# In this part we explore some of the basic inspection score values visually.

# <!-- BEGIN QUESTION -->
# 
# <br/><br/><br/>
# 
# ---
# 
# 
# ## Question 6a
# Let's look at the distribution of inspection scores. As we saw before when we called head on this data frame, inspection scores appear to be integer values. The discreteness of this variable means that we can use a barplot to visualize the distribution of the inspection score. Make a bar plot of the counts of the number of inspections receiving each score.
# 
# It should look like the image below. It does not need to look exactly the same (e.g., no grid), but make sure that all labels and axes are correct.
# 
# ![](pics/6a.png)
# 
# You might find this [matplotlib.pyplot tutorial](https://matplotlib.org/tutorials/introductory/pyplot.html) useful. Key syntax that you'll need:
# 
# ```
# plt.bar
# plt.xlabel
# plt.ylabel
# plt.title
# ```
# 
# *Note*: If you want to use another plotting library for your plots (e.g. plotly, sns) you are welcome to use that library instead so long as it works on DataHub. If you use seaborn sns.countplot(), you may need to manually set what to display on xticks.
# 
# 
# <!--
# BEGIN QUESTION
# name: q6a
# points: 1
# manual: True
# -->

# In[195]:


score_counts = ins_named['score'].value_counts() 
heightyaxis = score_counts.tolist()
plt.bar(list(score_counts.index.values), height=heightyaxis) 
plt.xlabel('Score')
plt.ylabel('Count')
plt.title('Distribution of Inspection Scores')


# <!-- END QUESTION -->

# In[196]:


score_counts


# <!-- BEGIN QUESTION -->
# 
# <br/><br/><br/>
# 
# ---
# 
# ### Question 6b
# Describe the qualities of the distribution of the inspections scores based on your bar plot. Consider the mode(s), symmetry, tails, gaps, and anomalous values. Are there any unusual features of this distribution? What do your observations imply about the scores?
# 
# <!--
# BEGIN QUESTION
# name: q6b
# points: 2
# manual: True
# -->

# The distribution has one peak, at 100, which means that it is a unimodal distribution. There is a left skew with a lengthy left tail. From the range of 50-70, there are very few values that mark the end of the left tail. It seems like even numbered scores have higher total counts than odd numbered scores. This could be due to the scoring system, where penalties are also even numbers. There are also some gaps in the 90-100 range of scores, which is unusual.

# <!-- END QUESTION -->
# 
# 
# 
# <br/><br/><br/><br/>
# 
# ---
# 
# <br/><br/>
# 
# ## 7: Restaurant Ratings Over Time
# 
# Let's consider various scenarios involving restaurants with multiple ratings over time.
# 
# 

# <br/><br/><br/>
# 
# ---
# 
# ### Question 7a
# 
# Let's see which restaurant has had the most extreme improvement in its rating, aka scores. Let the "swing" of a restaurant be defined as the difference between its highest-ever and lowest-ever rating. **Only consider restaurants with at least 3 ratings, aka rated for at least 3 times (3 scores)!** Using whatever technique you want to use, assign `max_swing` to the name of restaurant that has the maximum swing.
# 
# *Note*: The "swing" is of a specific business. There might be some restaurants with multiple locations; each location has its own "swing".

# The city would like to know if the state of food safety has been getting better, worse, or about average. This is a pretty vague and broad question, which you should expect as part of your future job as a data scientist! However for the ease of grading for this assignment, we are going to guide you through it and offer some specific directions to consider.
# 
# <!--
# BEGIN QUESTION
# name: q7a
# points: 2
# -->

# In[197]:


def swing(s):
    if len(s) < 3:
        return 0
    return max(s) - min(s)

swing_series = ins_named['score'].groupby(ins_named['bid']).agg(swing).rename('swing')

bus_swing = pd.concat([bus.set_index('bid'), swing_series], axis=1).sort_values("swing", ascending=False)
bus_swing

max_swing = bus_swing.iloc[0]['name']
max_swing


# In[198]:


grader.check("q7a")


# <br/><br/><br/>
# 
# ---
# 
# ### Question 7b
# 
# To get a sense of the number of times each restaurant has been inspected, create a multi-indexed dataframe called `inspections_by_id_and_year` where each row corresponds to data about a given business in a single year, and there is a single data column named count that represents the number of inspections for that business in that year. The first index in the MultiIndex should be on `bid`, and the second should be on year.
# 
# For example, a sample row in this dataframe will tell you that for `bid` 573, in `year` 2017, the total number of inspections was 4.
# 
# Hint: Use `groupby` to group based on both the `bid` and the `year`.
# 
# Hint: Use `rename` to change the name of the column to count.
# 
# <!--
# BEGIN QUESTION
# name: q7b
# points: 1
# -->

# In[199]:


inspections_by_id_and_year = ins.groupby([ins['bid'], ins['year']]).size().rename("count").to_frame()
inspections_by_id_and_year.head()


# In[200]:


grader.check("q7b")


# You should see that some businesses are inspected many times in a single year. Let's get a sense of the distribution of the counts of the number of inspections by calling `value_counts`. There are quite a lot of businesses with 2 inspections in the same year, so it seems like it might be interesting to see what we can learn from such businesses.

# In[201]:


inspections_by_id_and_year['count'].value_counts()


# <br/><br/><br/>
# 
# ---
# 
# 
# ### Question 7c
# 
# What's the relationship between the first and second scores for the businesses with 2 inspections in a year? Do they typically improve? For simplicity, let's focus on only 2018 for this problem, using `ins2018` data frame that will be created for you below.
# 
# First, make a dataframe called `scores_pairs_by_business` indexed by `business_id` (containing only businesses with exactly 2 inspections in 2018). This dataframe contains the field score_pair consisting of the score pairs ordered chronologically [first_score, second_score].
# 
# Plot these scores. That is, make a scatter plot to display these pairs of scores. Include on the plot a reference line with slope 1.
# 
# You may find the functions `sort_values`, `groupby`, `filter` and `agg` helpful, though not all necessary.
# 
# The first few rows of the resulting table should look something like:
# 
# |  **bid**   | **score_pair** |
# |-----|------------|
# | 48  | [94, 87]   |
# | 66  | [98, 98]   |
# | 146  | [81, 90]   |
# | 184  | [90, 96]  |
# | 273  | [83, 84]   |
# 
# In the cell below, create `scores_pairs_by_business` as described above.
# 
# Note: Each score pair must be a list type; numpy arrays will not pass the autograder.
# 
# Hint: Use the filter method from lecture 5 to create a new dataframe that only contains restaurants that received exactly 2 inspections.
# 
# Hint: Our code that creates the needed DataFrame is a single line of code that uses `sort_values`, `groupby`, `filter`, `groupby`, `agg`, and `rename` in that order. Your answer does not need to use these exact methods.
# 
# <!--
# BEGIN QUESTION
# name: q7ci
# points: 4
# -->

# In[202]:


ins2018 = ins[ins['year'] == 2018]
# Create the dataframe here
scores_pairs_by_business = (ins2018.sort_values('date').groupby('bid').filter(lambda group: len(group)==2).groupby('bid')
                            .agg({'score': lambda group: group.tolist()}).rename(columns={'score':'score_pair'}))
scores_pairs_by_business.head()


# In[203]:


grader.check("q7ci")


# <!-- BEGIN QUESTION -->
# 
# Now, create your scatter plot in the cell below. It does not need to look exactly the same (e.g., no grid) as the sample below, but make sure that all labels, axes and data itself are correct.
# 
# ![](pics/7c.png)
# 
# Key pieces of syntax you'll need:
# 
# `plt.scatter` plots a set of points. Use `facecolors='none'` and `edgecolors=b` to make circle markers with blue borders. 
# 
# `plt.plot` for the reference line.
# 
# `plt.xlabel`, `plt.ylabel`, `plt.axis`, and `plt.title`.
# 
# Hint: You may find it convenient to use the `zip()` function to unzip scores in the list.
# 
# <!--
# BEGIN QUESTION
# name: q7cii
# points: 2
# manual: True
# -->

# In[204]:


first_score, second_score = zip(*scores_pairs_by_business['score_pair'])

plt.scatter(first_score,second_score,s=20,facecolors='none',edgecolors='b')

plt.plot([55,100],[55,100],'r-')
plt.xlabel('First Score')
plt.ylabel('Second Score')
plt.axis([55,100,55,100])
plt.title("First Inspection Score vs. Second Inspection Score");


# <!-- END QUESTION -->
# 
# <!-- BEGIN QUESTION -->
# 
# <br/><br/><br/>
# 
# 
# ---
# 
# 
# ### Question 7d
# 
# Another way to compare the scores from the two inspections is to examine the difference in scores. Subtract the first score from the second in `scores_pairs_by_business`. Make a histogram of these differences in the scores. We might expect these differences to be positive, indicating an improvement from the first to the second inspection.
# 
# The histogram should look like this:
# 
# ![](pics/7d.png)
# 
# Hint: Use `second_score` and `first_score` created in the scatter plot code above.
# 
# Hint: Convert the scores into numpy arrays to make them easier to deal with.
# 
# Hint: Use `plt.hist()` Try changing the number of bins when you call `plt.hist()`.
# 
# <!--
# BEGIN QUESTION
# name: q7d
# points: 2
# manual: True
# -->

# In[205]:


diffs = np.array(second_score) - np.array(first_score)

plt.hist(diffs, bins=30)
plt.title("Distribution of Score Differences")
plt.xlabel("Score Difference (Second Score - First Score)")
plt.ylabel("Count");


# <!-- END QUESTION -->
# 
# <!-- BEGIN QUESTION -->
# 
# <br/><br/><br/>
# 
# 
# ---
# 
# 
# ### Question 7e
# 
# If restaurants' scores tend to improve from the first to the second inspection, what do you expect to see in the scatter plot that you made in question 7c? What do you oberve from the plot? Are your observations consistent with your expectations? 
# 
# Hint: What does the slope represent?
# 
# <!--
# BEGIN QUESTION
# name: q7e
# points: 1
# manual: True
# -->

# The slope represents the break-even point of restaurants achieving some degree of improvement from the first to the second inspection. If a restaurant does improve between the two inspections, we could assume that the point would lie above the slope. On that same note, if the restaurant does not improve, its point would lie below the slope line of 1. On the scatter plot, we can see that roughly half of the points are above the slope, and half are below. Therefore, we can see that half of the restaurants improved from the first to the second inspection, while the other half regressed.

# <!-- END QUESTION -->
# 
# <!-- BEGIN QUESTION -->
# 
# <br/><br/><br/>
# 
# ---
# 
# ### Question 7f
# 
# If a restaurant's score improves from the first to the second inspection, how would this be reflected in the histogram of the difference in the scores that you made in question 7d? What do you oberve from the plot? Are your observations consistent with your expectations? Explain your observations in the language of Statistics: for instance, the center, the spread, the deviation etc.
# 
# <!--
# BEGIN QUESTION
# name: q7f
# points: 1
# manual: True
# -->

# For the histogram, if a majority of restaurants are improving, the histogram should have generally more positive values than negative or neutral, which should have more values centered towards a positive number or a left skew with a center at a positive value. This is in line with an assumption of there being more improvements than regressions from the first to the second inspection, because a positive difference indicates a higher second inspection score and a lower first inspection score. Instead, the histogram's unimodal, peak values are centered around 0, with the mode being at a value right below 0. This indicates that on average there is no change, or a small regression, between the first and second inspection. We see that this distribution has extreme values at -20 and 30 with lengthy tails on both ends, which centers once again at 0. This is something I expected because the scatter plot shows the same features.

# <!-- END QUESTION -->
# 
# <!-- BEGIN QUESTION -->
# 
# <br/><br/><br/>
# 
# ---
# 
# ### Question 7g 
# To wrap up our analysis of the restaurant ratings over time, one final metric we will be looking at is the distribution of restaurant scores over time. Create a side-by-side boxplot that shows the distribution of these scores for each different risk category from 2017 to 2019. Use a figure size of at least 12 by 8.
# 
# The boxplot should look similar to the sample below. Make sure the boxes are in the correct order!
# 
# ![](pics/7g.png)
# 
# **Hint**: Use `sns.boxplot()`. Try taking a look at the first several parameters. [The documentation is linked here!](https://seaborn.pydata.org/generated/seaborn.boxplot.html)
# 
# **Hint**: Use `plt.figure()` to adjust the figure size of your plot.
# 
# <!--
# BEGIN QUESTION
# name: q7g
# points: 3
# manual: True
# -->

# In[206]:


# Do not modify this line
sns.set()

ins171819 = ins[(ins['year'] >= 2017) & (ins['year'] <= 2019) & (ins['Missing Score'] == False)]
insvio = ins171819.merge(ins2vio, how = "left", left_on = "iid", right_on = "iid")
insvio = insvio.merge(vio, how = "left", left_on = "vid", right_on = "vid")
insvio = insvio[(insvio['risk_category'] == "Low Risk") | (insvio['risk_category'] == "High Risk") | (insvio['risk_category'] == "Moderate Risk")]

plt.figure(figsize = (12,8))
sns.boxplot(x="year", y="score", hue="risk_category", data=insvio, hue_order = ["Low Risk", "Moderate Risk", "High Risk"], linewidth = 1.0)


# <!-- END QUESTION -->
# 
# 
# 
# ## Summary of Inspections Data
# 
# We have done a lot in this project! Below are some examples of what we have learned about the inspections data through some cool visualizations!
# 
# - We found that the records are at the inspection level and that we have inspections for multiple years.
# - We also found that many restaurants have more than one inspection a year.
# - By joining the business and inspection data, we identified the name of the restaurant with the worst rating and optionally the names of the restaurants with the best rating.
# - We identified the restaurant that had the largest swing in rating over time.
# - We also examined the change of scores over time! Many restaurants are not actually doing better.

# <!-- BEGIN QUESTION -->
# 
# <br/><br/><br/>
# 
# ---
# 
# <br/><br/><br/>
# 
# # 8: Open Ended Question 
# ## Question 8a
# 
# ### Compute Something Interesting
# 
# Play with the data and try to compute something interesting about the data. Please try to use at least one of groupby, pivot, or merge (or all of the above).  
# 
# Please show your work in the cell below and describe in words what you found in the same cell. This question will be graded leniently but good solutions may be used to create future homework problems.
# 
# ### Grading ###
# 
# Since the question is more open ended, we will have a more relaxed rubric, classifying your answers into the following three categories:
# 
# - **Great** (4 points): Uses a combination of pandas operations (such as groupby, pivot, merge) to answer a relevant question about the data. The text description provides a reasonable interpretation of the result.
# - **Passing** (1-3 points): Computation is flawed or very simple. The text description is incomplete but makes some sense.
# - **Unsatisfactory** (0 points): No computation is performed, or a computation with completely wrong results.
# 
# 
# **Please have both your code and your explanation in the same one cell below. Any work in any other cell will not be graded.**
# 
# 
# <!--
# BEGIN QUESTION
# name: q8a
# points: 4
# manual: True
# -->
# 
# 

# In[207]:


#YOUR CODE HERE
most_restaurants = bus.groupby('postal5').count().sort_values('bid',ascending=False)['bid']
most_restaurants.head(5)

#ins.iloc[0]

#YOUR EXPLANATION HERE (in a comment)
#First, I sort businesses by their IDs, and sort it in descending order of values associated with the zip code. This allows me to see which zip codes have the most restaurants in the area. 
#Then, because I want to compare the 5 zip codes with the most restaurants, I return the five most options. 94103, which is in San Francisco, is the zip code with the most restaurants. The next four are also different locations in San Francisco. 
#These zip codes are all near each other, in central areas in SF. Funny enough, these areas are also the most affected by coronavirus in the city. 
#The zip codes are South of Market, Inner Mission District, Civic Center, Mission Bay, and Marina District, in that order. These are all highly commercial areas, so it is not surprising to see the high number of restaurants.


# <!-- END QUESTION -->
# 
# 
# 
# <br/><br/><br/><br/>
# 
# ---
# 
# <br/><br/>
# 
# ## Question 8b 
# 
# ### Create some more cool visualizations!
# 
# <br/>

# Play with the data, and try to produce some visualizations to answer one question that you find interesting regarding the data. You might want to use `merge`/`groupby`/`pivot` to process the data before creating visualizations.
# 
# Please show your work in the cells below (feel free to use extra cells if you want), and describe in words what you found in the same cell. This question will be graded leniently, but good solutions may be used to create future homework problems. 
# 
# 
# 

# <!-- BEGIN QUESTION -->
# 
# ### Grading ###
# 
# Since the question is more open ended, we will have a more relaxed rubric, classifying your answers into the following three categories:
# 
# - **Great** (4 points): The chart is well designed, and the data computation is correct. The text written articulates a reasonable metric and correctly describes the relevant insight and answer to the question you are interested in.
# - **Passing** (1-3 points): A chart is produced but with some flaws such as bad encoding. The text written is incomplete but makes some sense.
# - **Unsatisfactory** (0 points): No chart is created, or a chart with completely wrong results.
# 
# We will lean towards being generous with the grading. We might also either discuss in discussion or post on Piazza some examplar analysis you have done (with your permission)!
# 
# You should have the following in your answers:
# * a few visualizations; Please limit your visualizations to 5 plots.
# * a few sentences (not too long please!)
# 
# Please note that you will only receive support in OH and Piazza for Matplotlib and seaborn questions. However, you may use some other Python libraries to help you create you visualizations. If you do so, make sure it is compatible with the PDF export (e.g., Plotly does not create PDFs properly, which we need for Gradescope).
# 
# <!--
# BEGIN QUESTION
# name: q8b
# points: 4
# manual: True
# -->

# In[208]:


# YOUR DATA PROCESSING AND PLOTTING HERE

#VARIABLES TO ORIENT AXES ON GRAPH
rated_geo = bus.merge(ins,how='inner',on='bid').loc[:,['latitude','longitude','score']]
rated_geo = rated_geo[rated_geo['latitude']>30]
rated_geo = rated_geo[rated_geo['latitude']<50]
rated_geo = rated_geo[rated_geo['longitude']<(-100)]
rated_geo = rated_geo[rated_geo['longitude']>(-150)]

min_lon = rated_geo['longitude'].min()
max_lon = rated_geo['longitude'].max()
min_lat = rated_geo['latitude'].min()
max_lat = rated_geo['latitude'].max()
max_score = rated_geo['score'].max()
min_score = rated_geo['score'].min()
bound = ((min_lon, max_lon, min_lat, max_lat))
min_lon, max_lon, min_lat, max_lat
map_bound = ((-122.5200, -122.3500, 37.6209, 37.8249))


fig, ax = plt.subplots(figsize = (11,11))
ax.set_xlim(map_bound[0],map_bound[1])
ax.set_ylim(map_bound[2],map_bound[3])


# Hexbin Plot Creation
hexbinplot = ax.hexbin(rated_geo['longitude'],rated_geo['latitude'],rated_geo['score'],gridsize=125,reduce_C_function=np.size)
fig.colorbar(hexbinplot,ax=ax,label='Inspection Count Number')
plt.title('Restaurant Density & Respective Inspection Counts')
plt.ylabel('Lat')
plt.xlabel('Long')



# YOUR EXPLANATION HERE (in a comment)
# This is a concept I saw in a previous version of this course, and I wanted to reproduce the interesting visualization with a different spin.
# In this version, I wanted to produce a visualization that focuses on the density of restaurants in a visual setting without any geographic orientation, like a map.
# Without knowing specific neighborhoods and locations using a map, it is interesting to see how the cluster of restaurants tend to form in relation to one another.
# By understanding the distribution of restaurant locations throughout the city, we can reverse engineer where we think the most populated areas are  with the most traffic.
# In this case, the area with the most restaurants on the map, approximately (37.8 latitude,-122.4 longitude) is the central area of the city, known as Civic Center. 
# The further you move from Civic Center, both West or South, the lesser restaurants you see, with less inspections per restaurant.


# <!-- END QUESTION -->

# In[209]:


# THIS CELL AND ANY CELLS ADDED BELOW WILL NOT BE GRADED


# ## Congratulations! You have finished Project 1! ##

# ---
# 
# To double-check your work, the cell below will rerun all of the autograder tests.

# In[210]:


grader.check_all()


# ## Submission
# 
# Make sure you have run all cells in your notebook in order before running the cell below, so that all images/graphs appear in the output. The cell below will generate a zip file for you to submit. **Please save before exporting!**

# In[211]:


# Save your notebook first, then run this cell to export your submission.
grader.export("proj1.ipynb")


#  

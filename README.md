# Data Engineer Interview Task

You are provided with historical auction data from Sothebys auction house in `data/sothebys_artists.csv` with information on 100,000 auction sales. This csv includes columns `name`, `title`, `date`, `birth_year`, `death_year`, and `uuid`.

feature | description
--------|-------------
name  | the name of the artist (sometimes these are objects rather than people)
title | the title of the lot (the piece of art)
date | the date the lot was sold at auction
birth_year | the artist's birth year (these values are often missing)
death_year | the artist's death year (these values are often missing)
uuid | a unique identifier for each lot

The goal of this task is to clean artist names, extract birth and death years, and deduplicate and consolidate the data. You will start by writing data from the csv to a database table called SourceArtist. You will then read data from SourceArtist, modify it and write it to CleanedArtist. See below for an example of what the database tables and data should look like before and after:

### SourceArtist

artist | birth | death | title | date | uuid
-------|-------|-------|-------|------|-----
John Marín |||Cape Split, Maine|2017-11-13 21:00:00.985+00| 2c37b3fd-2805-460b-9613-1a295d1cf3ea
John Marin 1870 -- 1953 |||Maple in Autumn|2016-11-21 21:00:00.016+00| 4a20233a-94ea-4c51-8a05-470f1a6bd9bd
John Marin  (1870-1953) ALPINE DISTRICT, NEW JERSEY ||||2000-11-30 15:15:00+00| ccbb7038-5987-4c42-a0a1-7d32afb94bb8
John Marin<br>1872 - 1953 |||Sky Forms and Mountain Forms, Delaware County, Pennsylvania|2009-12-03 15:00:00+00|	9832bd00-2b9d-41ff-b48a-fb78c37a7436
John Minihan (b,1946)		|||Francis Bacon, Paris, 1977|2008-11-18 14:00:00+00|	b2c2d803-4962-4758-8e75-593e19ff4a0b

### CleanedArtist

artist | birth | death | count
-------|-------|-------|------
John Marin | 1870 | 1953| 4
John Minihan | 1946	|| 1

The examples above are non-exhaustive. Notice that John Marin's birth year has been specified as both 1870 and 1872. In this case you should choose the most common year. Additionally, auction data is very noisy. Examples like `1966 World Cup memorabilia` or `20th Century` are not artists. You will need to make decisions about how to handle artists with various birth and death years listed, and when artist names are not actually people. Document these decisions.

## Notes:
- All work should be done in a private Github repository, if you do not have access to your own please let us know and we will create one for you and grant you access to it.
- You are not expected to finish everything. I repeat: **You are not expected to finish everything**. Good solutions will demonstrate strong technical and analytical proficiency, they will not necessary be complete.
- If you require random numbers, please use a seeded random number generator. All of your work done in building this task should be repeatable by a third party (me).
- Answers to the questions below should be done in markdown or latex.
- Please use a Python style guide of your choice and properly document your solutions. Pylint is included in this project. You are free to add and modify a pylintrc file as you see fit.
- Please use the provided Pipfile (package manager & virtualenv) for reproducibility (more details below).
- Please make new commits for each part/subpart (with a relevant commit message) or when it makes sense to do so, and try not to commit broken code.
- You may use any libraries of your choice, but please add them to the Pipfile.
- Please make sure your code is well documented and runnable from within your virtualenv.

## Task:

### Part 1: Data Management

a) Complete schema for CleanedArtist in `models.py` according to: artists as a text field; birth and death year as double fields; count as an integer field. We've written some skeleton code for you. (Note: this is the only code that goes in `model.py`. All other solution code goes in `main.py`)

b) Create a sqlite database called `artists.db` using peewee with the schema defined in `models.py` (see documentation: http://docs.peewee-orm.com/en/latest/peewee/api.html)

c) Read data from the csv into a pandas dataframe, and then use peewee to save this data to the SourceArtist table in `artist.db` and write an accompanying test using pytest verifying that 100,000 rows have been imported.

### Part 2 Data Cleaning
a) Query only the artist, birth, and death data from the SourceArtist table of `artists.db` and load it into a dataframe

b) Use the dataframe from 2(a) to clean the artist field, and save it as a column in a new dataframe for cleaned data (Note: if you are having trouble viewing the data, consider installing http://sqlitebrowser.org/)

c) Again use the dataframe from 2(a) to parse birth and death years out of the artist field, and save them to respective birth and death columns in your cleaned dataframe

d) Perform some simple deduplication of the artist field in your cleaned dataframe — as you do this, keep track of the count of each artist name, which should be added as a new column (this will help you answer Question 1 below)

e) Write your cleaned dataframe to the CleanedArtist table in `artist.db`, and write a test using pytest that involves querying the data from CleanedArtist to confirm your tables look correct.

## Questions:

Please answer each question in one or more sentences (these should all be relatively concise).

1. Who are the 10 most common artists in this dataset? Please answer with a SQL query (include query in your answer)

2. How many artists were born before 1900? Include any python/SQL code used to answer this question.

3. How many artists appear once in the dataset? How confident are you in this number?

4. How did you handle entries where the artist name was not actually a person?

5. Given more time, what else would you have explored? Did you find any interesting insights along the way?

6. Was this fun? Which sections / questions were the most difficult and which were the easiest?

## Before you begin:

* If you are not familiar with Pipenv, read the documentation [here](https://github.com/pypa/pipenv/blob/master/docs/basics.rst)
* Add a `.gitignore` (github maintains a Python `.gitignore` [here](https://github.com/github/gitignore/blob/master/Python.gitignore)).
* This project is designed to work with python 3.6.5. We recommend using [pyenv](https://github.com/pyenv/pyenv) to specify your python version.
* (Optional) Refer to the provided `SETUP.md` file if you need guidance on setting up Pipenv (let us know if you have issues with any commands)

### Authors
* [Michael D'Angelo](http://github.com/mldangelo) (michael.l.dangelo@gmail.com)
* [Basil Vetas](https://github.com/basilvetas)

from os.path import join, realpath, dirname
import pandas as pd
from models import SourceArtist, CleanedArtist, sqlite_db
from peewee import chunked

artist_csv = join(dirname(realpath(__file__)), 'data/sothebys_artists.csv')

### Part 1
# a) SEE models.py

# b)
# Connection to the database
sqlite_db.connect()
# Delete content of the table in case it was not empty
SourceArtist.delete().execute()
# Create the tables from the models
sqlite_db.create_tables([SourceArtist, CleanedArtist])

# c)
# Read data from csv into a dataframe
df = pd.read_csv(artist_csv, infer_datetime_format=True)
# Rename columns
df.columns = ['artist', 'title', 'date', 'birth', 'death', 'uuid']

# Handle missing values for peewee
values = {'artist': '','title':'', 'date':0, 'birth': 0, 'death':0, 'uuid':''}
df.fillna(value=values)
# Convert dataframe to list of dictionaries
dic = df.to_dict(orient='records')

# Insert data to the SourceArtist table by chunks of 100
with sqlite_db.atomic():
    for batch in chunked(dic, 100):
        SourceArtist.insert_many(batch).execute()

print('Number of rows in SourceArtist: {}'.format(SourceArtist.select().count()))
# Test if well inserted
# query = SourceArtist.select(SourceArtist.artist, SourceArtist.birth, SourceArtist.death)
# print(list(query.dicts())[0])

### Part 2
# a) TODO

# b) TODO

# c) TODO

# d) TODO

# e) TODO

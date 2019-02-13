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
# a) Query name, birth and death date
query = SourceArtist.select(SourceArtist.artist, SourceArtist.birth, SourceArtist.death)
artists = pd.DataFrame(list(query.dicts()))
#print(artists.head(100))

# b) Attempt to get cleaned names


def get_name_from_source(name):
    # Get two first words of the field
    return " ".join(name.split(' ')[0:2])


def remove_punctuations(text):
    punctuation_list = ['<', '>', ',', ';', '(', ')', '%', '*']
    for punctuation in punctuation_list:
        text = text.replace(punctuation, ' ')
    return text


cleaned_artists = pd.DataFrame(columns=['artist', 'birth', 'death'])
cleaned_artists['name'] = artists['artist']
# Apply data cleaning on field name
cleaned_artists['name_removed_punc'] = cleaned_artists['name'].apply(remove_punctuations)
cleaned_artists['cleaned_name'] = cleaned_artists['name_removed_punc'].apply(get_name_from_source)
# Remove rows where artist name is probably too short to be a real name
cleaned_artists = cleaned_artists[cleaned_artists['cleaned_name'].map(len) > 2]
print('Number of rows after name cleaning: {}'.format(len(cleaned_artists['cleaned_name'])))

# c) Get dates from Source artist field


def search_date_pattern(name):
    # Look for patterns date-date (eg:1906-1987)
    dates = re.search('\d{4}-\d{4}', name)
    if dates is not None:
        return dates.group(0).split('-')[0]
    else:
        return None


def search_b_date_pattern(name):
    # Look for patterns (eg: b. 1946)
    birth_date = re.search('[bB]\. \d{4}', name)
    if birth_date is not None:
        return birth_date.group(0).split(' ')[1]
    else:
        return None


def get_birth_date_from_source(name):
    if search_b_date_pattern(name) is not None:
        return search_b_date_pattern(name)
    elif search_date_pattern(name) is not None:
        return search_date_pattern(name)
    else:
        return None


def get_death_date_from_source(name):
    dates = re.search('\d{4}-\d{4}', name)
    if dates is not None:
        return dates.group(0).split('-')[1]
    else:
        return None


cleaned_artists['birth_date'] = cleaned_artists['name'].apply(get_birth_date_from_source)
cleaned_artists['death_date'] = cleaned_artists['name'].apply(get_death_date_from_source)
# print(cleaned_artists.head(15))

# d) Artist deduplication

# Keep only relevant rows and rename columns
df_artists = cleaned_artists[['cleaned_name', 'birth_date', 'death_date']]
df_artists.columns = ['artist', 'birth', 'death']

# Get counts for artist appearance and remove redundancy
gp = df_artists.groupby(['artist', 'birth', 'death']).size().reset_index(name='count')
# print(gp.tail(50))

# e) Write dataframe to CleanedArtist table

dic = gp.to_dict(orient='records')
CleanedArtist.delete().execute()
with sqlite_db.atomic():
    for batch in chunked(dic, 100):
        CleanedArtist.insert_many(batch).execute()

print(CleanedArtist.select().count())
query = CleanedArtist.select()
print(list(query.dicts())[0])

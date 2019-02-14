from os.path import join, realpath, dirname
from peewee import Model, TextField, DoubleField, DateTimeField, SqliteDatabase, IntegerField

#data_path = join(dirname(realpath(__file__)), '../data/artists.db')
data_path = join(dirname(realpath(__file__)), "data\\artists.db")
#print(data_path)
sqlite_db = SqliteDatabase(data_path, pragmas={'journal_mode': 'wal'})

class BaseModel(Model):
  """ base class that establishes our connection to our sqlite database """
  class Meta:
    database = sqlite_db
    primary_key = False

class SourceArtist(BaseModel):
  """ model to import uncleaned artist data into """
  artist = TextField()
  birth = DoubleField(null=True)
  death = DoubleField(null=True)
  title = TextField()
  date = DateTimeField()
  uuid = TextField()

### Don't change code above this line - write your code for CleanedArtist schema below ###

### Part 1
# a) TODO

class CleanedArtist(BaseModel):
  """ model for cleaned artist data """
  artist = TextField()
  birth = DoubleField(null=True)
  death = DoubleField(null=True)
  count = IntegerField(null=True)
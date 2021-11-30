from pymongo import MongoClient
import os
import csv
import datetime

client = MongoClient()
db = client['imdb']

errors = db['errors']

# **title.akas.tsv.gz** - Contains the following information for titles:

# * titleId (string) - a tconst, an alphanumeric unique identifier of the title
# * ordering (integer) – a number to uniquely identify rows for a given titleId
# * title (string) – the localized title
# * region (string) - the region for this version of the title
# * language (string) - the language of the title
# * types (array) - Enumerated set of attributes for this alternative title. One or more of the following: "alternative", "dvd", "festival", "tv", "video", "working", "original", "imdbDisplay". New values may be added in the future without warning
# * attributes (array) - Additional terms to describe this alternative title, not enumerated
# * isOriginalTitle (boolean) – 0: not original title; 1: original title

title_akas = db['title.akas']

with open(os.path.join('data', 'title.akas.tsv')) as file:
    tsv = csv.reader(file, delimiter="\t")
    next(tsv)
    count = 0
    for line in tsv:
      count += 1
      if count % 100000 == 0:
        print('title.akas', count)
      try:
        title_akas.insert_one({
          'titleId': line[0],
          'ordering': line[1],
          'title': line[2],
          'region': line[3],
          'language': line[4],
          'types': line[5].split(','),
          'attributes': line[6].split(','),
          'isOriginalTitle': line[7]
        })
      except Exception as e:
        print(e, line)
        errors.insert_one({
          'error': str(e),
          'collection': 'title.akas',
          'line': line,
          'timestamp': datetime.datetime.utcnow()
        })        

# **title.basics.tsv.gz** - Contains the following information for titles:

# * tconst (string) - alphanumeric unique identifier of the title
# * titleType (string) – the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)
# * primaryTitle (string) – the more popular title / the title used by the filmmakers on promotional materials at the point of release
# * originalTitle (string) - original title, in the original language
# * isAdult (boolean) - 0: non-adult title; 1: adult title
# * startYear (YYYY) – represents the release year of a title. In the case of TV Series, it is the series start year
# * endYear (YYYY) – TV Series end year. ‘\N’ for all other title types
# * runtimeMinutes – primary runtime of the title, in minutes
# * genres (string array) – includes up to three genres associated with the title

title_basics = db['title.basics']

with open(os.path.join('data', 'title.basics.tsv')) as file:
    tsv = csv.reader(file, delimiter="\t")
    next(tsv)
    count = 0
    for line in tsv:
      count += 1
      if count % 100000 == 0:
        print('title.basics', count)
      try:
        title_basics.insert_one({
          'tconst': line[0],
          'titleType': line[1],
          'primaryTitle': line[2],
          'originalTitle': line[3],
          'isAdult': line[4],
          'startYear': line[5],
          'endYear': line[6],
          'runtimeMinutes': line[7],
          'genres': line[8].split(',')
        })
      except Exception as e:
        print(e, line)
        errors.insert_one({
          'error': str(e),
          'collection': 'title.basics',
          'line': line,
          'timestamp': datetime.datetime.utcnow()
        })
      
# **title.crew.tsv.gz** – Contains the director and writer information for all the titles in IMDb. Fields include:

# * tconst (string) - alphanumeric unique identifier of the title
# * directors (array of nconsts) - director(s) of the given title
# * writers (array of nconsts) – writer(s) of the given title

title_crew = db['title.crew']

with open(os.path.join('data', 'title.crew.tsv')) as file:
    tsv = csv.reader(file, delimiter="\t")
    next(tsv)
    count = 0
    for line in tsv:
      count += 1
      if count % 100000 == 0:
        print('title.crew', count)
      try:
        title_crew.insert_one({
          'tconst': line[0],
          'directors': line[1].split(','),
          'writers': line[2].split(',')
        })
      except Exception as e:
        print(e, line)
        errors.insert_one({
          'error': str(e),
          'collection': 'title.crew',
          'line': line,
          'timestamp': datetime.datetime.utcnow()
        })

# **title.episode.tsv.gz** – Contains the tv episode information. Fields include:

# * tconst (string) - alphanumeric identifier of episode
# * parentTconst (string) - alphanumeric identifier of the parent TV Series
# * seasonNumber (integer) – season number the episode belongs to
# * episodeNumber (integer) – episode number of the tconst in the TV series

title_episode = db['title.episode']

with open(os.path.join('data', 'title.episode.tsv')) as file:
    tsv = csv.reader(file, delimiter="\t")
    next(tsv)
    count = 0
    for line in tsv:
      count += 1
      if count % 100000 == 0:
        print('title.episode', count)
      try:
        title_episode.insert_one({
          'tconst': line[0],
          'parentTconst': line[1],
          'seasonNumber': line[2],
          'episodeNumber': line[3]
        })
      except Exception as e:
        print(e, line)
        errors.insert_one({
          'error': str(e),
          'collection': 'title.episode',
          'line': line,
          'timestamp': datetime.datetime.utcnow()
        })

# **title.principals.tsv.gz** – Contains the principal cast/crew for titles

# * tconst (string) - alphanumeric unique identifier of the title
# * ordering (integer) – a number to uniquely identify rows for a given titleId
# * nconst (string) - alphanumeric unique identifier of the name/person
# * category (string) - the category of job that person was in
# * job (string) - the specific job title if applicable, else '\N'
# * characters (string) - the name of the character played if applicable, else '\N'

title_principals = db['title.principals']

with open(os.path.join('data', 'title.principals.tsv')) as file:
    tsv = csv.reader(file, delimiter="\t")
    next(tsv)
    count = 0
    for line in tsv:
      count += 1
      if count % 100000 == 0:
        print('title.principals', count)
      try:
        title_principals.insert_one({
          'tconst': line[0],
          'ordering': line[1],
          'nconst': line[2],
          'category': line[3],
          'job': line[4],
          'characters': line[5].split(',')
        })
      except Exception as e:
        print(e, line)
        errors.insert_one({
          'error': str(e),
          'collection': 'title.principals',
          'line': line,
          'timestamp': datetime.datetime.utcnow()
        })

# **title.ratings.tsv.gz** – Contains the IMDb rating and votes information for titles

# * tconst (string) - alphanumeric unique identifier of the title
# * averageRating – weighted average of all the individual user ratings
# * numVotes - number of votes the title has received

title_ratings = db['title.ratings']

with open(os.path.join('data', 'title.ratings.tsv')) as file:
    tsv = csv.reader(file, delimiter="\t")
    next(tsv)
    count = 0
    for line in tsv:
      count += 1
      if count % 100000 == 0:
        print('title.ratings', count)
      try:
        title_ratings.insert_one({
          'tconst': line[0],
          'averageRating': line[1],
          'numVotes': line[2]
        })
      except Exception as e:
        print(e, line)
        errors.insert_one({
          'error': str(e),
          'collection': 'title.ratings',
          'line': line,
          'timestamp': datetime.datetime.utcnow()
        })

# **name.basics.tsv.gz** – Contains the following information for names:

# * nconst (string) - alphanumeric unique identifier of the name/person
# * primaryName (string)– name by which the person is most often credited
# * birthYear – in YYYY format
# * deathYear – in YYYY format if applicable, else '\N'
# * primaryProfession (array of strings)– the top-3 professions of the person
# * knownForTitles (array of tconsts) – titles the person is known for

name_basics = db['name.basics']

with open(os.path.join('data', 'name.basics.tsv')) as file:
    tsv = csv.reader(file, delimiter="\t")
    next(tsv)
    count = 0
    for line in tsv:
      count += 1
      if count % 100000 == 0:
        print('name.basics', count)
      try:
        name_basics.insert_one({
          'nconst': line[0],
          'primaryName': line[1],
          'birthYear': line[2],
          'deathYear': line[3],
          'primaryProfession': line[4].split(','),
          'knownForTitles': line[5].split(',')
        })
      except Exception as e:
        print(e, line)
        errors.insert_one({
          'error': str(e),
          'collection': 'name.basics',
          'line': line,
          'timestamp': datetime.datetime.utcnow()
        })
from pymongo import MongoClient

client = MongoClient()
db = client['imdb']

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
      
# **title.crew.tsv.gz** – Contains the director and writer information for all the titles in IMDb. Fields include:

# * tconst (string) - alphanumeric unique identifier of the title
# * directors (array of nconsts) - director(s) of the given title
# * writers (array of nconsts) – writer(s) of the given title

title_crew = db['title.crew']

# **title.episode.tsv.gz** – Contains the tv episode information. Fields include:

# * tconst (string) - alphanumeric identifier of episode
# * parentTconst (string) - alphanumeric identifier of the parent TV Series
# * seasonNumber (integer) – season number the episode belongs to
# * episodeNumber (integer) – episode number of the tconst in the TV series

title_episode = db['title.episode']

# **title.principals.tsv.gz** – Contains the principal cast/crew for titles

# * tconst (string) - alphanumeric unique identifier of the title
# * ordering (integer) – a number to uniquely identify rows for a given titleId
# * nconst (string) - alphanumeric unique identifier of the name/person
# * category (string) - the category of job that person was in
# * job (string) - the specific job title if applicable, else '\N'
# * characters (string) - the name of the character played if applicable, else '\N'

title_principals = db['title.principals']

# **title.ratings.tsv.gz** – Contains the IMDb rating and votes information for titles

# * tconst (string) - alphanumeric unique identifier of the title
# * averageRating – weighted average of all the individual user ratings
# * numVotes - number of votes the title has received

title_ratings = db['title.ratings']

# **name.basics.tsv.gz** – Contains the following information for names:

# * nconst (string) - alphanumeric unique identifier of the name/person
# * primaryName (string)– name by which the person is most often credited
# * birthYear – in YYYY format
# * deathYear – in YYYY format if applicable, else '\N'
# * primaryProfession (array of strings)– the top-3 professions of the person
# * knownForTitles (array of tconsts) – titles the person is known for

name_basics = db['name.basics']


###############################################################################

title_ratings.update_many({ 'averageRating': { '$gte': 10 } }, {'$set': { 'sample10': True }})

print('updating titles based on averageRating >= 10')
for rating in list(title_ratings.find({ 'averageRating': { '$gte': 10 } })):
  title_akas.update_many({ 'titleId': rating['tconst'] }, {'$set': { 'sample10': True }})
  title_basics.update_many({ 'tconst': rating['tconst'] }, {'$set': { 'sample10': True }})
  title_crew.update_many({ 'tconst': rating['tconst'] }, {'$set': { 'sample10': True }})
  title_episode.update_many({ 'tconst': rating['tconst'] }, {'$set': { 'sample10': True }})
  title_episode.update_many({ 'parentTconst': rating['tconst'] }, {'$set': { 'sample10': True }})
  title_principals.update_many({ 'tconst': rating['tconst'] }, {'$set': { 'sample10': True }})

print('updating the crew')
for crew in title_crew.find({ 'sample10': True }):
  for director in crew['directors']:
    if director == '\\N':
      continue
    name_basics.update_many({ 'nconst': director }, {'$set': { 'sample10': True }})
  for writer in crew['writers']:
    if writer == '\\N':
      continue
    name_basics.update_many({ 'nconst': writer }, {'$set': { 'sample10': True }})

print('updating the names')
for name in name_basics.find({ 'sample10': True }):
  for title in name['knownForTitles']:
    if title == '\\N':
      continue
    title_basics.update_many({ 'tconst': title }, {'$set': { 'sample10': True }})
  title_principals.update_many({ 'nconst': name['nconst'] }, {'$set': { 'sample10': True }})

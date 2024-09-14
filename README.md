# IMDb

## Data Model

https://developer.imdb.com/non-commercial-datasets/

```mermaid
erDiagram
    TITLE["title.basics.tsv.gz"] {
        string tconst PK "alphanumeric unique identifier of the title"
        string titleType "the type/format of the title"
        string primaryTitle "the more popular title / the title used by the filmmakers on promotional materials at the point of release"
        string originalTitle "original title, in the original language"
        boolean isAdult "0: non-adult title; 1: adult title"
        int startYear "represents the release year of a title. In the case of TV Series, it is the series start year"
        int endYear "TV Series end year. '\N' for all other title types"
        int runtimeMinutes "primary runtime of the title, in minutes"
        string[] genres "includes up to three genres associated with the title"
    }
    TITLE_AKA["title.akas.tsv.gz"] {
        string titleId FK "a tconst, an alphanumeric unique identifier of the title"
        int ordering "a number to uniquely identify rows for a given titleId"
        string title "the localized title"
        string region "the region for this version of the title"
        string language "the language of the title"
        string[] types "Enumerated set of attributes for this alternative title"
        string[] attributes "Additional terms to describe this alternative title, not enumerated"
        boolean isOriginalTitle "0: not original title; 1: original title"
    }
    TITLE_CREW["title.crew.tsv.gz"] {
        string tconst FK "alphanumeric unique identifier of the title"
        string[] directors "director(s) of the given title"
        string[] writers "writer(s) of the given title"
    }
    TITLE_EPISODE["title.episode.tsv.gz"] {
        string tconst PK,FK "alphanumeric identifier of episode"
        string parentTconst FK "alphanumeric identifier of the parent TV Series"
        int seasonNumber "season number the episode belongs to"
        int episodeNumber "episode number of the tconst in the TV series"
    }
    TITLE_PRINCIPALS["title.principals.tsv.gz"] {
        string tconst FK "alphanumeric unique identifier of the title"
        int ordering "a number to uniquely identify rows for a given titleId"
        string nconst FK "alphanumeric unique identifier of the name/person"
        string category "the category of job that person was in"
        string job "the specific job title if applicable, else '\N'"
        string characters "the name of the character played if applicable, else '\N'"
    }
    TITLE_RATINGS["title.ratings.tsv.gz"] {
        string tconst FK "alphanumeric unique identifier of the title"
        float averageRating "weighted average of all the individual user ratings"
        int numVotes "number of votes the title has received"
    }
    NAME["name.basics.tsv.gz"] {
        string nconst PK "alphanumeric unique identifier of the name/person"
        string primaryName "name by which the person is most often credited"
        int birthYear "in YYYY format"
        int deathYear "in YYYY format if applicable, else '\N'"
        string[] primaryProfession "the top-3 professions of the person"
        string[] knownForTitles "titles the person is known for"
    }

    TITLE ||--o{ TITLE_AKA : "has"
    TITLE ||--o| TITLE_CREW : "has"
    TITLE ||--o{ TITLE_EPISODE : "has"
    TITLE ||--o{ TITLE_PRINCIPALS : "has"
    TITLE ||--o| TITLE_RATINGS : "has"
    TITLE }o--o{ NAME : "involves"
    NAME ||--o{ TITLE_PRINCIPALS : "participates in"
```

## Star Schema

```mermaid
erDiagram
    TITLE_FACT {
        string tconst PK "Unique identifier"
        string titleType FK "Reference to Title Type dimension"
        boolean isAdult "0: non-adult, 1: adult"
        int startYear "Release year"
        int endYear "End year for TV Series"
        int runtimeMinutes "Runtime in minutes"
        float averageRating "Average rating"
        int numVotes "Number of votes"
    }
    TITLE_TYPE_DIM {
        string titleType PK "Type of title"
        string description "Description of title type"
    }
    TITLE_TEXT_DIM {
        string tconst PK "Unique identifier"
        string primaryTitle "Popular title"
        string originalTitle "Original title"
    }
    GENRE_DIM {
        string genreId PK "Unique identifier for genre"
        string genreName "Name of genre"
    }
    TITLE_GENRE_BRIDGE {
        string tconst FK "Reference to Title"
        string genreId FK "Reference to Genre"
    }
    PERSON_DIM {
        string nconst PK "Unique identifier for person"
        string primaryName "Name of person"
        int birthYear "Birth year"
        int deathYear "Death year"
    }
    PROFESSION_DIM {
        string professionId PK "Unique identifier for profession"
        string professionName "Name of profession"
    }
    PERSON_PROFESSION_BRIDGE {
        string nconst FK "Reference to Person"
        string professionId FK "Reference to Profession"
    }
    TITLE_CREW_BRIDGE {
        string tconst FK "Reference to Title"
        string nconst FK "Reference to Person"
        string role "Director or Writer"
    }
    TITLE_PRINCIPAL_BRIDGE {
        string tconst FK "Reference to Title"
        string nconst FK "Reference to Person"
        string category "Job category"
        string job "Specific job title"
        string characters "Character name(s)"
    }
    EPISODE_DIM {
        string tconst PK "Unique identifier for episode"
        string parentTconst FK "Reference to parent TV Series"
        int seasonNumber "Season number"
        int episodeNumber "Episode number"
    }
    AKA_DIM {
        string akaId PK "Unique identifier for AKA"
        string tconst FK "Reference to Title"
        string title "Alternative title"
        string region "Region for this version"
        string language "Language of the title"
    }

    TITLE_FACT ||--o{ TITLE_GENRE_BRIDGE : "has"
    TITLE_FACT ||--o{ TITLE_CREW_BRIDGE : "has"
    TITLE_FACT ||--o{ TITLE_PRINCIPAL_BRIDGE : "has"
    TITLE_FACT ||--|| TITLE_TEXT_DIM : "has"
    TITLE_FACT ||--|| TITLE_TYPE_DIM : "has"
    TITLE_FACT ||--o{ AKA_DIM : "has"
    TITLE_FACT ||--o| EPISODE_DIM : "may be"
    GENRE_DIM ||--o{ TITLE_GENRE_BRIDGE : "belongs to"
    PERSON_DIM ||--o{ PERSON_PROFESSION_BRIDGE : "has"
    PERSON_DIM ||--o{ TITLE_CREW_BRIDGE : "participates in"
    PERSON_DIM ||--o{ TITLE_PRINCIPAL_BRIDGE : "participates in"
    PROFESSION_DIM ||--o{ PERSON_PROFESSION_BRIDGE : "belongs to"
```
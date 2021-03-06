# tech_miners_test

Simple data retriever from Github. Of course retriever doesn't retrieve all 
data but it is supposed to be easily extended to do so.

## Getting started

Clone the repository
```
git clone https://github.com/1dnorozec/Intelligencia_task.git
```

Create virtual env and install requirements
```buildoutcfg
cd tech_miners_test
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Before we start we need to set up few things.
We assume that postgres database is already existing with existing 
correct schema and tables.

If you have Postgres db already running you can run this small script to 
create tables and schema for extractor to save data to.

```postgres-sql
CREATE SCHEMA github;

CREATE TABLE github.pr_raw (
	id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,	
	raw_data jsonb,	
	run_timestamp INT,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE github.comment_raw (
	id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,	
	raw_data jsonb,	
	run_timestamp INT,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE github.commit_raw (
	id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,	
	raw_data jsonb,	
	run_timestamp INT,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

```

When we have database prepared we need to export few variables to our 
virtual environment. 

 - HOST - database host
 - PORT - port of db 
 - DATABASE - name of database
 - USER - username
 - PASSWORD - password for user
 - AUTH_TOKEN - authentication key for github (see page: [create personal 
 access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token))

When we are all set up we are ready to run the script. When calling the 
script pass argument --owner (owner of the repo) --repo (repository to scrape)

In task case it will be
```sh
python pr_extractor.py --owner contiamo --repo restful-react
```
 
## Reasons to choose GraphQL

The reason to choose GraphQL over REST API was because:

- There was no well documentation about exact fields that endpoint is 
returning (or at least I couldn't find it)
- REST API returns a lot of repeating data
- With the REST API I couldn't find simple way to filter out `pr` results by 
`updated date` while it is possible by GraphQL in `search` query
- We can get exactly what we need.

## Reasons to store data in Postgres / ELT instead of ETL

Since we use GraphQl we will have data that is already pretty standardized. 
If we store raw data in jsonb fields we can easily normalize and transform 
data in Postgres.
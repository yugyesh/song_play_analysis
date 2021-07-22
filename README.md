# SONG PLAY ANALYSIS

## Propose of the project
This project has been developed in order to understand the the songs listening behavior of the music streaming application.

## Project Requirements
- Model a relational database to store data collected on songs and user activity
- Write an ETL pipeline to store the data into the database.

## About datasets
- The songs data are in JSON format
- The log data are in JSONL format

## Tech stack
- Python
- Postgres
- Notion for project management
- Github for Version control
- List of libraries are defined in the [libraries&#46;md](https://github.com/yugyesh/song_play_analysis/blob/V1.0/libraries.md) file

## Usage manual
- Create .env file to store username and password of the database
- Store all log_data and song_data inside the data directory
- Execute create_tables.py program to create the database and required tables based on designed schema.
- Execute `etl.py` to extract the data from the data folder, processes the data and store it inside the database
- Use command line to execute the programs, in command line type python `filename.py` to execute. For e.g. python `etl.py`.

## Files description
The project consists of three major files
### sql_queries.py
This file consists of all sql queries

### create_tables.py
It performs operation using sql_queries

- Establish connection with database
- Drops table 
- Creates table

### etl&#46;py
This program is a pipeline for the project that 
- Extracts the song data and log data from the json file
- Process the data that matches the database model schema
- And, stores the processed data into the database.

## Additional files
The project also consists of additional files such as:
- etl.ipynb: It describes the process of ETL script
- [libraries&#46;md](https://github.com/yugyesh/song_play_analysis/blob/V1.0/libraries.md): Lists the name of used third party libraries
- Pipfile: To mange project dependencies
- .pylintrc: Defines linting rules in the project
- [commit_rules.md](https://github.com/yugyesh/song_play_analysis/blob/master/commit_rules.md): Defines the commit rules for the project

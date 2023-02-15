# Terrascope Assignment
==============================

This projects showcases a data ingestion and query workflow involving the following components:
  * **MySQL** database for data storage
  * **loader** service for loading data from CSV files and into the database
  * **reader** service for reading data from the database and writing an aggregate statistic to a JSON file

In addition, an exploratory data analysis (EDA) was performed beforehand.

## Setup

### Project Organization


    ├── .gitignore
    ├── LICENSE
    ├── README.md                  <- The top-level README for developers using this project.
    |
    ├── data
    │   ├── misc                   <- Additional data not directly used by the application, e.g. sample data.
    │   └── raw                    <- The original, immutable data dump. Put people.csv and places.csv here.
    |
    ├── notebooks                  <- Jupyter notebooks for EDA and experimentation.
    │
    ├── reports                    <- Generated analysis, e.g. summary_output.json
    │
    ├── requirements.txt           <- The requirements file for reproducing the analysis environment
    │
    └── src
        ├── loader                 <- Scripts for the loader service
        |   ├── config.py          <- Configuration file, loads config from the container environment
        |   ├── dockerfile         <- Docker file to build the loader image
        |   ├── loader.py          <- The actual loader code
        |   ├── loader.sql         <- An alternative implementation in pure SQL; for reference only and not used by the container
        │   └── requirements.txt   <- Requirement file to build the python environment in the container
        │
        ├── reader
        │   ├── config.py          <- Configuration file, loads config from the container environment
        |   ├── dockerfile         <- Docker file to build the reader image
        |   ├── reader.py          <- The actual reader code
        │   └── requirements.txt   <- Requirement file to build the python environment in the container
        │
        └── stack.yml              <- Docker-compose file to run all containers

This project was initialized with the [cookiecutter data science template](https://github.com/drivendata/cookiecutter-data-science). The folder structure has been modified to fit the needs of this project.

## Working with the Repository

### Exploratory Data Analysis (EDA)

Assuming `conda` is available in your shell you can run the following from the root of this repository to create and activate an anaconda environment called `Terrascope`, and to run the `jupyter notebook` server:

```
conda env create --file environment.yml
conda activate Terrascope
jupyter notebook notebooks/data_analysis.ipynb
```

### Deployment

The application consists of three containers. A docker compose file is available to run and orchestrate these services.
The `stack.yml` file expects the input CSVs (`people.csv` and `places.csv`) to be located in `data/raw/`. The output will be written to `reports/summary_output.json`. Adjust the configuration, if necessary.

Finally call:
```
docker-compose -f src/stack.yml up
```

Chances are, that the `loader` and `reader` services are started before the database container has been fully initialized. Both containers will terminate with a non-zero exit code since the database can't be reached yet. For that reason `loader` and `reader` containers are set to restart up to 10 times. This should suffice to address that situation. 

### Implementation

Both services, `loader` and `reader`, utilize the popular `SQLAlchemy` python package to connect to databases and define the ORM. The `pymysql` package is used as driver to connect to MySQL. The `pandas` package is used to conveniently handle tabular data, read CSV and convert tables to JSON. `pydantic` is used for data validation and settings management. For both containers, the database configuration is loaded and validated from the respective container's environment variables.

#### Loader

The `loader` service uses a simple data model with 2 tables. The tables are created, if they don't exist. Next, all CSV files under `/data` are loaded into a dictionary. A database connection and corresponding session are created via context managers. A loop iteratively writes the data to the database. SQL and database driver exceptions/errors will terminate the container with an exit code of `1`. Loading all CSV files beforehand is a trade-off of using more RAM for loading all data at once while keeping the database connection open for a shorter period of time.

#### Reader

The `reader` service creates a database connection in the same fashion as the `loader`. It then runs a SQL query against the database. The result is converted into a `pandas.Series` and written to JSON, i.e. `/data/summary_output.json`.
The SQL query creates an inner join of the `people` and `places` table, matched on `place_of_birth` and `city` respectively. Finally a count is computed by grouping the result by `country`.

## Ideas for Improvement

### Code
  * Refactor code: extract database models, performance optimization, make magic values configurable
  * Make logging configurable
  * At the moment, the `loader` and `reader` containers stop after their task has been completed. The services could be implemented in a way, that they run REST APIs that can be used continuously to load and query data.
  * Reimplement the application in Rust, if performance really matters

### Data Model
  * Introduce foreign key constraints, e.g. to cascade updates
  * For large tables, use partitioning
  * For large tables, create an aggregate table to reduce runtime load from queries
  

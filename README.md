# Terrascope Assignment
==============================

This projects showcases a data ingestion and query workflow involving the following components:
  * **MySQL** database for data storage
  * **loader** service for loading data from file and into the database
  * **reader** service for reading data from the database and writing an aggregate statistic to a file

In addition, an exploratory data analysis (EDA) was performed beforehand.

## Setup

Project Organization
------------

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
        |   ├── loader.sql         <- An alternative implementation in pure SQL
        │   └── requirements.txt   <- Requirement file to build the python environment in the container
        │
        ├── reader
        │   ├── config.py          <- Configuration file, loads config from the container environment
        |   ├── dockerfile         <- Docker file to build the reader image
        |   ├── reader.py          <- The actual reader code
        │   └── requirements.txt   <- Requirement file to build the python environment in the container
        │
        └── stack.yml              <- Docker-compose file to run all containers


## Working with the Repository

### Exploratory Data Analysis (EDA)

Assuming `conda` is available in your shell you can run the following from the root of this repository to create and activate an anaconda environment called `Terrascope`, and to run the `jupyter notebook` server:

```
conda env create --file environment.yml
conda activate Terrascope
jupyter notebook notebooks/data_analysis.ipynb
```

### Deployment

The application consists of three containers. A docker compose file has been provided to run and orchestrate the services.
The `stack.yml` file expects the input CSVs to be located in `data/raw`. The output will be written to `reports/summary_output.json`. Adjust the file, if necessary.

Finally call `docker-compose -f src/stack.yml up`.

Chances are, that the loader and reader services are started before the database container has been fully initialized. Both containers will terminate with a non-zero exit code, since the database can't be reached yet. For that reason reader and loader containers are set to restart up to 10 times. This should suffice to address that situation. 

### Implementation

Both services, loader and reader, utilize the popular `SQLAlchemy` python package to connect to databases and define the ORM. The `pymysql` package is used as driver to connect to MySQL.

#### Loader

#### Reader

## Ideas for Improvement

  * Refactor code: extract database models, performance optimization, make magic values configurable
  * Make logging configurable
  * At the moment, the loader and reader containers stop after their task is completed. The services could be implemented in a way, that they run REST APIs that can be used continuously to load and query data.
  * Reimplement the application in Rust if performance really matters
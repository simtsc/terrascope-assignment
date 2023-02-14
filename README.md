# Terrascope Assignment
==============================

This projects showcases a data ingestion and retrieval workflow involving the following components:
  * _MySql_ database for data storage
  * _loader_ service for loading data from file and into the database
  * _reader_ service for reading data and writing an aggregate statistic to file

In addition, a exploratory data analysis (EDA) was performed beforehand.

## Setup

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    |
    ├── data
    |
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    └── src                <- Source code for use in this project.
        ├── data           <- Scripts to download or generate data
        │
        ├── loader         <- Scripts to turn raw data into features for modeling
        │   └── build_features.py
        │
        ├── reader         <- Scripts to train models and then use trained models to make
        │   │                 predictions
        │   ├── predict_model.py
        │   └── train_model.py
        │
        └── stack.yml      <- Scripts to create exploratory and results oriented visualizations

## Ideas fir Improvement

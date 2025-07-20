
# Crypto Data Enrichment
A project to extract, transform and load enriched data to db which is available to general users by making api requests.

This application has following parts

### ETL Portion
Includes data extraction from API, data processing by cleaning it, conforming it to quality data standards and adding metrics to data like percentage change, volatility and others.

### Pipeline Portion
Configuring airflow and writing a dag fro this application so that application script can run automatically at the specified periodic intervals of time.

### Data Serving Portion
Written an API using Fast API module so that all relevant users can access the enriched data by making standard api request which takes input values in standard format and respond with a json payload.

### Deployment Portion
All parts involved in this application are deployed on docker so that all of the app is portable, easy to configure and debug, all tool are configuration are made using a docker compose application which you can see in the airflow-deployment.yaml file.


## Application Architecture Diagram

![App Screenshot](https://drive.google.com/file/d/1KrRAE80AR9Qd3l5udaomXYUzf1tl3ujh/view?usp=drive_link/468x300?text=App+Screenshot+Here)


## Tech Stack

**Data Processing:** Python 3.12

**Database:** Postgres:15

**Pipeline:** Airflow:2.7.3

**Data Serving:** Public API - build using Fast API Module

**Deployment:** Docker:28.2.2


## Run Locally

Clone the project

```bash
  git clone https://github.com/saimnaveed/Big-Data/tree/54c4366198897ddd8b4599679ce380eb93b99645/Crypto%20Data%20Enrichment%20ETL
```

Go to the project directory

```cmd/powershell
  cd < project directory name ..,>
```

Starting DOcker Compose Application

```cmd/powershell
  docker compose -f airflow-deployment.yaml up
```

Making API Request 1

```https request made on web browser make on local host or on configured ip address with choosen port no

  https:127.0.0.1:8000/prices?coin='ETHUSDT'&start_date='...'&end_date='...'
```

Making API Request 2

```https request made on web browser make on local host or on configured ip address with choosen port no

  https:127.0.0.1:8000/metrics/volatility?coin='BTCUSDT'&period=8d
```

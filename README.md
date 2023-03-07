# The largest heading
## The second largest heading
###### The smallest heading


# Spyrk-cluster: um mini-laboratório de dados
A ideia do projeto é montar um data lake com informações vindo de alguma base externa, seguindo o fluxo do dia a dia de uma area de engenharia de dados contemplando controle de código e teste.

## Estrutura disponibilizasa em container docker contendo:

1. Spark:3.0.0
2. Hadoop:
3. PostgreSql
4. Airflow
5. Jupyter Notebook

## Iniciar container
Execute `bash master-build.sh` para iniciar os containers.

## Atualizando as dags 
docker exec -it --user airflow airflow-scheduler bash -c "airflow dags list"
docker build . --tag pyrequire_airflow:2.5.1


### 


<!-- ABOUT THE PROJECT -->
## About The Project

Purpose for this tutorial is to show how to get started with Hadoop, Spark and Jupyter for your BigData solution, deploy as Docker Containers.

![Architecture overview][arch]

## Pre-requisite
- Only confirmed working on Linux/Windows (Apple Silicon might have issues).
- Ensure Docker is installed.

## Start

Execute `bash master-build.sh` to start the the build and start the containers.

### Hadoop
Access Hadoop UI on ' http://localhost:9870 '

### Spark
Access Spark Master UI on ' http://localhost:8080 '

### Jupyter
Access Jupyter UI on ' http://localhost:8888 '


### Airflow
Access Jupyter UI on ' http://localhost:8280 '
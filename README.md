# GFT processo  - Serasa
O objetivo desse ambiente é simular um processo de data lake, onde é feito a consultar aos dados externos (Nesse caso utlizei a fonte do governo: https://opendatasus.saude.gov.br/dataset/registro-de-ocupacao-hospitalar-covid-19), onde foi feito uma busca por arquivos no diretorio, executando o download do mesmo, enviando para o HDFS, e executando as tratativas dos dados para consultas futuras, mantendo historico dos mesmo 4

Para iniciar os containers basta executar o comando 'make build' que carregara o arquivo na pasta docker

## Projeto desenvolvido para apresentar uma estrutura de data lake, onde foram utlizados os seguintes recursos:
* postgres: 
* Airflow:
* jupyter:
* Spark:
* Hadoop HDFS:
* Hadoop Yarn:


## Estrutura do projeto 
    -GTF-PROCESSO
    --airflow ('Responsável por carregar dags, logs e plugins a serem executadas')
    ---dags
    ----startProcessoRaw ('Inicia o processo acessado os arquivos da pasta covid-app')
    ---logs
    ---plugins
    -covid-app (Projeto contendo o código para executar os processo)
    --src
    ---carga (Classes de execuções - responsável por executar e carregar dados tanto de fonte externa como para dentro do hdfs)
    ----processaCovidRaw.py 
    ----processaCovidTrusted.py
    ----processaCovidRefined.py
    ---utils (Classes responsáveis por requisiões de varios bloco de código )
    ----connectionClass.py
    ----functionClass.py
    ---startProcessoRaw.py (Responsável por iniciar os códigos de processamento dos dados)
    --src-test (Estrutura de teste )

## Processo de extração de informações
#### Nesse projeto criei uma estrutura de armazenamento de arquivos direto no HDFS onde os dados seguem essa sequencia de ingestão e tratamentos
        1 raw
        2 trusted
        3 refined 
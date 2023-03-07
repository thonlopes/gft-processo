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

## Árvore do diretório
        .
        ├── airflow
        │   ├── dags
        │   │   └── startProcessoRaw.py
        │   ├── logs
        │   ├── plugis
        ├── covid-app
        │   ├── src
        │   │   ├── carga
        │   │       │   ├── processaCovidRaw.py
        │   │       │   ├── processaCovidTrusted.py
        │   │       │   ├── processaCovidRefined.py
        │   │   ├── utils
        │   │       │   ├── connectionClass.py
        │   │       │   ├── functionClass.py
        │   │   ├── startProcesso.py
        │   ├── src-teste
        ├── docker
        │   ├── airflow
        │   │   ├── Dockerfile
        │   ├── hadoop
        │   │   ├── base
        │   │       ├── Dockerfile
        │   │       ├── entrypoint.sh
        │   │   ├── datanode
        │   │       ├── Dockerfile
        │   │       ├── run.sh
        │   │   ├── historyserver
        │   │       ├── Dockerfile
        │   │       ├── run.sh
        │   │   ├── namenode
        │   │       ├── Dockerfile
        │   │       ├── run.sh
        │   │   ├── nodemanager
        │   │       ├── Dockerfile
        │   │       ├── run.sh
        │   │   ├── resourcemanager
        │   │       ├── Dockerfile
        │   │       ├── run.sh
        │   │   └── hadoop.env
        │   ├── jupyter
        │   │   ├── Dockerfile
        │   │   └── workspace
        │   └── spark
        │   │   ├── base
        │   │       ├── Dockerfile
        │   │   ├── master
        │   │       ├── Dockerfile
        │   │   ├── worker
        │   │       ├── Dockerfile
        │   ├── docker-compose.yml
        │   ├── Makefile
        ├── README.md


## Processo de extração de informações
#### Nesse projeto criei uma estrutura de armazenamento de arquivos direto no HDFS onde os dados seguem essa sequencia de ingestão e tratamentos
        1 raw
        2 trusted
        3 refined 


## diretório do projeto
### covid-app
    Toda a estrutura do código esta dentro do diretorio covid-app, esse diretorio esta separada em algumas camadas como:
      * src: raiz do arquivos principais
      ** src/carga: Responsável por executar as rotinas de download dos arquivos, trativas e disponibilização para uso na refined seguindo a regra de negócio.
         *** processaCovidRaw.py
         *** processaCovidTrusted.py
         *** processaCovidRefined.py
     
      ** src/utils: Responsável por executar funções padrões como: iniciar sessão do spark, leitura de arquivos, e gravação no hdfs, podendo inserir mais funções seguindo padrões.
         *** connectionClass.py:
         *** functionClass.py:

      ** startProcesso.py - Responsável por exeuctar o processo de ponta a ponta, fazendo as chamadas as funcções na pasta carga.

      * src-teste: raiz dos arquivos de teste

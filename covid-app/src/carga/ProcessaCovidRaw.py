#! /usr/bin/env /usr/local/bin/python3.3
import os
from pyspark.sql.types      import *
from pyspark.sql            import SparkSession 
from pyspark.sql.functions  import *
from pyspark                import SparkFiles
from datetime               import datetime, timedelta
from utils.ConnectionClass  import *
from utils.FunctionClass  import *
import requests


class ProcessaCovidRaw():
        
       
        def __init__(self):
                self.ConnectionClass = ConnectionClass()
                self.FunctionClass   = FunctionClass()
                        
        def main(self):
                
                ######### varias basicas de controle ###########
                appNameSpark = "Carrega dados covid"
                hdfsNode = "hdfs://hadoop-namenode:9000/gft/"
                path_load = "covid/raw/"
                 ######### inicia a sessão no spark ###########
                spark = self.ConnectionClass.spark_session_gft(appNameSpark)
                
                dtFolderLoad = datetime.today() - timedelta(days=2)
                dtFolderLoad = str(dtFolderLoad.strftime('%Y-%m-%d'))
                
                urlGov = 'https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/LEITOS/'
                csvName = "esus-vepi.LeitoOcupacao_202"
                qtsAnos = 1
                
                try:
                        ## CARREGA TODOS OS ARQUIVOS E DATAFRAMES 
                        for ano in range(qtsAnos):
                                url  = str(urlGov) + dtFolderLoad +"/"+ csvName + str(ano) + ".csv"
                                
                                if requests.get(url).status_code == 200:
                                
                                        print("O servidor está disponível." + url)  
                                        spark.sparkContext.addFile(url)
                                        df = spark.read.csv(SparkFiles.get(csvName + str(ano) + ".csv"),inferSchema=False, header=False,  sep =',',  multiLine=True)
                                
                                        # df = df.withColumn('dtFolderLoad', dtFolderLoad)
                                        df = df.withColumn('dtLoadDate', current_date())

                                        df.write.option("header", False)\
                                                .mode("overwrite") \
                                                .partitionBy("dtLoadDate")\
                                                .csv(hdfsNode + path_load)
                                        
                                      
                                else: 
                                        print("O servidor está indisponível.") 
                        spark.stop()

                except Exception as e:
                        erro = str(e)
                        print(erro)
                        raise

                return 
                        

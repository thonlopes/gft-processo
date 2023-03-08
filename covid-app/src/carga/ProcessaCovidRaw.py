import os
from pyspark.sql.types      import *
from pyspark.sql            import SparkSession 
from pyspark.sql.functions  import *
from pyspark                import SparkFiles
from datetime               import datetime, timedelta
from utils.connectionClass  import *
from utils.functionClass  import *
import requests


class processaCovidRaw():
        
       
        def __init__(self):
                self.connectionClass = connectionClass()
                self.functionClass   = functionClass()
                        
        def main(self):
                
                ######### varias basicas de controle ###########
                appNameSpark = "Carrega dados covid"
                hdfsNode = "hdfs://hadoop-namenode:9000/gft/raw/covid"
                 ######### inicia a sessão no spark ###########
                spark = self.connectionClass.spark_session_gft(appNameSpark)
                
                dtFolderLoad = datetime.today() - timedelta(days=2)
                dtFolderLoad = str(dtFolderLoad.strftime('%Y-%m-%d'))
                
                urlGov = 'https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/LEITOS/'
                csvName = "esus-vepi.LeitoOcupacao_202"
                anos = 1
                header = True
                delimiter = ","
                encoding = "UTF-8"
                
                try:
                        ## Carrega a quantidade de anos selecionado na variavel, buscar dentro do diretorio da url goc e vê qual data esta disponivel 
                        for ano in range(anos):
                                urlFile  = str(urlGov) + dtFolderLoad +"/"+ csvName + str(ano) + ".csv"
                                csvName = str(csvName + str(ano) + ".csv")
                                if requests.get(urlFile).status_code == 200:
                                        
                                        self.functionClass.import_csv(spark, 
                                                                hdfsNode, 
                                                                header, 
                                                                delimiter, 
                                                                encoding, 
                                                                urlFile,
                                                                csvName)
                        
                                else: 
                                        print("O servidor está indisponível.") 
                except Exception as e:
                        erro = str(e)
                        print(erro)
                        raise

                return 
                        

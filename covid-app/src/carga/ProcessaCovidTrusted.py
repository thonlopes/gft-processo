import os
from pyspark.sql.types      import *
from pyspark.sql            import SparkSession 
from pyspark.sql.functions  import *
from pyspark                import SparkFiles
from datetime               import datetime, timedelta
from utils.ConnectionClass  import *
from utils.FunctionClass  import *
import requests

class ProcessaCovidTrusted():
                
        def __init__(self):
                self.ConnectionClass = ConnectionClass()
                self.FunctionClass = FunctionClass()
                
        def main(self):
                
                ######### varias basicas de controle ###########
                appNameSpark = 'Carrega dados covid Trusted'
                hdfsNode = "hdfs://hadoop-namenode:9000/gft/"
                path_load = "covid/raw/"
                path_trusted = "covid/trusted/"

                ######### inicia a sessão no spark ###########
                spark_session_gft = self.ConnectionClass.spark_session_gft(appNameSpark)
                
                try:
                    
                    fileSchema = StructType([StructField('_c0', StringType(),True),
                         StructField('_id', StringType(),True),
                         StructField('dataNotificacao', StringType(),True),
                         StructField('cnes', StringType(),True),
                         StructField('ocupacaoSuspeitoCli', StringType(),True),
                         StructField('ocupacaoSuspeitoUti', StringType(),True),
                         StructField('ocupacaoConfirmadoCli', StringType(),True),
                         StructField('ocupacaoConfirmadoUti', StringType(),True),
                         StructField('ocupacaoCovidUti', StringType(),True),
                         StructField('ocupacaoCovidCli', StringType(),True),
                         StructField('ocupacaoHospitalarUti', StringType(),True),
                         StructField('ocupacaoHospitalarCli', StringType(),True),
                         StructField('saidaSuspeitaObitos', StringType(),True),
                         StructField('saidaSuspeitaAltas', StringType(),True),
                         StructField('saidaConfirmadaObitos', StringType(),True),
                         StructField('saidaConfirmadaAltas', StringType(),True),
                         StructField('origem', StringType(),True),
                         StructField('_p_usuario', StringType(),True),
                         StructField('estadoNotificacao', StringType(),True),
                         StructField('municipioNotificacao', StringType(),True),
                         StructField('estado', StringType(),True),
                         StructField('municipio', StringType(),True),
                         StructField('excluido', StringType(),True),
                         StructField('validado', StringType(),True),
                         StructField('_created_at', StringType(),True),
                         StructField('_updated_at', StringType(),True),
                         StructField('dt_folder', DateType(),True)
    
                    ])
                    
                    df = spark_session_gft.read.csv(hdfsNode + path_raw + csvName, schema= fileSchema, header=True, sep=",", multiLine=True)
                    
                    df.write.option("header",True) \
                      .mode("append") \
                      .partitionBy("dt_folder","estado")\
                      .parquet(hdfsNode + path_trusted)
                      
                    spark_session_gft.stop()

                except Exception as e:
                        erro = str(e)
                        print(erro)
                        raise

                return 
                        

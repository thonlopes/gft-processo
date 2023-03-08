import os
from pyspark.sql.types      import *
from pyspark.sql            import SparkSession 
from pyspark.sql.functions  import *
from datetime               import datetime, timedelta
from utils.connectionClass  import *
from utils.functionClass  import *

class processaCovidRefined():
                
        def __init__(self):
                self.connectionClass = connectionClass()
                self.functionClass = functionClass()
                
        def main(self):
                
                appNameSpark = 'Carrega dados covid Trusted'
                hdfsNodeTrusted = "hdfs://hadoop-namenode:9000/gft/trusted/covid"
                hdfsNodeRefined = "hdfs://hadoop-namenode:9000/gft/refined/covid/"

                ######### inicia a sessão no spark ###########
                spark = self.connectionClass.spark_session_gft(appNameSpark)
                
                try:
                    
                    header = True
                    delimiter = ","
                    self.functionClass.save_parquet_refined(spark, 
                                                    hdfsNodeTrusted,
                                                    hdfsNodeRefined, 
                                                    header, 
                                                    delimiter)
        

                except Exception as e:
                        erro = str(e)
                        print(erro)
                        raise

                return 
                        
import os
from pyspark.sql.types      import *
from pyspark.sql            import SparkSession 
from pyspark.sql.functions  import *
from datetime               import datetime, timedelta
from utils.connectionClass  import *
from utils.functionClass  import *

class processaCovidTrusted():
                
        def __init__(self):
                self.connectionClass = connectionClass()
                self.functionClass = functionClass()
                
        def main(self):
                
                appNameSpark = 'Carrega dados covid Trusted'
                hdfsNodeRaw = "hdfs://hadoop-namenode:9000/gft/raw/covid"
                hdfsNodeTrusted = "hdfs://hadoop-namenode:9000/gft/trusted/covid/"

                ######### inicia a sessão no spark ###########
                spark = self.connectionClass.spark_session_gft(appNameSpark)
                
                try:
                        schema = StructType([ \
                                StructField('_c0', StringType(),True),
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
                                StructField('_updated_at', StringType(),True)       
                        ])
                    
                        header = True
                        delimiter = ","
                        encoding = "UTF-8"
                        campos = ""
                        self.functionClass.save_parquet(spark, 
                                                        hdfsNodeRaw,
                                                        hdfsNodeTrusted, 
                                                        header, 
                                                        delimiter, 
                                                        encoding, 
                                                        schema,
                                                        campos)

                except Exception as e:
                        erro = str(e)
                        print(erro)
                        raise

                return 
                        

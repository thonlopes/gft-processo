from pyspark.sql import SparkSession

class ConnectionClass():
    def spark_session_gft( self, appNameSpark,):
        try:
            spark = SparkSession.builder \
                                    .config('spark.executor.memory', '1g') \
                                    .config('spark.driver.memory', '1g') \
                                    .config("spark.driver.maxResultSize", "1048MB") \
                                    .config("spark.port.maxRetries", "100")\
                                    .appName(appNameSpark) \
                                    .getOrCreate()
                                                        
                                    
            print ("sessão: " + appNameSpark + "crida com sucesso")
            return spark

        except Exception as e:
            erro = str(e)
            print(erro)
            raise

            
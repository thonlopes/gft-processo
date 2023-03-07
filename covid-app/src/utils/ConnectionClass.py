from pyspark.sql import SparkSession

class connectionClass():
    def spark_session_gft( self, appNameSpark,):
        try:
            spark = SparkSession.builder \
                                    .master("local[1]")\
                                    .appName(appNameSpark) \
                                    .getOrCreate()
                                                        
            print ("sessão: " + appNameSpark + "crida com sucesso")
            return spark

        except Exception as e:
            erro = str(e)
            print(erro)
            raise

            
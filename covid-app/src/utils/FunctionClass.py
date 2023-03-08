from pyspark.sql.types      import *
from pyspark.sql.functions  import *
from pyspark                import SparkFiles



class functionClass():
    
    def import_csv(self, spark, hdfsNode, header, delimiter, encoding, urlFile,csvName):

        try:
             print("O servidor está disponível." + urlFile)  
             
             spark.sparkContext.addFile(urlFile)
             df = spark.read.csv(SparkFiles.get(csvName),inferSchema=True, header=header, sep =delimiter,  multiLine=True)                                        # df = spark.read.csv(SparkFiles.get(csvName),inferSchema=True, header=True,  sep =',',  multiLine=True)
    
             df = df.withColumn('dt_load_date', lit(current_timestamp()))
             df = df.withColumn('dt_insert', lit(current_timestamp()))
        
             df.write.option("header",True)\
                    .mode("append") \
                    .partitionBy("dt_load_date")\
                    .csv(str(hdfsNode))
                                            
        except Exception as e:
                    erro = str(e)
                    print(erro)
                    raise
        return
    
    def save_parquet(self, spark, hdfsNodeRaw,hdfsNodeTrusted, header, delimiter, encoding, schema,
                  dropDuplicate=True,have_dt_load=True):
        
        try:
            #Valor vindo da assinatura do método
            if have_dt_load:
                dt_load = self.listDtLoads( delimiter, hdfsNodeRaw ,spark)
                #for dt_load in lista_dt_load:

            df = spark.read\
                .option('header', header)\
                .option('delimiter', delimiter)\
                .option("escape", "\"")\
                .csv(str(hdfsNodeRaw))\
            
           #Valor vindo da assinatura do método
            if have_dt_load:
                df_max = df.select(col('dt_load_date'))\
                    .agg(max(col('dt_load_date')).alias('dt_load_date'))

                df = df.join(df_max, ((df.dt_load_date == df_max.dt_load_date)), how='inner')\
                    .drop(df_max.dt_load_date)

            df = df.withColumn('id_hash', sha2(concat_ws('|', *df.columns), 256))
            
            #Valor vindo da assinatura do método
            if have_dt_load:
                df_duplicates = df.withColumn('dt_load_date', col("dt_load_date"))
            else:
                df_duplicates = df.withColumn('dt_load_date', lit(current_timestamp()))
            df_duplicates = df_duplicates.withColumn('dt_insert', lit(current_timestamp()))


            ## Cria DF vazio, na estrutura e nomenclatura dos campos da analysis
            df_final = spark.createDataFrame(spark.sparkContext.emptyRDD(),schema)

            df_final = df_final\
                .withColumn('id_hash',lit(None).cast(StringType()))\
                .withColumn('dt_load_date',lit(None).cast(StringType()))\
                .withColumn('dt_insert',lit(None).cast(TimestampType()))\
            #df_final.cache().count()

            # Insere dados na estrutura final
            df_resultado = df_final.union(df_duplicates)
            
            df_resultado.write\
                        .mode('append')\
                        .parquet(str(hdfsNodeTrusted))
                        
        except Exception as e:
            print(str(e))
            raise
        return
    
    def listDtLoads(self, delimiterIngress, pthRaw, spark):
        dfData = spark.read\
            .option('header', False)\
            .option('delimiter', delimiterIngress)\
            .csv(str(pthRaw))

        if ('dt_load_date' in dfData.columns):
            vData = dfData.select(max('dt_load_date').cast(StringType()).alias('dt_load_date')).distinct().collect()[0].dt_load_date
        else:
            vData = None

        return vData
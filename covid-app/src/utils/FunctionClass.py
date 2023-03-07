from pyspark.sql.types      import *
from pyspark.sql            import SparkSession 
from pyspark.sql.functions  import *


class FunctionClass():
    def import_csv(self, spark, pthRaw, header, delimiter, encoding, campos, schema,
                id_chave, csvFile, nr_repartition=5, getItemFileName=3,dropDuplicate=True,have_dt_load=True):

        try:
            #Valor vindo da assinatura do método
            if have_dt_load:
                dt_load = self.listDtLoads( delimiter, pthRaw ,spark)
                #for dt_load in lista_dt_load:

            df = spark.read\
                .option('header', header)\
                .option('delimiter', delimiter)\
                .option('encoding', encoding)\
                .option("escape", "\"")\
                .csv(str(pthRaw))\
                .withColumn('filename', split(trim(substring(input_file_name(), 54, 309)),"/").getItem(getItemFileName))
                #.withColumn('filename_norm', input_file_name())
                
            
            df.show(20, False)
            #df = df.withColumn("filename", split(col("filename"), ".csv").getItem(0))

            #Valor vindo da assinatura do método
            if have_dt_load:
                df_max = df.select(col('filename'),col('dt_load_date'))\
                    .groupBy(col('filename'))\
                    .agg(max(col('dt_load_date')).alias('dt_load_date'))

                df = df.join(df_max, ((df.dt_load_date == df_max.dt_load_date) & (df.filename == df_max.filename)), how='inner')\
                    .drop(df_max.dt_load_date)\
                    .drop(df_max.filename)

            ## Renomea os campos para retirar caracteres especiais
            cColumn = len(df.columns)
            c = 0
            while c < cColumn:
                cOld = df.columns[c]
                cNew = str(str(str(str(str(str(df.columns[c]).replace('.','')).replace('/','')).replace(',','_')).replace('(','_')).replace(')','_')).replace("'",'')
                df = df.withColumnRenamed(cOld,cNew)
                c = c+1
            ## Fim
            cColumn = len(campos)
            c = 0
            while c < cColumn:
                campos[c] = str(str(str(str(str(str(campos[c]).replace('.','')).replace('/','')).replace(',','_')).replace('(','_')).replace(')','_')).replace("'",'')
                c = c+1       

            
            if dropDuplicate:
                df_duplicates = df.dropDuplicates(campos)
            else:
                df_duplicates = df

            #sub = 'hdfs://nameservice1'+str(pthRaw)+str('dt_load_date=')+str(dt_load)+'/'
            df = df.withColumn('id_hash', sha2(concat_ws('|', *df.columns), 256))
            #df = df.withColumn('filename', regexp_replace(input_file_name(),sub,''))

            ## Remove dados duplicados, caso exista o campo mergeFilename, temos que retirar da lista no dropduplicate.
            if ('mergeFilename' in campos):
                auxCampos.remove('mergeFilename')
            df_duplicates = df.dropDuplicates(campos)
        
            ## log success  
            #df_log = self.Log.closeProcessLogSucess("Remover duplicados", df_log)


            #Valor vindo da assinatura do método
            if have_dt_load:
                df_duplicates = df_duplicates.withColumn('dt_load_date', col("dt_load_date"))
            else:
                df_duplicates = df_duplicates.withColumn('dt_load_date', lit(current_timestamp()))
            df_duplicates = df_duplicates.withColumn('dt_insert', lit(current_timestamp()))

            if len(id_chave) != 0:
                df_duplicates = df_duplicates.withColumn('id_hash_key', sha2(concat_ws('|', *id_chave), 256))
            else:
                df_duplicates = df_duplicates.withColumn('id_hash_key', lit(None))

            ## Coloca os campos na sequencia do destino
            campos.append('filename')
            campos.append('id_hash')
            campos.append('dt_load_date')
            campos.append('dt_insert')
            campos.append('id_hash_key')

            df_duplicates = df_duplicates.select(campos)
            #df_duplicates.cache().count()

            ## Cria DF vazio, na estrutura e nomenclatura dos campos da analysis
            df_final = spark.createDataFrame(spark.sparkContext.emptyRDD(),schema)

            df_final = df_final\
                .withColumn('filename',lit(None).cast(StringType()))\
                .withColumn('id_hash',lit(None).cast(StringType()))\
                .withColumn('dt_load_date',lit(None).cast(StringType()))\
                .withColumn('dt_insert',lit(None).cast(TimestampType()))\
                .withColumn('id_hash_key',lit(None).cast(StringType()))
            #df_final.cache().count()

            # Insere dados na estrutura final
            df_resultado = df_final.union(df_duplicates)

            ## Grava o resultado.
            #var_dt_beginning=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            
            df_resultado.repartition(nr_repartition)\
                        .write\
                        .mode('overwrite')\
                        .parquet(str(pthTrusted))


            ## Create table caso solcitado via paramentro
            if create_table:
                self.create_table(spark=spark
                                    ,database=db_analysis
                                    ,table=table_analysis
                                    ,path=pthTrusted
                                    ,dataframe=df_resultado)

        except Exception as e:
            print(str(e))
            #df_log = self.Log.closeProcessLogFail("Load do arquivo CSV", str(e), df_log)
            #self.Log.salvar_log(df_log, self.Dados['caminho_log'])
            raise
        return
    
    def columnTrim(self):

        return True

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
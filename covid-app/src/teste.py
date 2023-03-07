import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark import SparkFiles
import datetime    
dtLoad = datetime.datetime.today()

hdfsNode = "hdfs://hadoop-namenode:9000/gft/"
path_save = "raw/covid/"

spark = SparkSession.\
        builder.\
        master("local[1]").\
        appName("pyspark-raw-covid").\
        getOrCreate()

spark.sparkContext.setLogLevel("WARN")
        
url = "https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/LEITOS/2023-02-21/esus-vepi.LeitoOcupacao_2022.csv"
csvName = "esus-vepi.LeitoOcupacao_2022.csv"

spark.sparkContext.addFile(url)
df = spark.read.csv(SparkFiles.get(csvName),inferSchema=True, header=True,  sep =',',  multiLine=True)

df = df.withColumn('dt_folder', current_date())\
     .withColumn("file_name", input_file_name()) \

df.write.option("header", False)\
        .mode("overwrite") \
        .partitionBy("dt_folder")\
        .csv(hdfsNode + path_save )
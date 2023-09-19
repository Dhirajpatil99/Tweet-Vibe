import os
import pyspark
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from helper_functions import clean_tweets
import pandas as pd
from pyspark.sql.types import ArrayType, StringType
from cloud_functions import upload_file,read_file

from pyspark.sql.functions import udf
from pyspark.ml.classification import LogisticRegressionModel
# findspark.init("C:\spark\spark-3.4.1-bin-hadoop3")

def spark_predict():
    spark = SparkSession.builder.appName("ModelSaveExample").config("spark.driver.host", "localhost").config("spark.driver.memory", "2g").getOrCreate()

    pipeline_=PipelineModel.load("spark_saves/pipeline_hash_idf")

    df = spark.createDataFrame(read_file("tweets.csv"))
    # df = spark.read.option("header","True").csv("tweeets.csv")
    df=df.select("tweets")
    cleanTweets = udf(clean_tweets,ArrayType(StringType()))
    df=df.withColumn("tweet_lem",cleanTweets("tweets"))
    transform_tweets=pipeline_.transform(df)
    # print(transform_tweets.toPandas().head())

    model=LogisticRegressionModel.load("spark_saves/logistic model")
    df_p=model.transform(transform_tweets)
    # df_p.select("tweets","prediction").write.csv("predicted_spark", header=True, mode="overwrite")  # Change mode if needed
    df_p=df_p.toPandas()[["tweets","prediction"]]
    df_p["prediction"]=df_p.prediction.apply(lambda x : "POSITIVE" if int(x)==1 else "NEGATIVE")
    flag=upload_file(df_p,"predicted.csv")
    return flag
   

        

    spark.stop()

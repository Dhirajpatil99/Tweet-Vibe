


import os
#import chardet
# import pyspark
# from pyspark.ml import PipelineModel
# from pyspark.sql import SparkSession
# from helper_functions import clean_tweets
# import pandas as pd

# # Set HADOOP_HOME to the directory containing winutils.exe
# os.environ["HADOOP_HOME"] = "C:\\hadoop"

# # # Initialize SparkSession
# # spark = SparkSession.builder.master("local").appName("ModelSaveExample").getOrCreate()

# spark = SparkSession.builder.master("local").appName("ModelSaveExample") \
#         .config("spark.driver.extraClassPath", "C:\\hadoop") \
#         .getOrCreate()

# # Load the PipelineModel from the correct directory
# model_directory = "spark_saves/pipeline_hash_idf"
# pipeline_ = PipelineModel.load(model_directory)

# # Read CSV using the correct path
# csv_path = os.path.abspath("src/tweeets.csv")
# df = pd.read_csv(csv_path)

# # Apply cleaning function and transform using the loaded model
# df["tweet_lem"] = df.tweets.apply(lambda x: clean_tweets(x).split())
# transform_tweets = pipeline_.transform(df)

# # Show the transformed DataFrame
# print(transform_tweets.head())print("hello")
import pyspark
# import findspark
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
    # input_folder = "predicted_spark"
    # output_file = "predicted.csv"

        


    # with open(output_file, "w") as output:
    #     for filename in os.listdir(input_folder):
    #         if filename.endswith(".csv"):
    #             filepath = os.path.join(input_folder, filename)
    #             # with open(filepath, 'rb') as file:
    #             #     result = chardet.detect(file.read())
    #             #     encoding = result['encoding']
    #             with open(filepath, "r",encoding="utf-16") as file:
    #                 output.write(file.read())
    #                 output.write("\n")  # Add newline after each file
    # Stop the Spark session
    spark.stop()
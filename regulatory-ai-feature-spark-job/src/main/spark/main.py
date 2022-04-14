from __future__ import print_function
import os
import configparser
import sys
import traceback
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
import pyspark
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, array, ArrayType, DateType, DecimalType
from pyspark.sql.functions import *
from pyspark.sql.functions import concat, lit, col, udf
from delta import * 
import shutil

import logging
logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__) # __name__=docai
logger.info("This is an INFO message on the root logger.")


if __name__ == "__main__":
    
    """
        Start Spark Session

    """
    table_name = "delta-table"
    container_name = "docai-container"
    storage_account_name = "silliansdocai"
    account_access_key = "sCYyqgpmt+oxr8I5JkZkJMqxHwIboQIOR4Ew8AO95U8bhbEDM1kldLtdCJtcQStkr5M5xrqK2suHkvdtWLKrPA=="

    try:
        builder = SparkSession \
                    .builder \
                    .appName("DocumentAI") \
                    .master("local") \
                    .config("spark.jars.packages", "io.delta:delta-core_2.12:1.1.0") \
                    .config("spark.jars.packages", "org.apache.hadoop:hadoop-azure-datalake:3.3.1") \
                    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
                    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
                    .config(f"spark.hadoop.fs.azure.account.auth.type.{storage_account_name}.dfs.core.windows.net", "SharedKey") \
                    .config(f"spark.hadoop.fs.azure.account.key.{storage_account_name}.dfs.core.windows.net", f"{account_access_key}")

        logger.info(SparkConf().getAll())
        spark = configure_spark_with_delta_pip(builder).getOrCreate()
        spark.sparkContext.setLogLevel('INFO')
    
    except Exception as error:
        logger.info(f"Exception occurred {error}")
        logger.info("Spark builder connection prompted out due to : %s", error)
        logger.info(traceback.format_exc())

    # Create a data schema
    schema = StructType([
            StructField("city", StringType(), True),
            StructField("dates", StringType(), True),
            StructField("population", IntegerType(), True)])


    dates = ["1991-02-25","1998-05-10", "1993/03/15", "1992/07/17", "1992-05-23", "2022-06-23"]
    cities = ['Caracas', 'Ccs', 'São Paulo', 'Madrid', "San Francisco", "New Hampshire"]
    population = [37800000, 19795791, 12341418, 6489162, 8483993, 76234589]

    # Dataframe:
    data = spark.createDataFrame(list(zip(cities, dates, population)), schema=schema)

    # write to delta-lake
    # data.write \
    #           .format("delta") \
    #           .save(f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/{table_name}")
    # logger.info("Successfully written")
    # data.show(truncate=False)

    # Append the new-data to delta-table
    data.write \
        .format("delta") \
        .mode("overwrite")  \
        .save(f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/{table_name}")


    # Read from delta-table
    new_df = spark.read.format("delta").load(f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/{table_name}")
    new_df.show()

    spark.stop()
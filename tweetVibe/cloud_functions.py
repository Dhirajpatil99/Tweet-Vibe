from smart_open import smart_open
import pandas as pd
from io import StringIO # python3; python2: BytesIO 
import boto3
pd.DataFrame.iteritems=pd.DataFrame.items

ACCESS_KEY_ID = 'AKIA4W2VANNNLF4VHPST'
SECRET_KEY = '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'
bucket="tweetvibes"
def read_file(filename,ACCESS_KEY_ID=ACCESS_KEY_ID,SECRET_KEY=SECRET_KEY,bucket=bucket):
    try:
        path = 's3://{}:{}@{}/{}'.format(ACCESS_KEY_ID,SECRET_KEY,bucket,filename)
        return pd.read_csv(smart_open(path))
    except:
        return pd.DataFrame()

def upload_file(dataframe,filename,ACCESS_KEY_ID=ACCESS_KEY_ID,SECRET_KEY=SECRET_KEY,bucket=bucket):
    s3 = boto3.resource("s3",\
                  aws_access_key_id=ACCESS_KEY_ID,\
                  aws_secret_access_key=SECRET_KEY)
    csv_buffer = StringIO()
    dataframe.to_csv(csv_buffer,header=True,index=False)
    s3.Object(bucket, filename).put(Body=csv_buffer.getvalue())
    return True


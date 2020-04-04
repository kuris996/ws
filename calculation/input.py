import requests
import xml.etree.ElementTree as ET
import os
import boto3
import datetime

STORAGE_URL = 'https://storage.yandexcloud.net'
BUCKET_NAME = 'ui-test'
ACCESS_KEY_ID = 'jE46D2owP1uHS9dHRdyM'
SECRET_ACCESS_KEY = 'qx-tm8jD82sCMwQHP3YG1siKMUtVJ3nDVb7o-kx-'

class Input:
    def fetch(self, prefix = ""):
        session = boto3.session.Session()
        s3 = session.client(
            service_name='s3',
            endpoint_url=STORAGE_URL,
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=SECRET_ACCESS_KEY,
            region_name='ru-central1'
        )
        files = []
        try:
            for content in s3.list_objects(Bucket=BUCKET_NAME)['Contents']:
                key = content['Key']
                if key.startswith(prefix):
                    name = key[len(prefix):]
                    if not name:
                        continue
                    files.append({
                        "key" : name,
                        "size" : content['Size'],
                        "lastModified" : content['LastModified'].isoformat(),
                        "url": os.path.join(STORAGE_URL, BUCKET_NAME, key)
                    })
        except:
            pass
        return files

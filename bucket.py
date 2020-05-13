import requests
import xml.etree.ElementTree as ET
import os
import boto3
import datetime
from collections import defaultdict
from constants import STORAGE_URL, BUCKET_NAME, ACCESS_KEY_ID, SECRET_ACCESS_KEY

KEY = 'key'
NAME = 'name'
SIZE = 'size'
LAST_MODIFIED = 'lastModified'
URL = 'url'
CHILDREN = 'children'

class Bucket:
    def __init__(self):
        self.session = boto3.session.Session()
        self.s3 = self.session.client(
            service_name='s3',
            endpoint_url=STORAGE_URL,
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=SECRET_ACCESS_KEY,
            region_name='ru-central1'
        )

    def write(self, source_file_name, dest_file_name):
        try:
            self.s3.upload_file(source_file_name, BUCKET_NAME, dest_file_name)
            return True
        except:
            return False

    def read(self, source_file_name, dest_file_name):
        try:
            self.s3.download_file(BUCKET_NAME, source_file_name, dest_file_name)
            return True
        except:
            return False

    def fetch(self, kit, uuid):
        tree = []
        try:
            for content in self.s3.list_objects(Bucket=BUCKET_NAME)['Contents']:
                path = None                
                prefix = 'data/Inputs/' + kit
                key = content['Key']
                if uuid:
                    for n in range(4):
                        if key.startswith(prefix + '/{}/'.format(n) + uuid):
                            path = key[len('data/Inputs/'):]
                            path = path.replace('/{}/'.format(n) + uuid, '')
                            break
                    
                if key.startswith(prefix + '/Input_inputs'):
                    path = key[len('data/Inputs/'):]
                elif key.startswith(prefix + '/Input_outputs'):
                    path = key[len('data/Inputs/'):]
                elif key.startswith(prefix + '/Backtesting'):
                    path = key[len('data/Inputs/'):]
                if path:
                    path = path.replace(kit, 'root')
                    self.__append_contents(path, content, tree)
        except:
            pass
        return tree

    def fetch_inputs(self, kit):
        tree = []
        try:
            for content in self.s3.list_objects(Bucket=BUCKET_NAME)['Contents']:
                path = None                
                prefix = 'data/Inputs/' + kit + '/Input_outputs/Inputs/'
                key = content['Key']
                if key.startswith(prefix):
                    path = key[len(prefix):]                
                if path:
                    path = path.replace(kit, 'root')
                    self.__append_contents(path, content, tree)
        except:
            pass
        return tree

    def __append_contents(self, path, contents, tree):
        if not path:
            return
        parts = path.split('/', 1)
        if len(parts) == 1:
            tree.append({ 
                KEY: path, 
                NAME: parts[0],
                SIZE: contents['Size'],
                LAST_MODIFIED: contents['LastModified'].isoformat(),
                URL: os.path.join(STORAGE_URL, BUCKET_NAME, contents['Key'])
            })
        else:
            name, others = parts
            node = None
            for n in tree:
                if n[NAME] == name:
                    node = n
                    break
            children = []
            if not node:
                tree.append({ 
                    KEY: path, 
                    NAME: name, 
                    CHILDREN: children 
                })
            else:
                try:
                    children = node[CHILDREN]
                except:
                    node[CHILDREN] = children

            self.__append_contents(others, contents, children)

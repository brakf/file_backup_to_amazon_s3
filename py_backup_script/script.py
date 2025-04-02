from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
import sys
import zipfile
import yaml
import boto3
import time

start_time = time.time()
if len(sys.argv) == 2:
    config_path = sys.argv[1]
else:
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    
config = yaml.load(open(config_path), Loader=yaml.FullLoader)

logging.basicConfig(encoding='utf-8', level=logging.INFO, handlers=[RotatingFileHandler(os.path.join(os.path.dirname(__file__), "s3_upload.log"), maxBytes=1024000, backupCount=1)])

logging.info(["---------NEW EXECUTION STARTED---------", datetime.now().__str__()])

s3_client = boto3.client('s3', aws_access_key_id=config.get("AWSAccessKey"), aws_secret_access_key=config.get("AWSSecretKey"))

bucket_folder = config.get("BucketFolder", "")
if bucket_folder and not bucket_folder.endswith("/"):
    bucket_folder += "/"

for file in config.get("FilesToBackup", []):
    try: 
        path = os.path.join(config.get("BasePath", ""), file)
        filename_zip = file + ".zip"
        path_zip = os.path.join(os.path.dirname(__file__), filename_zip)  
        zip_time = time.time()

        # Test if file exists
        if not os.path.exists(path):
            raise Exception("File not found: " + path) 
        
        logging.info("Zipping file: " + path)
        
        with zipfile.ZipFile(path_zip, mode='w', compression=zipfile.ZIP_DEFLATED, allowZip64=True, compresslevel=6) as zipf:
            zipf.write(path, arcname=file)
        
        logging.debug("---Zip Time %s seconds ---" % (time.time() - zip_time))
        logging.info("Uploading file: " + path_zip)
        
        try:
            upload_time = time.time()
            s3_key = bucket_folder + filename_zip
            s3_client.upload_file(path_zip, config.get("BackupBucket"), s3_key)
            logging.debug("---Upload Time %s seconds ---" % (time.time() - upload_time))
        except boto3.ClientError as e:
            logging.error(e)
            raise Exception(e)

        logging.info("Deleting file: " + path_zip)
        os.remove(path_zip)

    except Exception as e:
        logging.error(e)
        if os.path.exists(path_zip):
            logging.info("Deleting file as cleanup: " + path_zip)
            os.remove(path_zip) 
        
logging.debug("---Total Time %s seconds ---" % (time.time() - start_time))
logging.info(["--------- EXECUTION ENDED---------", datetime.now().__str__()])

# Script for uploading DB backup to the cloud
import sys
import os
from boto3 import resource, client
from pprint import pprint
from pathlib import Path
import re
import datetime

ACCESS_ID = os.environ['ACCESS_ID']
SECRET_KEY = os.environ['SECRET_KEY']
ENDPOINT_URL = os.environ['ENDPOINT_URL']
BUCKET_NAME = 'space_name' # Space name can be created in the DigitalOcean cloud

class UploadToCloud(object):
    """
    This script is used to upload Mongodb backup tar file to DigitalOcean Space Storage
    """
    def __init__(self, input_tuple):
        super(UploadToCloud, self).__init__()
        self.conn, self.client = self.cloud_conn()
        self.tar_file, self.db_name = input_tuple
        self.download_folder = str(Path.home())


    def tar_file_upload(self):
        now = datetime.datetime.now()
        print("Uploading {} to cloud".format(self.tar_file))
        regex = r"(\d{6})"
        match = re.search(regex, self.tar_file, re.IGNORECASE)
        if match:
            date = match.group()
        else:
            date = now.strftime("%d%m%y")

        upload = self.client.upload_file(self.tar_file, BUCKET_NAME, '/{}/backup_{}.tar.gz'.format(self.db_name, date))
        self.list_backups_in_cloud()


    def download_file(self, file_to_download=None):
        # Bucket, From, To
        print("Downloding file to {}".format(self.download_folder))
        self.client.download_file(BUCKET_NAME, file_to_download, '/{}/latest_db_backup.tar.gz'.format(self.download_folder))


    def delete_files(self, file_to_delete=None):
        print("Deleting {} file from cloud and cannot be revert.".format(file_to_delete))
        self.client.delete_object(Bucket=BUCKET_NAME, Key=file_to_delete)
        self.list_backups_in_cloud()


    def cloud_conn(self):
        s3config = {
            "region_name": 'sgp1',
            "endpoint_url": ENDPOINT_URL.format('sgp1'),
            "aws_access_key_id": ACCESS_ID,
            "aws_secret_access_key": SECRET_KEY }

        s3resource = resource("s3", **s3config)
        s3client = client("s3", **s3config)
        return (s3resource, s3client)


    def list_backups_in_cloud(self):
        backups = self.client.list_objects(Bucket=BUCKET_NAME)
        if 'Contents' not in backups: sys.exit("Bucket is empty.")
        print("*** Listing the backup files from the DigitlOcean cloud ***\n")
        for files in backups['Contents']:
            print("file {} - ({} MB) stored as {}".format(files['Key'],int(files['Size']/1024/1024) ,files['StorageClass']))
        print("\n*** End ***")


if __name__ == '__main__':
    # sys.argv = ['test', '/home/mo/mongodb_backups/040319/mohan.tar.gz', 'mohan']
    if len(sys.argv) == 3:
        backup_file, bucket_name = tuple(sys.argv[1:])
        cloud_obj = UploadToCloud((backup_file, bucket_name))
        cloud_obj.tar_file_upload()
        # cloud_obj.list_backups_in_cloud()
        # cloud_obj.delete_files('mohan/test.tar.gz')
        # cloud_obj.download_file('/path/to/backup_120319.tar.gz')
    else:
        print("Missing or passing more params: usage ex: python {} /db/backup/file/path.tar.gz db_name".format(sys.argv[0]))

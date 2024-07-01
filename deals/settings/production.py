import os

# DEBUG for production
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allowed hosts for production including live server
ALLOWED_HOSTS = ['127.0.0.1', '.vercel.app', '.now.sh', 'localhost','www.edudealio.com']

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_SIGNATURE_NAME = os.getenv("AWS_S3_SIGNATURE_NAME"),
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = os.getenv("DEFAULT_FILE_STORAGE")


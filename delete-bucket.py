#!/usr/local/bin/python3
import json
import subprocess

bucketName = "example-bucket"
endpointURL = "https://s3api-core.uhc.com"

# Set default value for bucketExists to False
bucketExists = False

# Verifies s3 bucket exists
getBucketName = subprocess.check_output("aws s3api --endpoint-url " + endpointURL + " list-buckets --query 'Buckets[].Name'", stderr=subprocess.STDOUT, shell=True)

# Loop through Owner's available buckets to match to bucketName provided above
for bucket in eval(getBucketName):
    if bucket == bucketName:
        bucketExists = True
        break

# if bucket provided (bucketName) exists and is available to the Owner, run empty and delete of bucket    
if bucketExists:
    # Takes s3 Bucket Object contents and assigns it to s3bucketObjects variable
    s3bucketObjects = subprocess.check_output("aws s3api --endpoint-url " + endpointURL + " list-objects --bucket " + bucketName, stderr=subprocess.STDOUT, shell=True)

    # Validate s3bucketObjects is not null
    if s3bucketObjects:
        # Takes s3bucketObjects and transforms the data to json 
        jsonObject = json.loads(s3bucketObjects)

        # Loop through Contents for each key value and removes the object 
        for obj in jsonObject['Contents']:
            key = obj['Key']
            print("Removing Object")
            subprocess.check_output("aws s3api --endpoint-url " + endpointURL + " delete-object --bucket " + bucketName + " --key " + key, stderr=subprocess.STDOUT, shell=True)

    print("Deleting bucket")

    # Delete empty bucket
    subprocess.check_output("aws s3api --endpoint-url " + endpointURL + " delete-bucket --bucket " + bucketName, stderr=subprocess.STDOUT, shell=True)

    print("s3 bucket " + bucketName + " has been emptied of objects and deleted")

else:
    print ("Bucket " + bucketName + " could not be found")
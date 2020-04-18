import json
import boto3
import time
import datetime

bucket = 'knownfacesphotos'
collection_id = "Collection1"
face_dict = {}
time_limit = 300

def list_diff(list1, list2): 
    return (list(set(list1) - set(list2)))

def parse_face_response(response):
    for face in response['Faces']:
        faceId = face['FaceId']
        image_name = face['ExternalImageId']
        face_dict[faceId] = image_name

def collection_faceId():
    client = boto3.client('rekognition')
    nextToken = None
    while(True):
        if nextToken:
            response = client.list_faces(CollectionId=collection_id, NextToken=nextToken)
            parse_face_response(response)
        else:
            response = client.list_faces(CollectionId=collection_id)
            parse_face_response(response)
            break
        nextToken = response.get('NextToken', None)

def dynamodb_faceId():
    #print("Dynamo DB")
    face_list = []
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('visitors')
    response = table.scan(AttributesToGet=['faceID'])
    face_list = [ faceID['faceID'] for faceID in response['Items']]
    return face_list

def get_timestamp_s3(filename):
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket, Key=filename)
    #print(response)
    img_timestamp = str(response['LastModified'])
    img_timestamp = img_timestamp[:-6]
    pattern = '%Y-%m-%d %H:%M:%S'
    img_epoch = int(time.mktime(time.strptime(str(img_timestamp), pattern)))
    cur_epoch = int(datetime.datetime.utcnow().timestamp())
    #print(cur_epoch - img_epoch)
    if cur_epoch - img_epoch > time_limit:
        return True
    return False

def delete_from_collection(faceID_list_deletion):
    print("Deleting " + str(faceID_list_deletion) + " from " + collection_id)
    client = boto3.client('rekognition')
    response = client.delete_faces(CollectionId=collection_id, FaceIds=faceID_list_deletion)
    #print(response)

def lambda_handler(event, context):
    faceID_list_dynamodb = dynamodb_faceId()
    collection_faceId()
    faceID_dict_collection = face_dict
    faceID_list_collection = list(face_dict.keys())
    faceID_list_diff = list_diff(faceID_list_collection, faceID_list_dynamodb)
    faceID_list_deletion = []
    print(faceID_list_diff)
    for faceID in faceID_list_diff:
        filename = faceID_dict_collection[faceID]
        if get_timestamp_s3(filename):
            faceID_list_deletion.append(faceID)
    print(faceID_list_deletion)
    if faceID_list_deletion:
        delete_from_collection(faceID_list_deletion)

import boto3


client = boto3.client('rekognition', region_name='us-east-1',
	      aws_access_key_id = aws_access_key_id,
	      aws_secret_access_key = aws_secret_access_key)
bucket = ''
photo = ''
collection_id = ''

def create_collection(collection_id):
    collection_id = 'Collection1'
    #Create a collection
    print('Creating collection:' + collection_id)
    response=client.create_collection(CollectionId=collection_id)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')


def add_faces_to_collection(bucket,photo,collection_id): 

    response=client.index_faces(CollectionId=collection_id,
                                Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                ExternalImageId=photo,
                                MaxFaces=1,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])
    print(response)

    
def main():
    create_collection(collection_id)
    add_faces_to_collection(bucket,photo,collection_id)

if __name__ == "__main__":
    main()  

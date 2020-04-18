import boto3

aws_access_key_id = '' 
aws_secret_access_key = ''
kds_arn = ''
kvs_arn = ''
iam_arn = ''
collection_id = ''

client = boto3.client('rekognition', region_name='us-east-1',
              aws_access_key_id = aws_access_key_id,
              aws_secret_access_key = aws_secret_access_key)

def create_stream_processor():

    input_dict = {
			  "KinesisVideoStream": {
				 "Arn": kvs_arn
			  }
		   }
    output_dict = {
		          "KinesisDataStream": {
			         "Arn": kds_arn
			   }
	          }
    settings_dict = {
			  "FaceSearch": {
				 "CollectionId": collection_id,
				 "FaceMatchThreshold": 85.5
			  }
		   }
    
    response = client.create_stream_processor(Input=input_dict, Output=output_dict, Name="StreamProcessor1", Settings=settings_dict, RoleArn=iam_arn)
    print(response)


def main():
    create_stream_processor()

if __name__ == "__main__":
    main()

from urllib.parse import quote_plus

def to_s3_url(file, prefix="", bucket_name="2022assets"):
    key = file
    key = quote_plus(key, safe="~()*!.'")
    object_url = f'''https://{bucket_name}.s3.amazonaws.com/music/{prefix}/{key}'''
    return object_url


# file = "meh 130 (jazz fusion).wav"
# f = to_s3_url(file)
# print(f)

# https://2022assets.s3.amazonaws.com/music/audio/daw1loops/meh+130+(jazz+fusion).wav

# import boto3

# # Create a Boto3 S3 client
# s3 = boto3.client('s3')

# # Specify the name of the bucket
# bucket_name = '2022assets'

# # List the objects in the bucket
# response = s3.list_objects(Bucket=bucket_name)

# # Extract the URLs for the objects
# for obj in response['Contents']:
#     object_key = obj['Key']
#     object_url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
#     print(object_url)
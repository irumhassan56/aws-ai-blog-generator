import boto3
import botocore.config
import json
import response
from datetime import datetime


def blog_generator(blogtopic:str)-> str:
    prompt = f"""<s>[INST]Human:
    Write a blog about {blogtopic} in 200 words.
    The blog should be engaging and informative, providing valuable insights and tips related to the topic.
    The blog should be well-structured, with a clear introduction, body, and conclusion.
    The blog should be written in a conversational tone, making it easy for readers to understand and relate to the content.
    The blog should include relevant examples and anecdotes to illustrate key points and make the content more relatable.
    The blog should be optimized for SEO, incorporating relevant keywords and phrases to improve search engine rankings and attract more readers.
    The blog should be original and unique, avoiding plagiarism.
    Assistant: [/INST]
    """
    
    body = {
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.5,
        "top_p": 0.9
    }
    
    try:
        bedrock_client = boto3.client('bedrock-runtime', region_name = "us-east-1",
                                      config=botocore.config.Config(read_timeout=300, retries={'max_attempts': 3}))
        bedrock.invoke_model(body =json.dumps(body), modelId = "meta.llama3-8b-instruct-v1:0")
        response_content = response.get("body").read()
        response_data =json.load(response_content)
        print(response_data)
        blog_details = response_data['generation']
        return blog_details
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
    
 
def upload_to_s3(s3_bucket, s3_key, generate_blog):
    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(Bucket=s3_bucket, Key=s3_key, Body=generate_blog)
        print(f"Blog uploaded to S3 bucket '{s3_bucket}' with key '{s3_key}'.")
    except Exception as e:
        print(f"An error occurred while uploading to S3: {e}")
       
def lambda_handler(event, context):
    # TODO implement
    event =json.loads(event['body'])
    blogtopic = event["blogtopic"]
    
    generate_blog = blog_generator(blogtopic= blogtopic)
    if generate_blog:
        currrent_time = datetime.now().strftime("%H:%M:%S")
        s3_key = f"blog_output/{currrent_time}.txt"
        s3_bucket = "aws_bedrock"
        upload_to_s3(s3_bucket, s3_key, generate_blog)
    else:
        print("Blog generation failed.")
        
    return {
        'statusCode': 200,
        'body': json.dumps('Blog generation and upload process completed.')
    }
     
        
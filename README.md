
# AI Blog Generator (AWS Serverless)

This project is a serverless AI-powered blog generator built using AWS services.

## Architecture

User request → API Gateway → Lambda → Amazon Bedrock → Amazon S3

## Technologies Used

- AWS Lambda
- Amazon Bedrock
- Amazon API Gateway
- Amazon S3
- Python (boto3)
- 
## How It Works

1. User sends blog topic through API request.
2. Lambda function processes the request.
3. Amazon Bedrock generates the blog using the DeepSeek model.
4. The generated blog is saved in an S3 bucket.
## Example Request

{
 "blogtopic": "How Artificial Intelligence is Transforming Healthcare."
}

## Output
A blog text file is generated and stored in S3.

# Pull and run the Docker container
docker pull aghouth/web:latest
docker run -it --rm -v $(pwd)/data/:/app/data/ aghouth/web

# Source the .env file to load environment variables
source "$(dirname "$0")/.env" 

# Copy dataset to S3 bucket
aws s3 cp $(pwd)/data/dataSet.csv s3://"$BUCKET"/dataset.csv

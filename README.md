# Moritz Grossmann Watch Scraping
As part of this project, a python script is was used to scrape Moritz Grossmann website and collect information about all the watches. The script was containerized and pushed to Docker Hub.

## Files
The project includes two main files:
- **init.sh** is used install/update packages and set some configurations
- **run.sh** is used to pull/run the container then store the dataset to AWS S3

It is necessary to create a .env file to include AWS IAM information as well as AWS S3 bucket name and location. The variables that need to be set are:
- ACCESS_KY_ID
- SECRET_KEY
- LOCATION
- BUCKET

## Script Automation
A cron job is scheduled to automate the web scraping process. For testing purposes, the following command was used to run the script every 5 minutes:
`*/5 * * * * cd ~/web-scraping-project && bash run.sh`

Note: the script needs 2-3 minutes to run.

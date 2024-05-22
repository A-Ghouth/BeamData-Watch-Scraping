# Moritz Grossmann Watch Scraping

## Overview
This project involves using Python to scrape the Moritz Grossmann website and collect information about all the watches. The script is containerized and pushed to Docker Hub for easy deployment and distribution.

## Project Files
The project includes the following main files:

1. **init.sh**: This script is used to install/update packages and set some configurations before running the web scraping script.

2. **run.sh**: This script is responsible for pulling the Docker container, running the web scraping script, and storing the dataset to an AWS S3 bucket.

## Environmental Variables
To use this project, you will need to create a `.env` file and include the following environment variables:

- `ACCESS_KY_ID`: Your AWS IAM access key ID
- `SECRET_KEY`: Your AWS IAM secret access key
- `LOCATION`: The location of your AWS S3 bucket
- `BUCKET`: The name of your AWS S3 bucket

## Script Automation
To automate the web scraping process, a cron job can be scheduled to run the `run.sh` script periodically. For testing purposes, the following command was used to run the script every 5 minutes:

```
*/5 * * * * cd ~/web-scraping-project && bash run.sh
```

Note that the script typically takes 2-3 minutes to run.

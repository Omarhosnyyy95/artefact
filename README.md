# Project Description

# Architecture
![Alt text](images/architecture.png)
1) theguardian website
2) scraping application
3) mongodb database running in a dedicated Atlas cluster inside a vpc
    14845 documents fetched from https://www.theguardian.com/australia-news/all
    there is a limitation on the website for page>1900
    text index created on title and content to optimize data fetching from the API
    unique index created on s_uid to speed up upsert process

4) vpc peering
5) lambda function on aws in a vpc
6) api gateway
7) user application

# How to use the API
the simplest and fastest is using a tool like Postman. 
GET https://1shvuf0lmj.execute-api.eu-west-3.amazonaws.com/default/search_articles?search_text=australia&limit=10

![Alt text](images/postman.PNG)


# How to run the web scraping application code
1) clone the repo
2) set environment variables
## windows
setx mongodbConnectionStr <connectionstr>
setx mongodbDbName <DbName>
setx mongodbCollectionName <CollectionName>

## Linux
setx mongodbConnectionStr <connectionstr>
setx mongodbDbName <DbName>
setx mongodbCollectionName <CollectionName>

3) optional step if you want to use Anaconda
if you have Conda:
conda create --name mymongodbenv python=3.11.5
activate mymongodbenv


4)
cd <project_path>/theguardian
pip3 install pymongo=4.5.0
pip3 install Scrapy==2.11.0
scrapy crawl australia


# Solution enhancements
- build a docker image to the scraping application to be more portable and independent of the host environment 
- develop a serverless .YAML file to automate infrastructure deployment on AWS
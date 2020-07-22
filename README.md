# funnelytics_demo

### Setup

Install Serverless
```
npm i serverless@1.51.0
```

Install serverless python requirements
```
npm i serverless-python-requirements@5.0.0
```

Install docker (This is needed for packaging python dependencies)

Configure aws profile in ~/.aws/credentials. I configured with name funnelytics-backend-service

Command to deploy (This will deploy full stack)
```
serverless deploy -r eu-west-2 -s production --aws-profile funnelytics-backend-service

aws-vault exec devsoc-analytics -- ./node_modules/.bin/serverless deploy -r eu-west-2 -s production
```

Command to deploy just the lambda function
```
serverless deploy -f hits_handler -r eu-west-2 -s production --aws-profile funnelytics-backend-service
```

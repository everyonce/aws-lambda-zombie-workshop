# Zombie Microservices Workshop: Lab Guide

## Overview of Workshop Labs
The [Zombie Microservices Workshop](http://aws.amazon.com/events/zombie-microservices-roadshow/) introduces the basics of building serverless applications using [AWS Lambda](https://aws.amazon.com/lambda/), [Amazon API Gateway](https://aws.amazon.com/api-gateway/), [Amazon DynamoDB](https://aws.amazon.com/dynamodb/), [Amazon Cognito](https://aws.amazon.com/cognito/), [Amazon SNS](https://aws.amazon.com/sns/), and other AWS services. In this workshop, as a new member of the AWS Lambda Signal Corps, you are tasked with completing the development of a serverless survivor communications system during the Zombie Apocalypse.

This workshop has a baseline survivor chat app that is launched via [CloudFormation](https://aws.amazon.com/cloudformation/). Complete the lab exercises to extend the functionality of the communications system or add your own custom functionality!

Prior to beginning the labs, you will need to finalize the setup of User authentication for the application with [Cognito User Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html). This is a necessary step to finalize the readiness of the application.

### Required: Setup Authentication with Cognito User Pools
In this setup lab, you will integrate user authentication into your serverless survivor chat application using Amazon Cognito User Pools.

### Labs
Each of the labs in this workshop is an independent section and you may choose to do some or all of them, or in any order that you prefer.

* **Lab 1: Typing Indicator**  

  This exercise already has the UI and backend implemented, and focuses on how to setup the API Gateway to provide a RESTful endpoint. You will configure the survivor chat application to display which survivors are currently typing in the chat room.

* **Lab 2: SMS Integration with Twilio**  

    This exercise uses [Twilio](http://twilio.com) to integrate SMS text functionality with the survivor chat application. You will configure a free-trial Twilio phone number so that users can send text messages to the survivor chat application. You'll learn to leverage mapping templates in API Gateway to perform data transformations in an API.

* **Lab 3: Search Integration with Elasticsearch**  

    This exercise adds an Elasticsearch cluster to the application which is used to index chat messages streamed from the DynamoDB table containing chat messages.

* **Lab 4: Slack Integration**  

    This exercise integrates the popular messaging app, [Slack](http://slack.com), into the chat application so that survivors can send messages to the survivor chat from within the Slack app.

* **Lab 5: Intel Edison Zombie Motion Sensor** (IoT device required)

    This exercise integrates motion sensor detection of zombies to the chat system using an Intel Edison board and a Grove PIR Motion Sensor. You will configure a Lambda function to consume motion detection events and push them into the survivor chat!

### Workshop Cleanup

This section provides instructions to tear down your environment when you're done working on the labs.

* * *


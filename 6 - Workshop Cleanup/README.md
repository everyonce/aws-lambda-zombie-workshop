## 6 - Workshop Cleanup

1\. To cleanup your environment, it is recommended to first delete these manual resources you created in the labs before deleting your CloudFormation stack, as there may be resource dependencies that stop the Stack from deleting. Follow steps 2-6 before deleting your Stack.

2\. Be sure to delete the TwilioProcessing Lambda Function. Also if you no longer plan to use Twilio, please delete your Twilio free trial account and/or phone numbers that you provisioned.

3\. Be sure to delete the Elasticsearch cluster and the associated Lambda function that you created for the Elasticsearch lab. Also delete the IAM role you created for the Elasicsearch Lambda function, "ZombieLabLambdaDynamoESRole".

4\. Be sure to delete the Lambda function created as a part of the Slack lab and the Slack API resource you created. Also delete Slack if you no longer want an account with them.

5\. Be sure to delete the SNS topic (if you created one) and the Lambda function that you created in the Zombie Sensor lab.

6\. Delete the Cognito User Pool and Identity Pool associated with your application, that you created during lab setup.

* User Pool: Click into your User Pool and click the "Delete pool" button to delete your user pool.

* Identity Pool: Click into the Federated Identities page of Cognito and find your identity pool ([stackname]-identitypool). Then click **Edit identity pool**. Scroll to the bottom and delete the identity pool.

7\. Navigate to CloudWatch Logs and make sure to delete unnecessary Log Groups if they exist.   

8\. Once those resources have been deleted, go to the CloudFormation console and find the Stack that you launched in the beginning of the workshop, select it, and click **Delete Stack**.

* When the stack has been successfully deleted, it should no longer display in the list of Active stacks. If you run into any issues deleting stacks, please notify a workshop instructor or contact [AWS Support](https://console.aws.amazon.com/support/home) for additional assistance.

* * *

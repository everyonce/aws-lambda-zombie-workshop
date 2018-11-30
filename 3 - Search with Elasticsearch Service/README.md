# 3 - Search with Elasticsearch Service

## Lab 3 - Search over the chat messages with Elasticsearch Service

**What you'll do in this lab...**

In this lab you'll launch an Elasticsearch Service cluster and setup DynamoDB Streams to automatically index chat messages in Elasticsearch for future ad hoc analysis of messages.

**Elasticsearch Service Architecture**
![Overview of Elasticsearch Service Integration](/Images/ElasticsearchServiceOverview.png)

1\. Select the Amazon Elasticsearch icon from the main console page.

2\. Create a new Amazon Elasticsearch domain. Provide it a name such as "[Your CloudFormation stack name]-zombiemessages". Click **Next**.

3\. On the **Configure Cluster** page, leave the default cluster settings and click **Next**.

4\. For the access policy, select the **Allow or deny access to one or more AWS accounts or IAM users** option in the dropdown and fill in your account ID. Your AWS Account ID is actually provided to you in the examples section so just copy and paste it into the text box. Make sure **Allow** is selected for the "Effect" dropdown option. Click **OK**.

5\. Select **Next** to go to the domain review page.

6\. On the Review page, select **Confirm and create** to create your Elasticsearch cluster.

7\. The creation of the Elasticsearch cluster takes approximately 10 minutes.

* Since it takes roughly 10 minutes to launch an Elasticsearch cluster, you can either wait for this launch before proceeding, or you can move on to Lab 4 and come back to finish this lab when the cluster is ready.

8\. Take note of the Endpoint once the cluster starts, we'll need that for the Lambda function.
![API Gateway Invoke URL](/Images/Search-Step8.png)

9\. Go into the Lambda service page by clicking on Lambda in the Management Console.

10\. Select **Create a Lambda Function**.

11\. On the Blueprints screen select **Blank Function** to create a Lambda function from scratch.

12\. In Configure Triggers section, select the DynamoDB event source type and then select the **messages** DynamoDB table. It should appear as **"[Your CloudFormation stack name]-messages"**. Then set the **Batch size** to **5**, the **Starting position** to **Latest** and select the checkbox **Enable trigger**. Then click on Next button.

13\. Give your function a name, such as **"[Your CloudFormation stack name]-ESsearch"**. Keep the runtime at the default. You can set a description for the function if you'd like.

14\. Paste in the code from the ZombieWorkshopSearchIndexing.js file provided to you. This is found in the Github repo in the "ElasticsearchLambda" folder.

15\. On [line 6](/ElasticSearchLambda/ZombieWorkshopSearchIndexing.js#L6) in the code provided, replace the **region** variable with the code for the region you are working in (the region you launched your stack, created your Lambda function etc). If you're working in Oregon region, then leave the code us-west-2 as is.

Then on line 7, replace the **endpoint** variable that has a value of **ENDPOINT_HERE** with the Elasticsearch endpoint created in step 8\. **Make sure the endpoint you paste starts with https://**.

* This step requires that your cluster is finished creating and in "Active" state before you'll have access to see the endpoint of your cluster.

16\. Now you'll add an execution role to your Lambda function which gives permissions for your Lambda function to access AWS resources. For the Role, select **Choose an existing role**, and for the Existing Role, select **"[Your CloudFormation stack name]-ZombieLabLambdaRole"** which is the role that was created for you for this workshop. It has permissions to the Elasticsearch service.

17\. Expand the "Advanced settings" section and find the "Timeout" field for your Lambda function. In the timeout field, change the function timeout to **1** minute. This ensures Lambda can process the batch of messages before Lambda times out. Keep all the other defaults on the page set as is. Select **Next** and then on the Review page, select **Create function** to create your Lambda function.

18\. In the above step, we configured [DynamoDB Streams](http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html) to capture incoming messages on the table and trigger a Lambda function to push them to our Elasticsearch cluster. Your messages posted in the chat from this point forward will be indexed to Elasticsearch. Post a few messages in the chat, at least 5 as configured in the DynamoDB Streams event source (batch size). You should be able to see that messages are being indexed in the "Indices" section for your cluster in the Elasticsearch Service console.
![API Gateway Invoke URL](/Images/Search-Done.png)

**LAB 3 COMPLETE**

If you would like to explore and search over the messages in the Kibana web UI that is provided with your cluster, you will need to navigate to the Elasticsearch domain you created and change the permissions. Currently you've configured the permissions so that only your AWS account has access. This allows your Lambda function to index messages into the cluster.

To use the web UI to build charts and search over the index, you will need to implement an IP based policy to whitelist your computer/laptop/network or for simplicity, choose to allow everyone access. For instructions on how to modify the access policy of an ES cluster, visit [this documentation](http://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-gsg-configure-access.html). If you choose to open access to anyone be aware that anyone can see your messages, so please be sure to restrict access back to your AWS account when you're done exploring Kibana, or simply delete your ES cluster.  

* * *


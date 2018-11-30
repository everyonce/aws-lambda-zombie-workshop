# 4 - Slack Integration

## Lab 4 - Slack Integration

**What you'll do in this lab...**

In this lab, you'll integrate a Slack channel with your survivor chat. There may be survivors who use different chat systems and you'll want to communicate with them! After completing this lab, survivors communicating on Slack can send messages to survivors in the Zombie Chat App by configuring a slash command prefix to be used on any messages in their Slack channel that they want to send to the survivors. When Slack users type messages with this Slash command, it will pass the message to your survivor chat API, similiar to the webhook functionality enabled in the Twilio lab!

If you aren't familiar with Slack, they offer a free chat communications service that is popular, especially among the developer community. Slack uses a concept called "Channels" to distinguish different chat rooms. Visit their website to learn more!

**Slack Integration Architecture**
![Overview of Slack Integration](/Images/SlackOverview.png)

1\. Go to [http://www.slack.com](http://www.slack.com) and create a username, as well as a team. If you want to use your existing Slack username and existing team, then proceed with that profile instead of creating a new one.

2\. Once logged into your Slack team, navigate to [https://slack.com/apps](https://slack.com/apps) which should direct you to the app directory for your team. In the search bar in the middle of the App Directory page, type **slash commands** and select it from the options. This will take you to the Slash Commands portal. 

3\. On the Slash Commands page, click **Add configuration**. 

Slash commands allow you to define a command that you can use within Slack to trigger  Slack to perform actions in an event driven manner. In this case we are going to configure a slash command to forward messages to an external source with a webhook. You'll configure your Slash Command to make a POST request to a /zombie/slack API resource you will soon be creating in API Gateway. 

4\. On the Slash Commands configuration page, define a command in the **Commands** text box. Insert **/survivors** as your Slash Command. Then select "Add Slash Command Integration" to save it.

5\. On the Integration Settings page, scroll down to the **Method** configuration andmake sure the **Method** section has "POST" selected from the dropdown options. Then scroll to the **Token** section and copy the Token (or generate a new one) to a text file as you'll need it in the following steps.

6\. Keep the Slack browser tab open and in another tab navigate to the AWS Lambda management console in the AWS Management Console.

7\. Click **Create a Lambda function**. You'll create a Lambda function to parse incoming Slack messages and send them to the Chat Service.

8\. On the Blueprints page select **Blank Function** to create a function from scratch. Also skip past the triggers page by selecting **Next**.

9\. Give your function a name such as **"[Your CloudFormation Stack name]-SlackService"**. For the Nodejs version, you can keep the default Nodejs version selected. Now navigate to the GitHub repo for this workshop, or the location where you downloaded the GitHub files to your local machine.

10\. Open the **SlackService.js** file from the GitHub repo, found in the slack folder. Copy the entire contents of this js file into the Lambda inline edit window.

* This SlackService function will serve as the backend for a new /zombie/slack API resource you will create later. This function accepts incoming messages forwarded from Slack when you use the slash command, it then reformats the parameters and proxies the Slack messages to the zombie survivor chat service (/zombi/message) . This Lambda function verifies that the incoming message has the predefined Slack Token, and it also does a DynamoDB query against the Users table to validate that the user who submitted the message in Slack is a preconfigured survivor in our backend (Remember when you signed up for the chat, you provided your Slack username and team domain as part of the sign-up process). In this workshop, we're using this is as the way to authorize requests against the /zombie/slack resource.

11\. You should have saved the Slack Token string from earlier. Copy the Token string from Slack into the "token" variable on [line 15](/Slack/SlackService.js#L15) in the Lambda function, replacing the string **INSERT YOUR TOKEN FROM SLACK HERE** with your own token.

* Slack provides a unique token associated with your integration. You are copying this token into your Lambda function as a form of validation. When incoming requests from Slack are sent to your API endpoint, and your Lambda function is invoked with the Slack payload, your Lambda function will check to verify that the incoming Token in the request matches the Token you provided in the code. If the token does not match, Lambda returns an error and doesn't process the request.

12\. There are 4 variables you need to insert in the code to communicate with the backend.

a) In the "API" variable, you will insert the fully qualified domain name (FQDN) for your API. The **API.endpoint** variable should show a value of "INSERT YOUR API GATEWAY FQDN HERE INCLUDING THE HTTPS://" on [line 9](/Slack/SlackService.js#L9). Your final FQDN inserted into the code should look something like "https://xxxxxxxx.execute-api.us-west-2.amazonaws.com". This allows the SlackService function to communicate with your API.

b) You should also fill in the region code in the variable **API.region**. This should be the region where you launched CloudFormation.

c) Finally you will also copy in the name of your DynamoDB Users table that was created for you. This should be placed in the **table** variable. You will also need to copy in the name of your "slackindex" (this is an index that was created on the DynamoDB table to assist with querying). These attributes can be found in the Outputs section in CloudFormation. You should be copying the values for **DynamoDBUsersTableName** and **DynamoDBUsersSlackIndex** from CloudFormation.

13\. After you have copied the code into the Lambda inline code console and modified the variables, scroll down to the **Lambda function handler and role** section. For the role, select **Choose an existing role** from the dropdown and then select the role that looks like **[Your stack name]-ZombieLabLambdaRole...**. For simplicity we are reusing the same Lambda role for our functions.

14\. In the Advanced Settings, set the **Timeout** to **30** seconds. Then click **Next**.

15\. On the review page, make sure that everything looks correct.

16\. Click **Create function**. Your Lambda function will be created.

17\. When the function is created, navigate to the API Gateway service in the AWS Management Console. Click into your "Zombie Workshop API Gateway" API. On the left Resources pane, click/highlight the "/zombie" resource so that it is selected. Then select the **Actions** button and choose "Create Resource". For Resource Name, insert **slack** and for Resource Path, insert **slack**. Click "Create Resource" to create your slack API resource. The final resource for your Slack API should be as shown below.
![Create Slack API Resource](/Images/Slack-Step17.png)

*  In this step, you are creating a new API resource that the Slack slash command webhook can forward requests to. In the next steps, you'll create a POST method associated with this resource that triggers your Lambda function. When you type messages in Slack with the correct slash command, Slack will send requests to this resource, which will invoke your SlackService Lambda function to pre-process the payload and make a call to your /zombie/message endpoint to insert the data into DynamoDB.

18\. For your newly created "/slack" resource, highlight it, then click **Actions** and select **Create Method** to create the **POST** method for the /zombie/slack resource. In the dropdown, select **POST**. Click the checkmark to create the POST method. On the Setup page, choose an Integration Type of **Lambda Function**, and select the region that you are working in for the region dropdown. For the Lambda Function field, type "SlackService" for the name of the Lambda Function. It should autofill your function name. Click **Save** and then **OK** to confirm.

19\. Click **Integration Request** for the /slack POST method. We'll create a Mapping Template to convert the incoming query string parameters from Slack into JSON which is the format Lambda requires for parameters. This mapping template is required so that the incoming Slack message can be converted to the right format.

20\. Expand the **Body Mapping Templates** arrow and click **Add mapping template**. In the Content-Type box, enter **application/x-www-form-urlencoded** and click the little checkmark to continue. If a popup appears asking if you would like to secure the integration, click **Yes, secure this integration**. This ensures that only requests with the defined content-types will be allowed.

As you did in the Twilio lab, we're going to copy VTL mapping logic to convert the request to JSON. A new section will appear on the right side of the screen with a dropdown for **Generate Template**. Click that dropdown and select **Method Request Passthrough**.

In the text editor, delete all of the exiting VTL code and copy the following into the editor:

```
{"body": $input.json("$")}
```

Click the grey **Save** button to continue. The result should look like the screenshot below:

![Slack Integration Response Mapping Template](/Images/Slack-Step20.png)

21\. Click the **Actions** button on the left side of the API Gateway console and select **Deploy API** to deploy your API. In the Deploy API window, select **ZombieWorkshopStage** from the dropdown and click **Deploy**.

22\. On the left pane navigation tree, expand the ZombieWorkshopStage tree. Click the **POST** method for the **/zombie/slack** resource. You should see an Invoke URL appear for that resource as shown below.
![Slack Resource Invoke URL](/Images/Slack-Step22.png)

23\. Copy the entire Invoke URL. Navigate back to the Slack.com website to the Slash Command setup page and insert the Slack API Gateway Invoke URL you just copied into the "URL" textbox. Make sure to copy the entire url including "HTTPS://". Scroll to the bottom of the Slash Command screen and click **Save Integration**.

24\. You're ready to test out the Slash Command integration. In the team chat channel for your Slack account, type the Slash Command "/survivors" followed by a message. For example, type "/survivors Please help me I am stuck and zombies are trying to get me!". After sending it, you should get a confirmation response message from Slack Bot like the one below:
![Slack Command Success](/Images/Slack-Step24.png)

**LAB 4 COMPLETE**

Navigate to your zombie survivor chat app and you should see the message from Slack appear. You have configured Slack to send messages to your chat app!
![Slack Command in Chat App](/Images/Slack-Step25.png)

**Bonus Step:**

You've configured Slack to forward messages to your zombie survivor chat app. But can you get messages sent in the chat app to appear in your Slack chat (i.e.: the reverse)? Give it a try or come back and attempt it later when you've finished the rest of the labs! HINT: You'll want to configure Slack's "Incoming Webhooks" integration feature along with a Lambda code configuration change to make POST requests to the Slack Webhook whenever users send messages in the chat app!

* * *


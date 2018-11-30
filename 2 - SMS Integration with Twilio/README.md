# 2 - SMS Integration with Twilio

## Lab 2 - SMS Integration with Twilio

**What you'll do in this lab...**

In this section, you’ll create a free-trial Twilio SMS phone number. You will configure this Twilio phone number with a webhook to forward all incoming text messages sent to your Twilio number to the /zombie/twilio API resource in API Gateway. This will allow you to communicate with survivors in the chat room via text message.

**SMS Twilio Integration Architecture**
![Overview of Twilio Integration](/Images/TwilioOverview.png)

1\. Sign up for a free trial Twilio account at https://www.twilio.com/try-twilio. Or if you have an existing Twilio account, login.

2\. Once you have created your account, login to the Twilio console and navigate to the Home icon on the left navigation pane. On the Home screen/console dashboard, scroll down to the **Phone Numbers** section and click "Phone Numbers".
![Manage Twilio Phone Number](/Images/Twilio-Step2.png)

3\. On the Phone Numbers screen, click **Get Started** to assign a phone number to your account. Then click the red **Get your first Twilio phone number** button. We’re going to generate a 10-digit phone number in this lab, but a short-code would also work if preferred. This number should be enabled for voice and messaging by default. A popup will appear with your new phone number, click **Choose this number**. If the proposed phone number does not support messaging, click "Search for a different number", select your country and select the checkbox "SMS", then click "Search". Twilio propose a list of phone number, select "Choose number" for one of them. Then, type your address, click "Save and continue" and "Done".

* **International Users** - These are US phone numbers that you are provisioning in Twilio. You can also choose to configure an internationl number in Twilio, however there may be charges that apply. Currently this workshop only supports US phone numbers in the front end JS application due to the necessary formatting logic that has yet to be introduced into the code!

If you have an international mobile device, you can still do this lab. When registering for a user account in the zombie chat, just use a dummy placeholder 10 digit phone number for now. Later steps in this lab will illustrate a workaround that allows you to send SMS using your international phne number*

4\. Once you’ve received a phone number, click the **Manage Numbers** button on the left navigation pane. Click on your phone number, which will take you to the properties page for that number.

5\. Scroll to the bottom of the properties page, to the **Messaging** section. In the **Configure With** dropdown, select the **Webhooks/TwiML** option. Leave this page open for now and proceed to the next step.

* The Twilio webhooks section allows you to integrate your phone number with third party services. In this case, you're going to configure your Twilio phone number to forward any messages it receives over to your API Gateway /zombie/twilio resource with POST requests.

6\. Now you’ll retrieve your **/zombie/twilio** API endpoint from API Gateway and provide it to Twilio to hook up to AWS. Open the AWS Management console in a new tab, and navigate to API Gateway, as illustrated below. Be sure to leave the Twilio tab open as you’ll need it again to finish setup.
![API Gateway in Management Console](/Images/Twilio-Step6.png)

7\. In the API Gateway console, select your API.  Then on the left navigation tree, under your API, click **Stages**.
![API Gateway Resources Page](/Images/Twilio-Step7.png)

8\. With "Stages" selected, expand the "ZombieWorkshopStage" by clicking the blue arrow. Once expanded, select the **POST** method for the **/zombie/twilio** resource. The **/zombie/twilio** resource is the endpoint that we automatically created for you in CloudFormation for SMS integration with twilio.com. You should see an **Invoke URL** displayed for your **/zombie/twilio** resource, as shown below.
![API Gateway Invoke URL](/Images/Twilio-Step8.png)

9\. Copy the **Invoke URL** and return to the Twilio website. On the Twilio page that you left open, paste the Invoke URL from API Gateway into the text box next to the label **A message comes in**. Ensure that the request type is set to **HTTP POST**. This is illustrated below.
![Twilio Request URL](/Images/Twilio-Step9.png)

10\. Click **Save** to finalize the setup connecting Twilio to your API.

11\. You will now create the Lambda Function that processes your incoming Twilio messages, parses the message, and proxies it along to your /zombie/message Chat Service. To begin, navigate to the Lambda console.

* As you'll see throughout this workshop, we will leverage separate Lambda functions to pre-process data before sending standardized/formatted requests to the /zombie/message resource. This allows us to-reuse the existing DynamoDB logic sitting behind the /zombie/message resource rather than writing multiple separate functions that all interact with DynamoDB individually. As messages come in to your Twilio number, the Twilio webhook forwards them with HTTP POST requests to your /zombie/twilio resource, which will be integrated with a backend pre-processing Lambda function. This pre-processing function will strip apart the Twilio payload and format it before making a signed SigV4 HTTPS POST to your /zombie/message service which requires IAM authorization in order to be invoked.

12\. Click **Create a Lambda function** and select the blueprint titled **Blank Function** as we will be creating a brand new function. Click **Next** to skip through the Configure Triggers screen.

13\. Create a name for the function, such as **"[Your CloudFormation stack name]-TwilioProcessing"**. Set the "Runtime" as **Node.js 4.3**. In the source code found on Github, open the **TwilioProcessing.js** file found inside the **/Twilio** folder. Delete the sample code in the Lambda console editor and replace it with the entire contents from your TwilioProcessing.js file. Once you have copied the code into Lambda, scroll down to [line 8](/Twilio/TwilioProcessing.js#L8) in the code where the **API** variable is declared. **API.endpoint** should show a value of "INSERT YOUR API GATEWAY URL HERE INCLUDING THE HTTPS://". Please replace this string with the fully qualified domain name (FQDN) of the URL for your **/zombie/message** POST method found in API Gateway. For example, it should look something like "https://xxxxxxxx.execute-api.us-west-2.amazonaws.com".

You should also fill in the region code in the variable **API.region**. This should be the region where you launched CloudFormation.

Next, you will also copy in the name of your DynamoDB **Users** table that was created for you. This should be named as **[Your CloudFormation Stack Name]-users"**. You should copy this table name into the **table** variable in your Lambda code. You will also need to copy in the name of your "phoneindex" (this is an index that was created on the DynamoDB table to assist with querying). These attributes can be found in the Outputs section in CloudFormation. You should be copying the values for **DynamoDBUsersTableName** and **DynamoDBUsersPhoneIndex** from CloudFormation.

* Some of the functions in this workshop were originally authored for Nodejs 0.10 but are still capable of running in the Node4.3 runtimes +. The workshop will soon be upgraded to use the latest Nodejs runtime that is supported by Lambda.

14\. After you have copied the code into the Lambda inline code console and modified the variables, scroll down to the **Lambda function handler and role** section. **Choose an existing role** should be selected from the dropdown. Then for the existing **role**, select the role that looks like **[Your stack name]-ZombieLabLambdaRole...**. For simplicity we are reusing the same Lambda role for our functions.

15\. Under "Advancted settings", set the **Timeout** field to 30 seconds and keep all the rest of the defaults set. Then click **Next** and then **Create function** on the Review page to create your Lambda function.

* You have just created a Lambda function that is integrated as the backend for your /zombie/twilio resource POST method. The function converts the parameters to the correct format for our Chat Service including a conversion to JSON format, and makes an HTTPS POST request to the /zombie/message Chat Service resource. That endpoint will take care of inserting the data into the DynamoDB messages table.

16\. Now that you have created the TwilioProcessing function, you need to connect it to the **POST** method for your /zombie/twilio endpoint. Navigate back to the API Gateway console and select the **POST** method for your **/zombie/twilio** resource.

17\. On the **Method Execution** screen for the "POST" method, the "Integration Request" box should show a type of **MOCK** for your /twilio resource.

18\. You will now change the **Integration Request** so that instead of integrating with a Mock integration, it will integrate with your TwilioProcessing Lambda function. Click **Integration Request**. On the Integration Request screen, change the "Integration type" radio button to **Lambda Function**. In the "Lambda Region" dropdown, select the region in which you created your TwilioProcessing Lambda function, and where you launched your CloudFormation Stack. For the **Lambda Function**, begin typing "TwilioProcessing" and the autofill should display your function. Select your **TwilioProcessing** function from the autofill. Click **Save**. In the popup window, confirm that you want to switch to Lambda Integration by clicking **OK**. Then confirm that you want to give API Gateway permission to invoke your function by clicking **OK**. Wait a few seconds for the changes to save.

19\. You will be brought back to the Integration Request page for your "POST" method.

20\. Twilio sends data from their API with a content-type of "application/x-www-form-urlencoded", but Lambda requires the content-type to be "application/json" for any payload parameters sent to it. You will configure a Mapping Template so that API Gateway converts the content type of incoming messages into JSON before executing your backend Lambda TwilioProcessing function with the parameters.

21\. On the Integration Request screen for your /zombie/twilio POST method, expand the **Body Mapping Templates** section and click **Add mapping template**. In the textbox for "Content-Type", input **application/x-www-form-urlencoded** and click the little checkmark button to continue. Once you have clicked the little checkbox, a popup window will appear asking if you want to only allow requests that match the Content-Type you specified. Click **Yes, secure this integration**. A new section will appear below with a dropdown for **Generate Template**. Click that dropdown and select **Method Request Passthrough**.

22\. A "Template" text editor window will appear. In this section you will input a piece of VTL transformation logic to convert the incoming Twilio data to JSON format. In this text editor, **delete all of the pre-filled content** and copy the following code into the editor.

```{"postBody" : "$input.path('$')"}```

After copying the code into the editor, click the **Save** button. You have now setup the POST method to convert the incoming data to JSON anytime a POST request is made to your /zombie/twilio resource with a Content-Type of "application/x-www-form-urlencoded". This should look like the screenshot below:
![Twilio Integration Request Mapping Template](/Images/Twilio-Step22.png)

23\. Now that you have configured the Integration Request to transform incoming messages into JSON, we need to configure the Integration Response to transform outgoing responses back to Twilio into XML format since the Twilio API requires XML as a response Content-Type. This step is required so that when you send SMS messages to the survivor Chat Service, it can respond back to your Twilio Phone Number with a confirmation message that your message was received successfully.

24\. Head back to the Method Execution screen for the twilio POST method. On the "Method Execution" screen for your /zombie/twilio POST method, click **Integration Response**. On the "Integration Response" screen, click the black arrow to expand the method response section. Expand the **Body Mapping Templates** section. You should see a Content-Type of "application/json". We need a Content-Type of XML, not JSON, so **delete this Content-Type by clicking the little black minus icon** and click **Delete** on the pop-up window.

25\. Click **Add mapping template** similar to the way you did this in the earlier steps for the Integration Request section.

26\. In the "Content-Type" text box, insert **application/xml** and click the little black checkmark to continue. Similar to the steps done earlier, we are going to copy VTL mapping logic to convert the response data to XML from JSON. This will result in your /zombie/twilio POST method responding to requests with XML format. After you have created the new content-type, a new section will appear below with a dropdown for **Generate Template**. Click that dropdown and select **Method Request Passthrough**.
In the text editor, delete all the code already in there and copy the following into the editor:

```
#set($inputRoot = $input.path('$'))
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>
        <Body>
            $inputRoot
        </Body>
    </Message>
</Response>
```

Click the grey "Save" button to continue.

The result should look like the screenshot below:

![Twilio Integration Response Mapping Template](/Images/Twilio-Step26.png)

27\. Scroll up and click the blue **Save** button on the screen. Finally click the **Actions** button on the left side of the API Gateway console and choose **Deploy API** to deploy your API. In the Deploy API window, select **ZombieWorkshopStage** from the dropdown and click **Deploy**.

28\. You are now ready to test out Twilio integration with your API. Send a text message to your Twilio phone number from your mobile device.

**LAB 2 COMPLETE**

If the integration was successful, you should receive a confirmation response text message and your text message you sent should display in the web app chat room as coming from your Twilio Phone Number. You have successfully integrated Twilio text message functionality with API Gateway.

* **Troubleshooting tip**: If you are unable to send text messages, please ensure you are sending from the same phone number that you registered when you signed up for a survivor account in the Zombie Chat. If you review the TwilioProcessing Lambda function you will see that the code is checking the DynamoDB users table to confirm if the incoming message forward to us from Twilio was sent from an authorized phone number. Twilio provides that to us when it sends the message to our API.

* **For international users**: If you have an international phone number and want to send text messages -
  1. Modify your user record in the DynamoDB Users table with your correct International Phone Number. You need to do this in DynamoDB directly, because the JS chat application performs validation that requires a 10 digit US phone number on the client. After modifying this in DynamoDB, you should be able to send text messages to your Twilio phone number from your international phone number because the the Lambda phone number validation in the code will recognize your phone number.

* * *


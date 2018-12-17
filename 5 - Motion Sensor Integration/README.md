# Lab 5 - Motion Sensor Integration with Raspberry Pi and Grove Components

In this section, you'll help protect suvivors from zombies. Zombie motion sensor devices allow communities to determine if zombies (or intruders) are nearby. You'll setup a Lambda function to consume motion sensor events from an IoT device and push the messages into your chat application.

**IoT Integration Architecture**
![Zombie Sensor IoT Integration](/Images/EdisonOverview.png)

####Creating the AWS Backend

**If you are following this guide during a workshop presented by AWS, please ignore the steps below, 1-3\. An SNS topic should already be configured for the workshop participants to consume messages from. That SNS topic ARN will be provided to you.**

1\. Create the SNS Topic. Navigate to the SNS product page within the AWS Management Console and click **Topics** in the left hand menu. Then click on 'Create New Topic'. You will be presented with the following window. Fill in the fields with your desired values and click create topic.
![Create Topic Screenshot](/Images/MotionSensor-createTopic.png)

2\. You will now need to edit the topic policy to permit any AWS account to subscribe lambda functions to your SNS topic. Select the check box next to your new topic, and then click **Actions -> Edit topic policy**. You need to configure these settings presented as shown the below screenshot. Then click **Update Policy**. This part is what allows others (perhaps teammates working on this lab with you, to consume notifications from your SNS topic.
![Edit Topic Policy Screenshot](/Images/MotionSensor-createTopicPolicy.png)

3\. You now have your central SNS topic configured and ready to use. Ensure that you make a note of the Topic ARN and region where you have created the topic, you will need it in some of the following steps.

####Installing the application on the Intel Edison
**If you are following this guide during a workshop presented by AWS, please ignore this section. An Intel Edison board should already be configured for the workshop particants to consume messages from.**

1\. First, you will need to get your Edison board set up. You can find a getting started guide for this on the Intel site [here](https://software.intel.com/en-us/articles/assemble-intel-edison-on-the-arduino-board). Note that for the purpose of this tutorial, we will be writing our client code for the Edison in Node.js and will therefore be using the Intel® XDK for IoT (referred to as 'XDK' from here on, and which you will need to install) as our IDE.

2\. You will need to physically connect the Grove PIR Motion Sensor to pin D6 on the breakout board.

3\. Download all of the code from the 'zombieIntelEdisonCode' folder in the GitHub repository and store it in a folder locally on your machine. This simply consists of a main.js file (our application) and our package.json (our app dependencies).

4\. Navigate to the homepage in the XDK and start a new project.

5\. Choose to import an existing Node.js project and select the folder where you stored the code from this repository in the previous step.

6\. Give your project a name. We called ours **zombieSensor**.

7\. You now need to edit the code in main.js to include your AWS credentials and the SNS topic that you have created. Firstly, we'll need some AWS credentials.

8\. You will need to create an IAM User with Access and Secret Access Keys for your Edison to publish messages to your SNS topic. There is a guide on how to create IAM Users [here](http://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html). Your IAM policy for the user should look like the following:

```
{
    "Version": "2012-10-17",
    "Statement": [{
        "Action": [ "sns:Publish" ],
        "Effect": "Allow",
        "Resource": "ENTER YOUR SNS TOPIC ARN HERE"
    }]
}
```

9\. Now let's add your credentials to the client side code. Edit the following line in main.js to include your user access keys and the region where you have set up your SNS topic.

``` AWS.config.update({accessKeyId: 'ENTER ACCESSKEY HERE', secretAccessKey: 'ENTER SECRET ACCESS KEY HERE', region: 'ENTER REGION HERE'}); ```

10\. Edit the following line in main.js to reflect the region in which you created the SNS topic.

``` var sns = new AWS.SNS({region: 'ENTER REGION HERE'}); ```

11\. Edit the following line in main.js to reflect the Amazon Resource Name (ARN) of the SNS topic that you created earlier.

``` TopicArn: "ENTER YOUR SNS TOPIC ARN HERE" ```

12\. You now need to connect the XDK to your Intel Edison device. There is a guide on the Intel site on how to do this [here](https://software.intel.com/en-us/getting-started-with-the-intel-xdk-iot-edition) under the 'Connect to your Intel® IoT Platform' section.

13\. You now need to build the app and push it to your device. First, hit the build/install icon, this looks like a hammer in the XDK. It may take a couple of minutes to install the required packages etc.

14\. Once the app has been built succesfully, you can run the app by pressing the run icon, this looks like a circuit board with a green 'play' sign.

15\. Your app should now be running on the Edison device and your messages being published to the SNS topic. You can consume these messages using AWS Lambda. There is some documentation to get you started [here](http://docs.aws.amazon.com/sns/latest/dg/sns-lambda.html). Continue below to learn how to integrate the SNS notifications into the chat application.

####Consuming the SNS Topic Messages with AWS Lambda

Using the things learned in this workshop, can you develop a Lambda function that alerts survivors in the chat application when zombies are detected from the zombie sensor? In this section you will configure a Lambda function that triggers when messages are sent from the Edison device to the zombie sensor SNS topic. This function will push the messages to the chat application to notify survivors of zombies!

1\. Open up the Lambda console and click **Create a Lambda function**.

2\. On the blueprints screen, click **Skip** as we won't use one.

3\. On the next page (**Configure Triggers**), click the empty field next to the AWS Lambda logo and select SNS as an event source.

![Setup SNS as an Event Trigger for Lambda](/Images/Sensor-Step3.png)

* For the SNS topic selection, either select the SNS topic from the dropdown you created earlier (if you're working on this outside of an AWS workshop) or if you are working in an AWS workshop, insert the shared SNS topic ARN provided to you by the organizer. Make sure the trigger checkbox option is set to enabled so that your Lambda function will immediately begin processing messages. Click **Next**.

* The SNS Topic ARN provided by AWS (if in a workshop) is not in your AWS account and will not display in your dropdown of choices. It is an ARN provided by AWS in a separate account and needs to be typed in.

4\. On the "Configure Function" screen, name your function "[Your CloudFormation Stack Name]-sensor". Now open the **exampleSNSFunction.js** file from the workshop GitHub repository. It is located [here](/zombieSensor/lambda/exampleSNSFunction.js). Copy the entire contents of this JS file into the empty Lambda code editor.

When you've copied the code into the Lambda browser editor, locate the variable **API**. Replace the variable **API.endpoint** with your /zombie/message/post endpoint. It should look like **https://xxxxxxxx.execute-api.us-west-2.amazonaws.com**. This is the "Invoke URL" which you can grab from the Stages page in the API Gateway console. Remember, don't insert anything after the ".com" portion, the function fills in the rest of the resource path for you. You also should insert the region for your API in the **API.region** variable.

5\. For the **Role**, leave the option as **Choose an existing role**. Then in the "Existing Role" dropdown, select the ZombieLabLambdaRole that was created for you by CloudFormation. It should look like "[Your CloudFormation stack name]-ZombieLabLambdaRole".

6\. Set the **Timeout** to **30** seconds. Leave all other options as default on the Lambda creation page and click **Next**.

7\. On the Review page, click **Create function**.

8\. That's it! When your function is created, head on over to your survivor chat application. If your session has expired you may need to login again.

* Almost immediately you should begin seeing zombie sensor messages showing up in the chat application which means your messages are successfully sending from the Intel Edison device to the Zombie Sensor SNS Topic. Any survivors with Lambda functions subscribed to this topic will get notifications in their team's survivor chat service.  

* This Lambda Function takes the zombie sensor message from SNS, parses it, and makes an AWS SigV4 signed HTTPS POST request to your API Gateway message endpoint. That endpoint inserts the record into DynamoDB as a message making it available to the application on subsequent poll requests.

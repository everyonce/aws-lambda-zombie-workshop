### Let's Begin! Launch the CloudFormation Stack
*Prior to launching a stack, be aware that a few of the resources launched need to be manually deleted when the workshop is over. When finished working, please review the "Workshop Cleanup" section to learn what manual teardown is required by you.*

1\. To begin this workshop, **click one of the 'Deploy to AWS' buttons below for the region you'd like to use**. This is the AWS region where you will launch resources for the duration of this workshop. This will open the CloudFormation template in the AWS Management Console for the region you select.

Region | Launch Template
------------ | -------------
**N. Virginia** (us-east-1) | [![Launch Zombie Workshop Stack into Virginia with CloudFormation](/Images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=zombiestack&templateURL=https://s3.amazonaws.com/aws-zombie-workshop-us-east-1/CreateZombieWorkshop.json)
**Ohio** (us-east-2) | [![Launch Zombie Workshop Stack into Ohio with CloudFormation](/Images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=zombiestack&templateURL=https://s3-us-east-2.amazonaws.com/aws-zombie-workshop-us-east-2/CreateZombieWorkshop.json)
**Oregon** (us-west-2) | [![Launch Zombie Workshop Stack into Oregon with CloudFormation](/Images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=zombiestack&templateURL=https://s3-us-west-2.amazonaws.com/aws-zombie-workshop-us-west-2/CreateZombieWorkshop.json)
**Ireland** (eu-west-1) | [![Launch Zombie Workshop Stack into Ireland with CloudFormation](/Images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=zombiestack&templateURL=https://s3-eu-west-1.amazonaws.com/aws-zombie-workshop-eu-west-1/CreateZombieWorkshop.json)
**Frankfurt** (eu-central-1) | [![Launch Zombie Workshop Stack into Frankfurt with CloudFormation](/Images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?stackName=zombiestack&templateURL=https://s3-eu-central-1.amazonaws.com/aws-zombie-workshop-eu-central-1/CreateZombieWorkshop.json)
**Tokyo** (ap-northeast-1) | [![Launch Zombie Workshop Stack into Tokyo with CloudFormation](/Images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=zombiestack&templateURL=https://s3-ap-northeast-1.amazonaws.com/aws-zombie-workshop-ap-northeast-1/CreateZombieWorkshop.json)
**Seoul** (ap-northeast-2) | [![Launch Zombie Workshop Stack into Seoul with CloudFormation](/Images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?stackName=zombiestack&templateURL=https://s3-ap-northeast-2.amazonaws.com/aws-zombie-workshop-ap-northeast-2/CreateZombieWorkshop.json)
**Singapore** (ap-southeast-1) | [![Launch Zombie Workshop Stack into Singapore with CloudFormation](/Images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?stackName=zombiestack&templateURL=https://s3-ap-southeast-1.amazonaws.com/aws-zombie-workshop-ap-southeast-1/CreateZombieWorkshop.json)
**Sydney** (ap-southeast-2) | [![Launch Zombie Workshop Stack into Sydney with CloudFormation](/Images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=zombiestack&templateURL=https://s3-ap-southeast-2.amazonaws.com/aws-zombie-workshop-ap-southeast-2/CreateZombieWorkshop.json)

*If you have CloudFormation launch FAILED issues, please try launching in us-east-1 (Virginia)*

2\. Once you have chosen a region and are inside the AWS CloudFormation Console, you should be on a screen titled "Select Template". We are providing CloudFormation with a template on your behalf, so click the blue **Next** button to proceed.

3\. On the following screen, "Specify Details", your Stack is pre-populated with the name "zombiestack". You can customize that to a name of your choice **less than 15 characters in length** or leave as is. For the parameters section, if you want to develop with a team and would like to create IAM Users in your account to grant your teammates access, then specify how many teammates/users you want to be created in the **NumberOfTeammates** text box. Otherwise, leave it defaulted to 0 and no additional users will be created. The user launching the stack (you) already have the necessary permissions. Click **Next**.

*If you create IAM users, an IAM group will also be created and those users will be added to that group. On deletion of the stack, those resources will be deleted for you.*

4\. On the "Options" page, leave the defaults and click **Next**.

5\. On the "Review" page, verify your selections, then scroll to the bottom and select the checkbox **I acknowledge that AWS CloudFormation might create IAM resources**. Then click **Create** to launch your stack.

6\. Your stack will take about 3 minutes to launch and you can track its progress in the "Events" tab. When it is done creating, the status will change to "CREATE_COMPLETE".

7\. Click the "Outputs" tab in CloudFormation and click the link for "MyChatRoomURL". This should open your chat application in a new tab. Leave this tab open as you'll come back to it later.

Please continue to the next section for the required Cognito User Pools authentication setup.

## Setup Authentication with Cognito User Pools (Required)

The survivor chat uses [Amazon Cognito](https://aws.amazon.com/cognito/) for authentication. Cognito Federated Identity enables you to authenticate users through an external identity provider and provides temporary security credentials to access your app’s backend resources in AWS or any service behind Amazon API Gateway. Amazon Cognito works with external identity providers that support SAML or OpenID Connect, social identity providers (such as Facebook, Twitter, Amazon) and you can also integrate your own identity provider.

In addition to federating 3rd party providers such as Facebook, Google, and other providers, Cognito also offers a new built-in Identity Provider called [Cognito User Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html).

A Cognito Federated Identity pool has already been created for you when you launched CloudFormation.

You will now setup the Cognito User Pool as the user directory of your chat app survivors and configure it as a valid Authentication Provider with the Cognito Federated Identity Pool. API Gateway has been configured with IAM Authorization to only allow requests that are signed with valid AWS permissions. When a user signs into the Survivor Chat App (User Pool) successfully, a web call is made to the Cognito Federated Identity Pool to assume temporary AWS credentials for your authenticated user. These credentials are used to make signed [AWS SigV4](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html) HTTPS requests to your message API.

![Overview of Cognito Authentication](/Images/CognitoOverview.png)

**Let's get started...**

1\. Navigate to the Cognito service console.

![Navigate to the Cognito service](/Images/Cognito-Step1.png)

Cognito User Pools is not available in all AWS regions. Please review the list [here](https://docs.aws.amazon.com/general/latest/gr/rande.html#cognito_identity_region) for the regions that Cognito is available in. Therefore if you launched your CloudFormation stack in any region other than one of those listed on the above website, then please use the top navigation bar in the management console to switch AWS regions and navigate to **us-east-1 (Virginia)** to configure Cognito. Your application will stay hosted in the region you launched the CloudFormation template, but the authentication with Cognito will reside in us-east-1 (Virginia). If you launched the Cloudformation stack in one of those regions where Cognito exists, then please simply navigate to the Cognito service in the AWS Management Console as the service is available in that region already and you will configure it within that region.

When inside the Cognito service console, click the blue button **Manage your User Pools**. You will setup the user directory that your chat application users will authenticate to when they use your app.

2\. Click the blue button **Create a User Pool** in the upper right corner. You'll create a new user directory.

3\. In the "Pool Name" text box, name your user pool **[Your CloudFormation stack name]-userpool**. For example, if you named your CloudFormation stack "sample" earlier, then your user pool name would be "sample-userpool". After naming your User Pool, click **Step through Settings** to continue with manual setup.

4\. On the attributes page, select the "Required" checkbox for the following attributes: **email, name, phone number**.

* Cognito User Pools allows you to define attributes that you'd like to associate with users of your application. These represent values that your users will provide when they sign up for your app. They are available to your application as a part of the session data provided to your client apps when users authenticate with Cognito.

5\. Click the link "Add custom attribute". Leave all the defaults and type a "Name" of **slackuser** exactly as typed here. Add 2 additional custom attributes: **slackteamdomain** and **camp**.

* Within a User Pool, you can specify custom attributes which you define when you create the User Pool. For the Zombie Survivor chat application, we will include 3 custom attributes.

Your attributes configuration should match the image below:

![Cognito User Pools: Attributes Configuration](/Images/Cognito-Step5.png)

Click **Next Step**.

6\. On the Policies page, leave the Password policy settings as default and click **Next step**.

7\. On the verifications page, leave the defaults and click **Next step**.

* We will not require MFA for this application. However, for during sign up we are requiring verification via email address. This is denoted with the email checkbox selected for "Do you want to require verification of emails or phone numbers?". With this setting, when users sign up for the application, a confirmation code will be sent to their email which they'll be required to input into the application for confirmation.

8\. On the "Message Customizations" page, in the section titled **Do you want to customize your email verification message?** add a custom email subject such as "Signal Corps Survivor Confirmation". We won't modify the message body but you could add your own custom message in there. We'll let Cognito send the emails from the service email address, but in production you could configure Cognito to send these verifications from an email server you own. Leave the rest of the default settings and click **Next step**.

On the Tags page, leave the defaults and click **Next step**. Next, on the Devices page, leave the default option of "No" selected. We will not configure the User Pool to remember user's devices.

9\. On the Apps page, click **Add an app**. In the **App Name** textbox, type "Zombie Survivor Chat App" and **deselect the client secret checkbox**. Click **Set attribute read and write permissions**. You need to make sure that the app has "writable" and "readable" access to the attributes you created. Make sure that **all of the checkboxes are selected** for "Readable Attributes" and "Writable Attributes". Then click **Create app**, and then click **Next step**.

10\. In the dropdowns for the **Pre authentication** and **Post confirmation** triggers, select the Lambda function named "[Your CloudFormation Stack name]-CognitoLambdaTrigger-[Your Region]". Click **Next step**.

* Cognito User Pools allows developers to inject custom workflow logic into the signup and signin process. This custom workflow logic is represented with AWS Lambda functions known as Lambda Triggers.

* With this feature, developers can pass information to a Lambda function and specify that function to invoke at different stages of the signup/signin process, allowing for a serverless and event driven authentication process.

* In this application, we will create two (2) Lambda triggers:

    * Post-Confirmation: This trigger will invoke after a user successfully submits their verification code upon signup and becomes a confirmed user. The Lambda function associated with this trigger takes the attributes provided by the user and inserts them into a custom Users table in DynamoDB that was created with CloudFormation. This allows us to perform querying of user attributes within our application.

    * Pre-Authentication: This trigger will invoke when a user's information is submitted for authentication to Cognito each time the survivor signs into the web application. The code for with this Lambda Trigger takes the user's attributes have been passed in as parameters from the invoking User Pool and using them to perform an update on the User's record in DynamoDB Users table. This allows us to load the user's data into DynamoDB when they initially sign in and also keep it current with the values in User Pools in an on-going basis as they log in each time.

    * For this workshop we use the same backend Lambda function for both of the triggers. On invocation, the function checks what type of even has occurred, Post-Confirmation or Pre-Authentication, and executes the correct code accordingly.

11\. Review the settings for your User Pool and click **Create pool**. If your pool created successfully you should be returned to the Pool Details page and it will display a green box that says "Your user pool was created successfully".

12\. Open a text editor on your computer and copy into it the "Pool Id" displayed on the Pool details page. Then click into the **Apps** tab found on the left side navigation pane. You should see an **App client id** displayed. Copy that **App client id** into your text editor as well.

You are done configuring the User Pool. You will now setup federation into the Cognito Identity Pool that has already been created for you.

* An [Amazon Cognito Identity Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-identity.html) has been configured for you. Identity Pools allow external federated users to assume temporary credentials from AWS to make service API calls from within your apps.

* You've just created the User Pool for authentication into your app. Now your users still need access to make IAM Authorized AWS API calls.

* You'll setup federation inside of Cognito Identity and allow your User Pool as an **Authentication Provider**.

On the top navigation bar in the management console, switch to **Federated Identities** by clicking the link as shown below.

![Navigating to Federated Identities Console](/Images/Cognito-Step12.png)

13\. Click into the Identity Pool that has already been created for you. It should be named "[Your CloudFormation stack name] _ identitypool". On the Idenity pool dashboard, in the upper right, select **Edit identity pool**.

14\. Cognito Identity allows you to give access to both authenticated users and unauthenticated (guest) users. The permissions associated with these groups of users is dictated by the IAM role that you attach to these Cognito roles. Your Authenticated and Unauthenticated Cognito roles have already been configured for you in CloudFormation. The Authenticated role has been configured to give permissions to the principal (your Cognito authenticated application user) to make "execute-api:invoke" calls to the API Gateway endpoint ARNs associated with the survivor serverless app.

* When users authenticate into the application, they become an authenticated user, and the application allows them to send chat messages to the survivor chat.

15\. Click the black dropdown arrow in the section titled "Authentication providers". You will configure your Identity pool to allow federated access from your Identity Provider, your Cognito User Pool. In the "Cognito" identity provider tab, insert your **User Pool ID** and **App Client ID** into their respective text boxes from your text editor file. Do not delete them from the text file, you'll need these items again in a later step.

You should have copied these from your User Pool earlier when you set it up. If you do not have these copied, please navigate back to your Cognito User Pool you created earlier and locate your User Pool Id and App Client ID.

Scroll to the bottom of the page and click **Save Changes** to save the User Pool configuration settings. Your Cognito Federated Identiy Pool has been configured with Congito User Pool as an IdP. When users authenticate to the User Pool, they will assume temporary credentials with the permissions allowed via the Authenticated Role.

16\. You will now make an update to an application config file so that the serverless Javascript application can communicate with your User Pool to log users in.

Navigate to the Amazon S3 console **in the region where you launched your CloudFormation stack.**

* If you changed regions to configure Cognito, please return back to the region where you launched the stack and navigate to the S3 service.

![Navigate to the S3 service](/Images/Cognito-Step16.png)

17\. On the Amazon S3 buckets listing page, find and click into the bucket that was created for you by CloudFormation. It should be named with your stack name prepended to the beginning. Something like [CloudFormation Stack Name]-s3bucketforwebsitecontent"....

* In the S3 Console search bar you can type **s3bucketforwebsitecontent** and your S3 bucket will display.

18\. This bucket contains all the contents for hosting your serverless JS app as well as the source code for the workshop's Lambda functions and CloudFormation resources. Please do not delete these contents. Click into the folder (prefix) named **S3** and navigate through to the file **S3/assets/js/constants.js**

Download the **S3/assets/js.constants.js** file to your local machine and open it with a text editor.

![Download the constants.js file](/Images/Cognito-Step18.png)

19\. Open up the constants.js file and copy over the User Pool ID into the "USER_POOL_ID" variable. Then copy the App Client ID into the "CLIENT_ID" variable. These should be copied from the open text file you had open from earlier.

* Your serverless javascript zombie application requires this constants values in file communicate with the different services of the workshop.

* The Identity Pool Id was automatically filled in with several other variables when the CloudFormation template was launched.

20\. Save the constants.js file and upload it back to S3. While in the S3 console window, make sure you are in the **js** directory. Click the blue **Upload** button and upload the constants.js file from your local machine. Within the upload dialog, select the "Manage public permissions" dropdown and set the permissions on the file to read-only for the public by selecting the **Read** checkbox next to Everyone under the Objects category. You can also drag your file from your local machine into the S3 browser console to initiate an upload and then when the object is uploaded, make sure to select **Make Public**.

* Your application now has the configuration it needs to interact with Cognito.

21\. Navigate back to CloudFormation and find the Chat Room URL (MyChatRoomURL) in the Outputs tab of your CloudFormation stack. Click it to open the chat application in a new browser window.

* If you already had the application opened in your browser, please refresh the page so that the new constants.js loads with the app.

22\. You should see a sign in page for the Zombie survivor web app. You need to create an account so click **Sign Up**.

23\. Fill out the form to sign up as a survivor.

* **Select your Camp**: Specify the geography where you live! Currently this attribute is not used in the application and is available for those that want to tackle an extra credit opportunity!. When you're done with the workshop, try and tackle the Channel Challenge in the Appendix.

* **Slack Username**: Type the Slack Username you will use during the Slack lab of this workshop. This associates your Slack username with your Survivor app user account and is required if you want to do the Slack lab.

* **Slack Team Domain Name**: Slack users can be members of many teams. Type the Slack team domain name that you want to integrate with this survivor chat app. The combination of a Slack team domain and Slack Username will unique identity a user to associate with your new Survivor chat app account.

When done, click **Sign Up**.

24\. A form should appear asking you to type in your confirmation code. Please check your inbox for the email address you signed up with. You should received an email with the subject "Signal Corps Survivor Confirmation" (May be in your Spam folder!). Copy over the verification code and enter into the confirmation window.

**Troubleshooting tips:**

* If you are getting errors during the signup, please revisit the settings for your Cognito User Pool. You need to make sure that you've done the following -  

    * Configured your Cognito Lambda triggers for both the **Pre-Authentication** and **Post-Confirmation** steps as described in Step 10.

    * Properly modified the constants.js config file and re-uploaded it to the JS directory for your application in S3. After you uploaded this constants.js file, you should have refreshed your zombie chat browser application page so that it could pull down the latest JS files. The application is client-side and needs this file's properties in order to bootstrap itself.

* Users created in the application are also stored in a DynamoDB table named "Users". If you did not have your Cognito triggers set up correctly, you will need to navigate to the DynamoDB Users table and delete the entry for your user. You can then re-register in the application again.


![Confirm your signup](/Images/Cognito-Step24.png)

After confirming your account, sign in with your credentials and begin chatting! You should see a red button called **Start Chatting** - click that button to toggle your session on. You may then begin typing messages followed by the "Enter" key to submit them.

25\. Your messages should begin showing up in the central chat pane window. Feel free to share the URL with your teammates, have them signup for accounts and begin chatting as a group! If you are building this solution solo, you can create multiple user accounts with different email addresses. Then login to both user accounts in different browsers to simulate multiple users.

**The baseline chat application is now configured and working! There is still important functionality missing and the Lambda Signal Corps needs you to build it out...so get started below!**

*This workshop does not utilize API Gateway Cache. Please KEEP THIS FEATURE TURNED OFF as it is not covered under the AWS Free Tier and will incur additional charges. It is not a requirement for the workshop.*

## Appendix

* Channel Challenge: Currently all messages sent in the survivor app are saved in the database with a channel of 'default' - all survivors can see these messages. Your challenge is to modify the application so that users have the option to scope their messages to only display to survivors in the same "Camp" (Camp is an attribute that is collected from users when they sign up for a user account). You will need to modify the JS application as well as the backend messages database and Lambda functions to work with this "Camp" attribute instead of the existing 'channel' attribute.

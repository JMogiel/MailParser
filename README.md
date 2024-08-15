# MailParser

## How to setup google account:
1. Go to https://console.cloud.google.com on your Gmail account you want to read emails
2. Create New Project
3. Select newly created project
4. Go to APIs & Services
5. On the left side of the screen choose OAuth consent screen
6. Select "External" and click on "CREATE" button
7. Fill all the required fields
8. Click on "SAVE AND CONTINUE" button
9. On "Scopes" tab click "SAVE AND CONTINUE" button
10. On "Test users" tab click on "+ ADD USERS" and add your email address
11. Click on "SAVE AND CONTINUE" button
12. Click on "BACK TO DASHBOARD" button
13. Now go to "Credentials" on the left side of the screen
14. At the top of the page choose "+ CREATE CREDENTIALS"
15. Choose "OAuth client ID"
16. In the "Application type" choose "Web application"
17. Field "Name" can be whatever
18. Click on "+ ADD URI" in "Authorized redirect URIs"
19. Add those two URIs: "http://localhost:8080/" and "http://localhost:8080"
20. Click "CREATE" button
21. New pop-up should show up with information about "OAuth client created"
22. #### Download JSON. Don't show this to anyone, with this JSON it is possible to access your Google Account!!!
23. At the top of the page look for "Gmail API"
24. Click on "ENABLE" button
25. That's it code now should work with your Gmail account

## How to run code:
1. First of all you need to install all the necessary libraries
2. Place requirements.txt in directory where you are planning to run the command/code
3. Type this command into terminal in OS or in your IDE: "pip install -r requirements.txt"
4. All necessary libraries should be installed
5. Now first of all run our api_mockup.py code
6. Be sure that your downloaded JSON is in the same directory as main.py, downloaded file should be named "client_secret.json"
7. Send yourself mail with such message: "delete, 519876231"
8. Secondly run main.py
9. Authorize yourself in the browser, look on the output on your console/terminal
10. Code should work ;)
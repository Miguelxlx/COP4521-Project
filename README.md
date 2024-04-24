# Group 26: Basketball Wagering App

## Group Members
- **Osher Steel**
- **Miguel Montesinos**
- **Jared Braswell**
- **Drake Phousirith**


## Project Description
The goal of this application is to create a basketball wagering app in which users can track their sports betting performance without using real money. The app offers bets on daily NBA games offering wagers on the head-to-head or over/under. The app keeps track of all transactions placed and refreshes regularly to check the bets placed against the outcome of the games. Users also have the option to upgrade their account to premium to get visual analytics on their profits over time.

## How to Use


## How to Compile and Execute
### Requirements
- **LIBRARIES**
Backend
- Flask
- flask_cors
- pymongo
- json
- os
- bcrypt
- datetime
- requests

Frontend
- npm


### Initial Setup
**STEPS FOR SETUP GO HERE** such as "clone the git repository" and ```npm install react-scripts```

### Running the Application
- **Note**: We are using cloud.mongodb to store information in our database such as bettingData, account info, transactions, etc. Because of that, we cannot connect via FSU networks.
- We also ran this in VSCode

First start the backend of the application by navigating to the COP4521-Project/old_version/backend2 directory and running:
```
python3 main.py
```
This will connect MongoDB to the frontend when the application starts.

Run the frontend by navigating to the COP4521-Project/old_version/frontend directory and executing the command:
```
npm start
```
This will start the web application. (Drake: For me it doesn't show on localhost:5000 but shows on the network address. Probably because main.py is running in backend2.)

**ALSO** do you think Sharanya will try to run the app on her Ubuntu environment?

## Bugs
- **Document known bugs here if there are any**


## Separation of Work

- **Osher Steel**
    - API logic for the odds and nba apis
    - Route functions for the frontend 
- **Miguel Montesinos**
- **Jared Braswell**
- **Drake Phousirith**


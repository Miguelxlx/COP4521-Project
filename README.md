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
Backend: Ensure these Python3 libraries are installed using pip.
- Flask
- flask_cors
- pymongo
- json
- os
- bcrypt
- datetime
- requests
- python-dotenv

Frontend:
On a Linux machine:
- sudo apt install npm


### Initial Setup
After ensuring the requirements above are installed. Run the following commands to install the dependencies required by npm to run the frontend.
```
npm install
npm install react-scripts
```

### Running the Application
- **Note**: We are using cloud.mongodb to store information in our database such as bettingData, account info, transactions, etc. Because of that, we cannot connect via FSU networks.
- We also ran this in VSCode

First start the backend of the application by running main.py located in the backend directory.
```
python3 ./backend/main.py
```
This will connect MongoDB to the frontend when the application starts.

Run the frontend by navigating to the COP4521-Project/frontend directory and executing the command:
```
npm start
```
This will start the web application.

## Functionality
A user can register an account by navigating to the Sign In page and clicking register. Once they create an account by entering their username, email, and password, the information will be stored in MongoDB and they will be a regular "free" user.

The user once signed in will be able to add bets to their betslip and submit the betslip if they have sufficient balance. Users will be able to see their transactions and placed bets by clicking on the associated tabs in the header of the webpage.

In the profile screen, users can add to their balance by typing in the amount they want to add and clicking Add Balance. They can also upgrade to a premium user by clicking the Upgrade button, where $15 will be subtracted from their balance and they will become a "premium" user in the database.

Premium users will be able to see their profit overtime in the profile screen after upgrading.

Admin users

## Bugs
- **Document known bugs here if there are any**


## Separation of Work

- **Osher Steel**
    - API logic for the odds and nba apis
    - Route functions for the frontend 
- **Miguel Montesinos**
- **Jared Braswell**
- **Drake Phousirith**


# Group 26: Basketball Wagering App

## Group Members
- **Osher Steel**
- **Miguel Montesinos**
- **Jared Braswell**
- **Drake Phousirith**

## How to Compile and Execute
### Requirements
- **ADD REQUIREMENTS SUCH AS LIBRARIES, DEPENDENCIES, ETC.**
- Flask
- pymongo
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

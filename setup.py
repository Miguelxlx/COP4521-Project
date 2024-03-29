import sqlite3

conn = sqlite3.connect('bettingData.db')
print('Opened database successfully')

conn.execute('''
    CREATE TYPE StatusType AS ENUM ('ACTIVE','LIMITED,'SUSPENDED', 'BANNED');
             
    CREATE TABLE IF NOT EXISTS Account(
        AccountID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username VARCHAR(20),
        Status StatusType,
        Email VARCHAR(30),
        Password VARCHAR(20),
        Balance FLOAT,
    )
''')
print('Table Accounts created successfully')

conn.execute('''
    CREATE TABLE IF NOT EXISTS Transaction(
        TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
        AccountID INTEGER,
        Date Datetime,
        Amount FLOAT,
             
        FOREIGN KEY (AccountID) REFERENCES Accounts (AccountID),
    );
''')
print('Table Transactions created successfully')

conn.execute('''
    CREATE TABLE IF NOT EXISTS BetsInTransaction(
        TransactionID INTEGER,
        BetID INTEGER,
    
        PRIMARY KEY(TransactionID,BetID),
        FOREIGN KEY (TransactionID) REFERENCES Accounts (TransactionID),
        FOREIGN KEY (BetID) REFERENCES Accounts (BetID)
    );
''')

# The Bet Info is described as such
# The first letter describe the type of bet and what position the user placed
# O:Over U:Under W:Home team win L:Home team loss
# For O and U, it will be followed by a number which described the line
# Ex: O225- the user bet the total points of the game to be over 225


conn.execute('''
    CREATE TABLE IF NOT EXISTS Bet(
        BetID INTEGER PRIMARY KEY AUTOINCREMENT,
        GameID INTEGER,
        BetInfo VARCHAR(5),
        
        FOREIGN KEY (GameID) REFERENCES Game (GameID),
    )
''')
print('Table Bets created successfully')

conn.execute('''
    CREATE TABLE IF NOT EXISTS Game(
        GameID INTEGER PRIMARY KEY AUTOINCREMENT,
        Date DATETIME,
        HomeTeam VARCHAR(3),
        AwayTeam VARCHAR(3),
        HomeFinalScore INTEGER,
        AwayFinalScore INTEGER,
    )
''')
print('Table Games created successfully')

conn.execute('''
    CREATE ROLE Admin;  
    GRANT UPDATE ON Account to Admin;
    GRANT Admin to Someone;
''')

conn.close()
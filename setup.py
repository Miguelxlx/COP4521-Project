import sqlite3

conn = sqlite3.connect('bettingData.db')
print('Opened database successfully')

conn.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT,
        Email TEXT,
        Password TEXT
    )
''')
print('Table Users created successfully')

conn.execute('''
    CREATE TABLE IF NOT EXISTS Accounts (
        AccountID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        Balance FLOAT,
        FOREIGN KEY (UserID) REFERENCES Users (UserID)
    )
''')
print('Table Accounts created successfully')

conn.execute('''
    CREATE TABLE IF NOT EXISTS Transactions (
        TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
        AccountID INTEGER,
        TransactionType TEXT,
        Amount FLOAT,
        TransactionDate DATETIME,
        FOREIGN KEY (AccountID) REFERENCES Accounts (AccountID)
    )
''')
print('Table Transactions created successfully')

conn.execute('''
    CREATE TABLE IF NOT EXISTS Events (
        EventID INTEGER PRIMARY KEY AUTOINCREMENT,
        EventName TEXT,
        EventDate DATETIME,
        EventStatus TEXT
    )
''')
print('Table Events created successfully')

conn.execute('''
    CREATE TABLE IF NOT EXISTS Bets (
        BetID INTEGER PRIMARY KEY AUTOINCREMENT,
        AccountID INTEGER,
        EventID INTEGER,
        BetAmount FLOAT,
        BetType TEXT,
        BetStatus TEXT,
        BetPlacedTime DATETIME,
        FOREIGN KEY (AccountID) REFERENCES Accounts (AccountID),
        FOREIGN KEY (EventID) REFERENCES Events (EventID)
    )
''')
print('Table Bets created successfully')

conn.close()
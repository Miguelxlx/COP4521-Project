import sqlite3

def setup():
    conn = sqlite3.connect('bettingData.db')
    print('Opened database successfully')

    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Account(
            AccountID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username VARCHAR(20),
            Status VARCHAR(10),
            Email VARCHAR(30),
            Password VARCHAR(20),
            Balance FLOAT
        );
    ''')
    print('Table Account created successfully')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS 'Transaction'(
            TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
            AccountID INTEGER,
            Date DATETIME,
            Amount FLOAT,
                
            FOREIGN KEY (AccountID) REFERENCES Account (AccountID)
        );
    ''')
    print('Table Transaction created successfully')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS BetsInTransaction(
            TransactionID INTEGER,
            BetID INTEGER,
        
            PRIMARY KEY(TransactionID,BetID),
            FOREIGN KEY (TransactionID) REFERENCES Accounts (TransactionID),
            FOREIGN KEY (BetID) REFERENCES Accounts (BetID)
        );
    ''')
    print('BetsInTransaction created successfully')

    # The Bet Info is described as such
    # The first letter describe the type of bet and what position the user placed
    # O:Over U:Under W:Home team win L:Home team loss


    conn.execute('''
        CREATE TABLE IF NOT EXISTS Bet(
            BetID INTEGER PRIMARY KEY AUTOINCREMENT,
            AccountID INTEGER,
            GameID VARCHAR(16),
            BetType VARCHAR(10),
            Price FLOAT,
            Line INTEGER,
            Status VARCHAR(10),
                 
            FOREIGN KEY (GameID) REFERENCES Game (GameID),
            FOREIGN KEY (AccountID) REFERENCES Account(AccountID)
        );
    ''')
    print('Table Bets created successfully')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS Game(
            GameID INTEGER PRIMARY KEY AUTOINCREMENT,
            Date DATETIME,
            HomeTeam VARCHAR(3),
            AwayTeam VARCHAR(3),
            HomeFinalScore INTEGER,
            AwayFinalScore INTEGER
        );
    ''')
    print('Table Games created successfully')

    # conn.execute('''
    #     CREATE ROLE admin;  
    # ''')

    # conn.execute('''
    #     GRANT UPDATE ON Account to admin;
    # ''')

    # conn.execute('''
    #     GRANT admin to someone;
    # ''')

    conn.close()

if __name__ == "__main__":
    setup()
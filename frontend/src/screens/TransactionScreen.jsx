import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux'; // Import useSelector for accessing Redux store

const TransactionsScreen = () => {
  const [transactions, setTransactions] = useState([]);
  const userInfo = useSelector(state => state.auth.userInfo); // Access user info from Redux store

  useEffect(() => {
    const fetchTransactions = async () => {
      const response = await fetch(`http://127.0.0.1:5000/transactions?user_id=${userInfo.id}`);
      const data = await response.json();
      if (response.ok) {
        setTransactions(data.transactions);
      } else {
        console.error('Failed to fetch transactions');
      }
    };

    if (userInfo && userInfo.id) {  // Ensure userInfo and userInfo.id are not null
      fetchTransactions();
    }
    else
    {
      console.error('User info is missing');
    }
  }, [userInfo]);  // Depend on userInfo for re-fetching when it changes

  return (
    <div className="table-responsive">
      <h2>Transactions</h2>
      <table className="table table-striped table-bordered table-hover">
        <thead className="thead-dark">
        <tr>
            <th>Date</th>
            <th>Amount</th>
            <th>Bets</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction, index) => (
            <tr key={index}>
              <td>{transaction.transactionTime}</td>
              <td>${transaction.amount}</td>
              <td>
                <ul>
                  {transaction.betIds.map((betId, index) => (
                    <li key={index}>{betId}</li>
                  ))}
                </ul>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TransactionsScreen;

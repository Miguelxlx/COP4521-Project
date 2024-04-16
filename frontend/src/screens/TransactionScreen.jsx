import React, { useEffect, useState } from 'react';

const TransactionsScreen = () => {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    const fetchTransactions = async () => {
      const response = await fetch('http://127.0.0.1:5000/transactions');
      const data = await response.json();
      if (response.ok) {
        setTransactions(data.transactions);
      } else {
        console.error('Failed to fetch transactions');
      }
    };

    fetchTransactions();
  }, []);

  return (
    <div className="table-responsive">
      <h2>Transactions</h2>
      <table className="table table-striped table-bordered table-hover">
        <thead className="thead-dark">
        <tr>
            <th>Date</th>
            <th>Amount</th>
            <th>User ID</th>
            <th>Bets</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction, index) => (
            <tr key={index}>
              <td>{transaction.transactionTime}</td>
              <td>${transaction.amount}</td>
              <td>{transaction.userId}</td>
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

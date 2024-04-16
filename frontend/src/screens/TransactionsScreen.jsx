import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';  // Assuming you're using Redux for state management

function TransactionsScreen() {
    const [transactions, setTransactions] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const userInfo = useSelector(state => state.auth.userInfo); // Get user info from the store

    useEffect(() => {
        const fetchTransactions = async () => {
            setIsLoading(true);
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/transactions/${userInfo.id}`); // Adjust URL as needed
                const data = await response.json();
                setTransactions(data.transactions);
            } catch (error) {
                console.error("Failed to fetch transactions:", error);
            }
            setIsLoading(false);
        };

        if (userInfo) {
            fetchTransactions();
        }
    }, [userInfo]);

    return (
        <div>
            <h1>Transaction History</h1>
            {isLoading ? (
                <p>Loading...</p>
            ) : (
                <ul>
                    {transactions.map((transaction, index) => (
                        <li key={index}>
                            <p>Date: {new Date(transaction.date).toLocaleDateString()}</p>
                            <p>Description: {transaction.description}</p>
                            <p>Amount: ${transaction.amount}</p>
                            <p>Status: {transaction.status || 'N/A'}</p>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default TransactionsScreen;

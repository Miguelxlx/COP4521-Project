import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';

const BetsScreen = () => {
  const [bets, setBets] = useState([]);
  const userInfo = useSelector(state => state.auth.userInfo);

  useEffect(() => {
    const fetchBets = async () => {
      const response = await fetch(`http://127.0.0.1:5000/bets?user_id=${userInfo.id}`);
      const data = await response.json();
      if (response.ok) {
        setBets(data.bets);
      } else {
        console.error('Failed to fetch bets');
      }
    };

    if (userInfo && userInfo.id) {
      fetchBets();
    } else {
      console.error('User info is missing');
    }
  }, [userInfo]);

  return (
    <div className="table-responsive">
      <h2>Bets</h2>
      <table className="table table-striped table-bordered table-hover">
        <thead className="thead-dark">
          <tr>
            <th>Home Team</th>
            <th>Visitor Team</th>
            <th>Game Time</th>
            <th>Wager</th>
            <th>Line</th>
            <th>Amount Placed</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {bets.map((bet, index) => (
            <tr key={index}>
              <td>{bet.homeTeam}</td>
              <td>{bet.visitorTeam}</td>
              <td>{new Date(bet.gameTime).toLocaleString()}</td>
              <td>{bet.wager}</td>
              <td>{bet.line.$numberDouble}</td>
              <td>${bet.amountPlaced}</td>
              <td>{bet.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default BetsScreen;

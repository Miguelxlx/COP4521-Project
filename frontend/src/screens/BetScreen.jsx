import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { setCumulativeResults } from '../slices/authSlice';

const BetsScreen = () => {
  const [bets, setBets] = useState([]);
  const userInfo = useSelector(state => state.auth.userInfo);
  const dispatch = useDispatch();

  useEffect(() => {
    const fetchBets = async () => {
      const response = await fetch(`http://127.0.0.1:5000/bets?user_id=${userInfo.id}`);
      const data = await response.json();
      if (response.ok) {
        setBets(data.bets);
        calculateCumulativeResults(data.bets);
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

  const calculateCumulativeResults = (bets) => {
    let results = [];
    let total = 0;

    bets.forEach(bet => {
        console.log('Bet data:', bet);

        const amountPlaced = parseFloat(bet.amountPlaced);
        const profit = parseFloat(bet.profit);

        if (bet.status === 'W') {
            total += profit;
        } else if (bet.status === 'L') {
            total -= amountPlaced;
        }

        const formattedGameTime = new Date(bet.gameTime).toLocaleDateString('en-US');
        const existingResult = results.find(r => r.gameTime === formattedGameTime);

        if (existingResult) {
            existingResult.total = total;
        } else {
            results.push({
                gameTime: formattedGameTime,
                total: total
            });
        }
    });

    console.log('Cumulative results:', results); // Log to verify the results
    dispatch(setCumulativeResults(results));
};

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
            <th>Profit</th>
          </tr>
        </thead>
        <tbody>
          {bets.map((bet, index) => (
            <tr key={index}>
              <td>{bet.homeTeam}</td>
              <td>{bet.visitorTeam}</td>
              <td>{new Date(bet.gameTime).toLocaleString()}</td>
              <td>{bet.wager}</td>
              <td>{bet.line}</td>
              <td>${bet.amountPlaced}</td>
              <td>{bet.status}</td>
              <td>${bet.profit}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default BetsScreen;

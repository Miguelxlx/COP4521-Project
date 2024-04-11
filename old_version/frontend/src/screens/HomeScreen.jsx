import React, { useState, useEffect } from "react";
import { useSelector } from 'react-redux';

function App() {
  const [odds, setOdds] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [betSlip, setBetSlip] = useState([]);
  // Updating to include bet amount, type, and team selection in one state object
  const [betDetails, setBetDetails] = useState({});

  const userInfo = useSelector((state) => state.auth.userInfo); // Access login status

  useEffect(() => {
    fetchOdds();
  }, []);

  const fetchOdds = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/odds");
      const data = await response.json();
      setOdds(data.odds);
    } catch (error) {
      console.error("Error fetching odds:", error);
    }
    finally{
      setIsLoading(false);
    }
  };

  const handleBetDetailChange = (index, detail, value) => {
    setBetDetails(prev => ({
      ...prev,
      [index]: { ...prev[index], [detail]: value }
    }));
  };

  const addToBetSlip = (odd, index) => {
    const details = betDetails[index] || {};
    const bet = { ...odd, ...details };
    setBetSlip(current => [...current, bet]);
  };

  const handleSubmitBetSlip = async () => {

    if (!userInfo) {
      alert("You must be logged in to place bets.");
      // Alternatively, redirect to login page:
      // navigate('/login');
      return;
    }
    const totalBetAmount = betSlip.reduce((acc, bet) => acc + parseFloat(bet.amount || 0), 0);
    if (userInfo.balance < totalBetAmount) {
        alert("Insufficient funds.");
        return;
    }
    console.log("Submitting Bet Slip:", betSlip);
    try {
      // Map through each bet in the slip and send them individually
      const promises = betSlip.map(async (bet) => {
        const response = await fetch('http://127.0.0.1:5000/bet_logic', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            // Include authorization header if needed
            // 'Authorization': `Bearer ${yourAuthToken}`
          },
          body: JSON.stringify(bet), // Send each bet details
        });
  
        if (!response.ok) {
          throw new Error('Failed to submit a bet');
        }
  
        return response.json();
      });
  
      // Wait for all bets to be submitted
      const results = await Promise.all(promises);
      console.log("All bets submitted successfully", results);
      // Handle success, such as notifying the user or clearing the bet slip
    } catch (error) {
      console.error("Error submitting bets:", error.message); // Or display an error to the user
      // Handle error, such as notifying the user about the failure
    }
  };

  const totalBetAmount = betSlip.reduce((acc, bet) => acc + (parseFloat(bet.amount) || 0), 0);

  return (
    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
      <div style={{ flex: 3, padding: '20px' }}>
        {isLoading ? (
          <div>Loading odds...</div>
        ) : (
          odds.map((odd, index) => (
            <div key={index} style={{ marginBottom: '20px' }}>
              <h3>{odd.home_team} vs. {odd.visitor_team}</h3>
              <h4>Over: {odd.over_price} Under: {odd.under_price}</h4>
              <h5>Line: {odd.line}</h5>
              <select
                value={betDetails[index]?.type || ''}
                onChange={(e) => handleBetDetailChange(index, 'type', e.target.value)}
                style={{ marginRight: '10px' }}
              >
                <option value="">Select Bet Type</option>
                <option value="H2H">Head-to-Head</option>
                <option value="O/U">Over/Under</option>
              </select>
              {betDetails[index]?.type === 'H2H' && (
                <select
                  value={betDetails[index]?.team || ''}
                  onChange={(e) => handleBetDetailChange(index, 'team', e.target.value)}
                  style={{ marginRight: '10px' }}
                >
                  <option value="">Select Team</option>
                  <option value={odd.home_team}>{odd.home_team}</option>
                  <option value={odd.visitor_team}>{odd.visitor_team}</option>
                </select>
              )}
              <input
                type="number"
                placeholder="Bet Amount ($)"
                value={betDetails[index]?.amount || ''}
                onChange={(e) => handleBetDetailChange(index, 'amount', e.target.value)}
                style={{ marginRight: '10px' }}
              />
              <button onClick={() => addToBetSlip(odd, index)}>Add to Bet Slip</button>
            </div>
          ))
        )}
      </div>
      <div style={{ flex: 1, padding: '20px' }}>
        <h2>Bet Slip</h2>
        {betSlip.map((bet, index) => (
          <div key={index} style={{ marginBottom: '10px' }}>
            <p>{bet.home_team} vs. {bet.visitor_team}</p>
            <p>Bet Amount: ${bet.amount}</p>
          </div>
        ))}
        <div>Total Bet Amount: ${totalBetAmount.toFixed(2)}</div>
        <button onClick={handleSubmitBetSlip}>Submit Bet Slip</button>
      </div>
    </div>
  );
}

export default App;
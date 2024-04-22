import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { setCredentials } from '../slices/authSlice';

function App() {
  const [odds, setOdds] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [betSlip, setBetSlip] = useState([]);
  // Updating to include bet amount, type, and team selection in one state object
  const [betDetails, setBetDetails] = useState({});
  const [message, setMessage] = useState(null);
  const dispatch = useDispatch();

  const userInfo = useSelector((state) => state.auth.userInfo); // Access login status

  useEffect(() => {
    fetchOdds();
  }, []);

  const fetchOdds = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/odds");
      const data = await response.json();
      console.log(data.remaining_requests); 
      setOdds(data.odds)
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
    //check if user is loged in navigate to login page
    if (!userInfo) {
      alert("You must be logged in to place bets.");
      return;
    }
      

    if (!betDetails[index]?.amount || !betDetails[index]?.type || !betDetails[index]?.team) {
      setMessage("Please complete all bet details.");
      return;
    }
    if (betDetails[index]?.amount < 1) {
      setMessage("Minimum bet amount is $1.");
      return;
    }
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
    if (betSlip.length === 0) {
      setMessage("Please add bets to your bet slip.");
      return;
    }
    const totalBetAmount = betSlip.reduce((acc, bet) => acc + parseFloat(bet.amount || 0), 0);
    console.log(userInfo.id)

    const transactionData = {
      id: userInfo.id,
      total: totalBetAmount,
      betSlip: betSlip
    };

    const response = await fetch('http://127.0.0.1:5000/submit_transaction', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(transactionData), // Send each bet details
    });

    const data = await response.json()
    if(!response.ok){
      // setMessage('Insufficient Balance');
      throw new Error('Failed to submit bet slip');
      
    }
    else{
      dispatch(setCredentials(data.user));
      console.log(data.user)
      console.log("All bets submitted successfully")
      setBetSlip([]); // Clear the bet slip
      setMessage("Bet submitted successfully! Your balance has been updated.");
    }
  };

  const handleRemoveBet = (index) => {
    // Create a new array excluding the bet at the provided index
    const newBetSlip = betSlip.filter((_, i) => i !== index);
    setBetSlip(newBetSlip);
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
              <h3>{odd.home_team} <img src={odd.home_img}></img>({odd.h2h_home_price}) vs. {odd.visitor_team} ({odd.h2h_visitor_price}) <img src={odd.visitor_img}></img> </h3>
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
                  <option value='home_win'>{odd.home_team}</option>
                  <option value='visitor_win'>{odd.visitor_team}</option>
                </select>
              )}
              {betDetails[index]?.type === 'O/U' && (
                <select
                  value={betDetails[index]?.team || ''}
                  onChange={(e) => handleBetDetailChange(index, 'team', e.target.value)}
                  style={{ marginRight: '10px' }}
                >
                  <option value="">Select</option>
                  <option value='Over'>Over</option>
                  <option value='Under'>Under</option>
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
        {message && <div className="alert alert-danger">{message}</div>}
        {betSlip.map((bet, index) => (
          <div key={index} style={{ marginBottom: '10px' }}>
            <p>{bet.home_team} vs. {bet.visitor_team}</p>
            <p>Bet Amount: ${bet.amount}</p>
            <button onClick={() => handleRemoveBet(index)}>Remove Bet</button>
          </div>
        ))}
        <div>Total Bet Amount: ${totalBetAmount.toFixed(2)}</div>
        <button onClick={handleSubmitBetSlip}>Submit Bet Slip</button>
      </div>
    </div>
  );
}

export default App;
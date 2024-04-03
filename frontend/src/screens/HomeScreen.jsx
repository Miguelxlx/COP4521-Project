import React, { useState, useEffect } from 'react';

const HomeScreen = () => {
  const [games, setGames] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [betSlip, setBetSlip] = useState([]);
  // Updating to include bet amount, type, and team selection in one state object
  const [betDetails, setBetDetails] = useState({});

  useEffect(() => {
    const API_KEY = '2e45b517a7f1b28c45fac18d4eefd331'; // Reminder: Fetch this securely from your server in production
    const SPORT = 'basketball_nba';
    const REGIONS = 'us';
    const MARKETS = 'totals,h2h';
    const ODDS_FORMAT = 'decimal';
    const DATE_FORMAT = 'iso';
    const BOOKMAKERS = 'fanduel';

    const getGames = async () => {
      setIsLoading(true);
      const queryParams = new URLSearchParams({
        api_key: API_KEY,
        regions: REGIONS,
        markets: MARKETS,
        oddsFormat: ODDS_FORMAT,
        dateFormat: DATE_FORMAT,
        bookmakers: BOOKMAKERS
      }).toString();

      const url = `https://api.the-odds-api.com/v4/sports/${SPORT}/odds?${queryParams}`;

      try {
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch odds: status ${response.status}`);
        }

        const data = await response.json();
        setGames(data);
      } catch (error) {
        console.error(error.message);
      } finally {
        setIsLoading(false);
      }
    };

    getGames();
  }, []);

  const handleBetDetailChange = (index, detail, value) => {
    setBetDetails(prev => ({
      ...prev,
      [index]: { ...prev[index], [detail]: value }
    }));
  };

  const addToBetSlip = (game, index) => {
    const details = betDetails[index] || {};
    const bet = { ...game, ...details };
    setBetSlip(current => [...current, bet]);
  };

  const handleSubmitBetSlip = () => {
    console.log("Submitting Bet Slip:", betSlip);
    // Send to backend
  };

  const totalBetAmount = betSlip.reduce((acc, bet) => acc + (parseFloat(bet.amount) || 0), 0);

  return (
    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
      <div style={{ flex: 3, padding: '20px' }}>
        {isLoading ? (
          <div>Loading games...</div>
        ) : (
          games.map((game, index) => (
            <div key={index} style={{ marginBottom: '20px' }}>
              <h3>{game.home_team} vs. {game.away_team}</h3>
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
                  <option value={game.home_team}>{game.home_team}</option>
                  <option value={game.away_team}>{game.away_team}</option>
                </select>
              )}
              <input
                type="number"
                placeholder="Bet Amount ($)"
                value={betDetails[index]?.amount || ''}
                onChange={(e) => handleBetDetailChange(index, 'amount', e.target.value)}
                style={{ marginRight: '10px' }}
              />
              <button onClick={() => addToBetSlip(game, index)}>Add to Bet Slip</button>
            </div>
          ))
        )}
      </div>
      <div style={{ flex: 1, padding: '20px' }}>
        <h2>Bet Slip</h2>
        {betSlip.map((bet, index) => (
          <div key={index} style={{ marginBottom: '10px' }}>
            <p>{bet.home_team} vs. {bet.away_team}</p>
            <p>Bet Amount: ${bet.amount}</p>
          </div>
        ))}
        <div>Total Bet Amount: ${totalBetAmount.toFixed(2)}</div>
        <button onClick={handleSubmitBetSlip}>Submit Bet Slip</button>
      </div>
    </div>
  );
};

export default HomeScreen;
import React, { useState, useEffect } from 'react';

const HomeScreen = () => {
  const [games, setGames] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [betSlip, setBetSlip] = useState([]); // State to keep track of bets added to the slip

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

  // Function to add a bet to the bet slip
  const addToBetSlip = (game, betType) => {
    const bet = { ...game, betType };
    setBetSlip(current => [...current, bet]);
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
      <div style={{ flex: 3, padding: '20px' }}> {/* Games List Container */}
        {isLoading ? (
          <div>Loading games...</div>
        ) : (
          games.map((game, index) => (
            <div key={index} style={{ marginBottom: '20px' }}>
              <h3>{game.home_team} vs. {game.away_team}</h3>
              {/* Game details and odds */}
              <p>Line: {game.bookmakers[0]?.markets.find(market => market.key === "totals")?.outcomes[0]?.point}</p>
              <p>Over Price: {game.bookmakers[0]?.markets.find(market => market.key === "totals")?.outcomes[0]?.price}</p>
              <p>Under Price: {game.bookmakers[0]?.markets.find(market => market.key === "totals")?.outcomes[1]?.price}</p>
              {game.h2h && (
                <div>
                  <h4>Head to Head:</h4>
                  {game.h2h.map((odd, idx) => (
                    <p key={idx}>{odd.team_name}: {odd.price}</p>
                  ))}
                </div>
              )}
              <button onClick={() => addToBetSlip(game, 'H2H')}>Add to Bet Slip</button>
            </div>
          ))
        )}
      </div>
      <div style={{ flex: 1, padding: '20px' }}> {/* Bet Slip Container */}
        <h2>Bet Slip</h2>
        {betSlip.map((bet, index) => (
          <div key={index} style={{ marginBottom: '10px' }}>
            <p>{bet.home_team} vs. {bet.away_team}</p>
            <p>Bet: {bet.betType}</p>
            {/* Display more bet details here */}
          </div>
        ))}
      </div>
    </div>
  );
};

export default HomeScreen;
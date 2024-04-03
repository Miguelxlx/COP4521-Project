import React, { useState, useEffect } from 'react';

const HomeScreen = () => {
  const [games, setGames] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

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
        setGames(data); // Adjust this if you need to transform the data structure
      } catch (error) {
        console.error(error.message);
      } finally {
        setIsLoading(false);
      }
    };

    getGames();
  }, []);

  return (
    <div>
      {isLoading ? (
        <div>Loading games...</div>
      ) : (
        <div>
          {games.map((game, index) => (
  <div key={index} style={{ marginBottom: '20px' }}>
    <h3>{game.home_team} vs. {game.away_team}</h3>
    {/* Adjusted property paths */}
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
  </div>
))}
        </div>
      )}
    </div>
  );
};

export default HomeScreen;
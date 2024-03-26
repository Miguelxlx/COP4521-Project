import React from 'react';

const HomeScreen = () => {
  return (
    <div className="container">
      <div className="gamesContainer">
        {/* This will eventually display NBA games */}
        <h2>NBA Games</h2>
      </div>
      <div className="betSlipContainer">
        <h2>Bet Slip</h2>
        {/* This will display the bets the user picked */}
        
        {/* Place Bet button */}
        <button className="placeBetButton">Place Bet</button>
      </div>
    </div>
  );
};

export default HomeScreen;
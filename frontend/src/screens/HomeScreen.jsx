import React, { useState } from 'react';

function HomePage() {
    const [games, setGames] = useState([]);
    const [betSlip, setBetSlip] = useState([]);

    // Function to add a game to the bet slip
    const addToBetSlip = (game) => {
        setBetSlip([...betSlip, game]);
    };

    // Function to remove a game from the bet slip
    const removeFromBetSlip = (index) => {
        const updatedBetSlip = [...betSlip];
        updatedBetSlip.splice(index, 1);
        setBetSlip(updatedBetSlip);
    };

    // Sample data for games
    const sampleGames = [
        { id: 1, name: "Football", startTime: "10:00 AM" },
        { id: 2, name: "Basketball", startTime: "11:00 AM" },
        { id: 3, name: "Tennis", startTime: "12:00 PM" }
    ];

    return (
        <div>
            <header>
                <nav>
                    <ul>
                        <li><a href="#">Bet Slip ({betSlip.length})</a></li>
                    </ul>
                </nav>
            </header>

            {/* Main content */}
            <main>
                {/* Display Current/Upcoming Games */}
                <div id="games">
                    <h2>Current/Upcoming Games</h2>
                    <ul>
                        {sampleGames.map((game, index) => (
                            <li key={index}>
                                {game.name} - {game.startTime}
                                <button onClick={() => addToBetSlip(game)}>Add to Bet Slip</button>
                            </li>
                        ))}
                    </ul>
                </div>

                {/* Display Bet Slip */}
                <div id="bet-slip">
                    <h2>Bet Slip</h2>
                    <ul>
                        {betSlip.map((game, index) => (
                            <li key={index}>
                                {game.name} - {game.startTime}
                                <button onClick={() => removeFromBetSlip(index)}>Remove from Bet Slip</button>
                            </li>
                        ))}
                    </ul>
                </div>
            </main>
        </div>
    );
}

export default HomePage;
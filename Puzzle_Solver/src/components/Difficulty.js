import React, { useState } from 'react';
import "../App.css";


const Difficulty = ({ onSelectDifficulty }) => {
    const [selectedDifficulty, setSelectedDifficulty] = useState("facile");

    const handleDifficultyChange = (difficulty) => {
        setSelectedDifficulty(difficulty); 
        onSelectDifficulty(difficulty); 
    };

    return (
        <div>
            <div
                className={selectedDifficulty === "facile" ? "selectedButton" : "unselectedButton"}
                onClick={() => handleDifficultyChange("facile")}
            >
                Facile (3*3)
            </div>

            <div
                className={selectedDifficulty === "medium" ? "selectedButton" : "unselectedButton"}
                onClick={() => handleDifficultyChange("medium")}
            >
                Medium (4*4)
            </div>

            <div
                className={selectedDifficulty === "difficile" ? "selectedButton" : "unselectedButton"}
                onClick={() => handleDifficultyChange("difficile")}
            >
                Difficile(6*6)
            </div>
        </div>
    );
};

export default Difficulty;

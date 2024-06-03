import "../App.css";
import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Link, useNavigate, useParams } from "react-router-dom";
import ImageGallery from './ImageGallery.js';
import Difficulty from './Difficulty.js';
import Logo from './Logo.js';

function Play() {
  const [, setnavSize] = useState("10rem");
  const [navColor, setnavColor] = useState("transparent");

  const listenScrollEvent = () => {
    window.scrollY > 10 ? setnavColor("#252734") : setnavColor("transparent");
    window.scrollY > 10 ? setnavSize("5rem") : setnavSize("10rem");
  };

  useEffect(() => {
    window.addEventListener("scroll", listenScrollEvent);
    window.scrollTo(0, 0);
    return () => {
      window.removeEventListener("scroll", listenScrollEvent);
    };
  }, []);

  const [selectedImageId, setSelectedImageId] = useState(null);

  const handleSelectImage = (imageId) => {
    setSelectedImageId(imageId);
  };

  const [selectedDifficulty, setSelectedDifficulty] = useState("facile");

  const handleDifficultySelect = (difficulty) => {
    console.log("Nouvelle difficulté sélectionnée :", difficulty);
    setSelectedDifficulty(difficulty);
  };

  const navigate = useNavigate();

  const handlePlayButtonClick = () => {
    if (selectedImageId !== null) {
      let difficultyRoute = '';
      switch (selectedDifficulty) {
        case 'facile':
          difficultyRoute = 'Facile';
          navigate(`/${difficultyRoute}/${selectedImageId}`);
          break;
        case 'medium':
          difficultyRoute = 'Medium';
          navigate(`/${difficultyRoute}/${selectedImageId}`);
          break;
        case 'difficile':
          difficultyRoute = 'Difficile';
          navigate(`/${difficultyRoute}/${selectedImageId}`);
          break;
        default:
          difficultyRoute = 'Facile';
          navigate(`/${difficultyRoute}/${selectedImageId}`);
          break;
      }
    }
  };

  return (
    <div className="App">
      <nav
        class="navbar"
        id="navbarJs"
        style={{
          backgroundColor: navColor,
          transition: "all ",
        }}
      >
        <div className="logo"><Logo />
          <p>PUZZLE SOLVER</p></div>
        <ul class="nav-links">
          <div class="menu">
            <li>
              <Link to="../">Accueil</Link>
            </li>
            <li>
              <a href="#Accueil">Choix Puzzle</a>
            </li>
            <li>
              <a href="#footer">Contact</a>
            </li>
          </div>
        </ul>
      </nav>

      <div className="eclipse1"></div>
      <div id="Accueil">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <h3 style={{ marginRight: '10px' }}>Choisissez le puzzle que vous voulez :</h3>
          <div className="form-group">
            <button onClick={handlePlayButtonClick}>Play</button>
          </div>
        </div>

        <div className="form">
          <br /><br />
          <Difficulty onSelectDifficulty={handleDifficultySelect} />
        </div>
        <div className="form">
          <br /><br />
          <ImageGallery onSelectImage={handleSelectImage} />
        </div>
      </div>

      <footer id="footer">
        <div class="row primary">
          <div class="column about">
            <p>
              PUZZLE SOLVER doit permettre à un utilisateur de
              Jouer/Importer une image pour la crétion ou bien la réconstitution d'un puzzle
            </p>
          </div>

          <div class="column links">
            <h2>Naviguer</h2>
            <ul>
              <li>
                <a href="#Accueil">Choix Puzzle</a>
              </li>
            </ul>
          </div>
          <div class="column subscribe">
            <h2>Contact Us</h2>
            <ul>
              <a href="mailto:puzzle-solver@gmail.com">puzzle-solver@gmail.com</a>
            </ul>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default Play;

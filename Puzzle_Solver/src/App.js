import React, { useState, useEffect } from "react";
import Logo from './components/Logo.js';
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import Play from './components/Play';
import NiveauFacile from './components/NiveauFacile';
import NiveauMedium from './components/NiveauMedium';
import NiveauDifficile from './components/NiveauDifficile';
import PlayImgImp from './/components/PlayImgImp';

function App() {
  const [, setnavSize] = useState("10rem");
  const [navColor, setnavColor] = useState("transparent");
  const [imageUrl, setImageUrl] = useState(null);
  const [showMetadata, setShowMetadata] = useState(false);
  const listenScrollEvent = () => {
    window.scrollY > 10 ? setnavColor("#252734") : setnavColor("transparent");
    window.scrollY > 10 ? setnavSize("5rem") : setnavSize("10rem");
  };

  useEffect(() => {
    window.addEventListener("scroll", listenScrollEvent);
    return () => {
      window.removeEventListener("scroll", listenScrollEvent);
    };
  }, []);

  const handlePlayButtonClick = () => {
    console.log("Bouton Jouer cliqué");
    navigate("/play");
  };

  const handleImportImageClick = () => {
    console.log("Bouton 'Importer Image' cliqué");
    const fileInput = document.getElementById("imageInput");
    fileInput.click();
  };

  const handleFileInputChange = (event) => {
    const file = event.target.files[0];
    uploadImage(file);
  };

  const uploadImage = (file) => {
    const formData = new FormData();
    formData.append('image', file);

    fetch('http://localhost:5005/api/upload-image', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        setImageUrl(data.imageUrl);
        setShowMetadata(true);
        console.log(imageUrl);
      })
      .catch(error => {
        console.error('Error uploading image:', error);
      });
  };

  const handleStartPuzzle = () => {
    navigate(`/playimport?imageUrl=${imageUrl}`);
  };

  const navigate = useNavigate();

  return (
    <div className="App">
      <nav
        className="navbar"
        style={{
          backgroundColor: navColor,
          transition: "all ",
        }}
      >
        <div className="logo"><Logo />
          <p>PUZZLE SOLVER</p></div>
        <ul className="nav-links">
          <div className="menu">
            <li>
              <a href='#Accueil'>Accueil</a>
            </li>
            <li>
              <a href="#conteneur">Métadonnée</a>
            </li>
            <li>
              <a href="#footer">Contact</a>
            </li>
          </div>
        </ul>
      </nav>

      <div className="eclipse" id="Accueil"></div>
      <div className="conteneur">
        <div className="bienvenue">
          <h1>Bienvenue sur PUZZLE SOLVER</h1>
          <div className="parag">
            Amusez vous bien
            <br />
            Tu peux choisir entre Jouer ou bien Charger ta propre image
          </div>
        </div>
        <div className="form2">
          <div className="form-group">
            <button onClick={handlePlayButtonClick}>Jouer</button>
            <button onClick={handleImportImageClick}>Importer Image</button>
            <input
              id="imageInput"
              type="file"
              accept="image/*"
              style={{ display: "none" }}
              onChange={handleFileInputChange}
            />
          </div>
        </div>
      </div>

      {showMetadata && ( 
        <div id="conteneur">
          <button className="text" >
            {" "}
            Les Métadonnées
          </button>
        </div>
      )}
      {showMetadata && ( 
        <div className="form4">
          {imageUrl && <img src={imageUrl} alt="Uploaded" style={{ width: "300px", height: "300px" }} />}
        </div>
      )}
      {showMetadata && (
        <div className="form-group" style={{ marginLeft: '40%' }}>
          <button onClick={handleStartPuzzle}>Play</button>
        </div>
      )}

      <footer id="footer">
        <div className="row primary">
          <div className="column about">
            <p>
              PUZZLE SOLVER doit permettre à un utilisateur de
              Jouer/Importer une image pour la création ou bien la réconstitution d'un puzzle
            </p>
          </div>

          <div className="column links">
            <h2>Naviguer</h2>
            <ul>
              <li>
                <a href='#Accueil'>Accueil</a>
              </li>
              <li>
                <a href="#conteneur">Métadonnées</a>
              </li>
            </ul>
          </div>
          <div className="column subscribe">
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

function AppWithRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/playimport" element={<PlayImgImp />} />
        <Route path="/play" element={<Play />} />
        <Route path="/facile/:imageId" element={<NiveauFacile />} />
        <Route path="/medium/:imageId" element={<NiveauMedium />} />
        <Route path="/difficile/:imageId" element={<NiveauDifficile />} />
      </Routes>
    </Router>
  );
}

export default AppWithRouter;

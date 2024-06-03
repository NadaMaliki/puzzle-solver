import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Link, useParams } from "react-router-dom";
import PiecesGallery from './PiecesGallery';
import Logo from './Logo.js';

function NiveauFacile() {
    const [, setnavSize] = useState("10rem");
    const [navColor, setnavColor] = useState("transparent");    const { imageId } = useParams();
    const [hint, setHint] = useState(null);
    const [selectedPieceId, setSelectedPieceId] = useState(null);
    window.scrollTo(0, 0);

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

    const handleHintButtonClick = () => {
        if (selectedPieceId === null) {
            alert('Veuillez sélectionner une pièce du puzzle.');
            return;
        }

        console.log("Bouton Hint cliqué");

        fetch(`http://localhost:5008/api/getHint/${selectedPieceId}`)
            .then(response => response.json())
            .then(data => {
                if (data.correct_position !== undefined) {
                    setHint(data.correct_position);
                    alert(`La position correcte de la pièce est : ${data.correct_position}`);
                } else {
                    alert('Aucun indice trouvé');
                }
            })
            .catch(error => console.error('Erreur lors de la récupération de l\'indice : ', error));
    };

    return (
        <div className="App">
            <nav
                className="navbar"
                id="navbarJs"
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
                            <Link to="../">Accueil</Link>
                        </li>
                        <li>
                            <Link to="../Play">Choix Puzzle</Link>
                        </li>
                        <li>
                            <a href="#Accueil">Jouer au Puzzle</a>
                        </li>
                        <li>
                            <a href="#footer">Contact</a>
                        </li>
                    </div>
                </ul>
            </nav>

            <div className="eclipse1"></div>
            <div id="accueil">
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <h3 style={{ marginRight: '10px' }}>Résoudre votre Puzzle:</h3>
                    <div className="form-group">
                        <button onClick={handleHintButtonClick}>Hint</button>
                    </div>
                </div>
                <PiecesGallery
                    imageId={imageId}
                    hint={hint} 
                    setSelectedPieceId={setSelectedPieceId}
                    selectedPieceId={selectedPieceId}
                />
            </div>

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
                                <a href="#Accueil">Choix Puzzle</a>
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

export default NiveauFacile;

import React, { useState } from "react";
import { Link } from "react-router-dom";
import PiecesGallery from "./PiecesGalleryImp";
import Logo from "./Logo";
import Modal from 'react-modal';

Modal.setAppElement('#root');

function PlayImgImp() {
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [reconstructedImage, setReconstructedImage] = useState(null);

    const openModal = () => {
        setModalIsOpen(true);
        fetch('http://localhost:5007/api/reconstruct-image', {
            method: 'POST',
        })
            .then(response => response.json())
            .then(data => {
                setReconstructedImage(data.reconstructedImage);
                console.log(data.reconstructedImage, data);
            })
            .catch(error => console.error('Erreur lors de la requête:', error));
    };

    const closeModal = () => {
        setModalIsOpen(false);
    };


    return (
        <div className="App">
            <nav className="navbar" style={{ backgroundColor: "transparent", transition: "all" }}>
                <div className="logo">
                    <Logo />
                    <p>PUZZLE SOLVER</p>
                </div>
                <ul className="nav-links">
                    <div className="menu">
                        <li>
                            <Link to="../">Accueil</Link>
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
                <div style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
                    <h3 style={{ marginRight: "10px" }}>Résoudre votre Puzzle:</h3>
                    <div className="form-group">
                        <button onClick={openModal}>Reconstruire l'image</button>
                    </div>
                </div>
                <PiecesGallery />
            </div>

            <div className="ReactModal__Content">
                <Modal
                    isOpen={modalIsOpen}
                    onRequestClose={closeModal}
                    contentLabel="Reconstruire l'image"
                    style={{
                        overlay: {
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            backgroundColor: 'rgba(0, 0, 0, 0.5)'
                        },
                        content: {
                            position: 'relative',
                            border: 'none',
                            background: '#857199',
                            padding: '10px',
                            borderRadius: '16px',
                            maxWidth: '90%',
                            maxHeight: '90%',
                            overflow: 'auto',
                        }
                    }}
                >
                    <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                        <button style={{ background: 'transparent', border: 'none', cursor: 'pointer' }} onClick={closeModal}>
                            <i className="material-icons">close</i>
                        </button>
                    </div>
                    <h2>Image reconstituée</h2>
                    {reconstructedImage && <img src={reconstructedImage} alt="Reconstructed" />}
                </Modal>
            </div>

            <footer id="footer">
                <div className="row primary">
                    <div className="column about">
                        <p>
                            PUZZLE SOLVER doit permettre à un utilisateur de Jouer/Importer une image pour la création ou bien la
                            réconstitution d'un puzzle
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

export default PlayImgImp;

import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSync } from '@fortawesome/free-solid-svg-icons';

function PiecesGallery({ imageId }) {
    const [pieces, setPieces] = useState([]);
    const [initialPieces, setInitialPieces] = useState([]);
    const [grid, setGrid] = useState(Array.from({ length: 16 }, () => null));
    const [draggedPieceIndex, setDraggedPieceIndex] = useState(null);
    const [, setDraggedCellIndex] = useState(null);
    const [, setOriginalCellIndex] = useState(null);

    useEffect(() => {
        fetch(`http://localhost:5003/api/relatedData16/${imageId}`)
            .then(response => response.json())
            .then(data => {
                setPieces(data);
                setInitialPieces(data);
            })
            .catch(error => console.error('Erreur lors de la récupération des pièces : ', error));
    }, [imageId]);

    const dragStart = (e, pieceIndex) => {
        setDraggedPieceIndex(pieceIndex);
    };

    const dragDrop = (e, cellIndex) => {
        e.preventDefault();
        const draggedPiece = pieces[draggedPieceIndex];

        if (grid.includes(draggedPiece)) {

            return;
        }

        const newGrid = [...grid];

        if (grid[cellIndex] === null) {
            newGrid[cellIndex] = pieces[draggedPieceIndex];
            setGrid(newGrid);

            const newPieces = pieces.filter((_, i) => i !== draggedPieceIndex);
            setPieces(newPieces);
        } else {
            const temp = newGrid[cellIndex];
            newGrid[cellIndex] = pieces[draggedPieceIndex];
            setGrid(newGrid);

            const newPieces = [...pieces.filter((_, i) => i !== draggedPieceIndex), temp];
            setPieces(newPieces);
        }

        setGrid(newGrid);
        setOriginalCellIndex(null);
        setDraggedPieceIndex(null);
    };


    const dragEnter = (e, cellIndex) => {
        setDraggedCellIndex(cellIndex);
    };

    const removePieceFromGrid = (index) => {
        const newGrid = [...grid];
        newGrid[index] = null;
        setGrid(newGrid);

        const removedPiece = grid[index];
        if (removedPiece) {
            setPieces([...pieces, removedPiece]);
        }
    };

    const clearGrid = () => {
        setGrid(Array.from({ length: 16 }, () => null));
        setPieces(initialPieces);
    };

    return (
        <div>
            <button onClick={clearGrid} className="clear-button">
                <FontAwesomeIcon icon={faSync} /> Reset
            </button>
            <div className="piece-gallery">
                <div className="form3">
                    <div className="grid16">
                        {grid.map((piece, index) => (
                            <div
                                key={index}
                                className="cell16"
                                onDragOver={(e) => e.preventDefault()}
                                onDrop={(e) => dragDrop(e, index)}
                                onDragEnter={(e) => dragEnter(e, index)}
                                onDoubleClick={() => removePieceFromGrid(index)}
                            >
                                {piece && <img src={piece} alt={`Piece ${index}`} className="piece-in-grid" />}
                            </div>
                        ))}
                    </div>
                </div>
                <div className="pieces16">
                    {pieces.map((piece, index) => (
                        <img
                            key={index}
                            src={piece}
                            alt={`Piece ${index}`}
                            className="piece"
                            draggable
                            onDragStart={(e) => dragStart(e, index)}
                        />
                    ))}
                </div>
            </div>
        </div>
    );

}

export default PiecesGallery;
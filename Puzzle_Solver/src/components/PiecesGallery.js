import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSync } from '@fortawesome/free-solid-svg-icons';

function PiecesGallery({ imageId, hint, setSelectedPieceId, selectedPieceId }) {
    const [pieces, setPieces] = useState([]);
    const [indices, setIndices] = useState([]);
    const [initialPieces, setInitialPieces] = useState([]);
    const [initialIndices, setInitialIndices] = useState([]);
    const [grid, setGrid] = useState(Array.from({ length: 9 }, () => null));
    const [draggedPieceIndex, setDraggedPieceIndex] = useState(null);
    const [, setDraggedCellIndex] = useState(null);
    const [, setOriginalCellIndex] = useState(null);

    useEffect(() => {
        fetch(`http://localhost:5002/api/relatedData/${imageId}`)
            .then(response => response.json())
            .then(data => {
                const piecesUrls = data.map(item => item.url);
                const pieceIds = data.map(item => item.id);
                setPieces(piecesUrls);
                setIndices(pieceIds);
                setInitialPieces(piecesUrls);
                setInitialIndices(pieceIds);
                console.log(pieceIds);
            })
            .catch(error => console.error('Erreur lors de la récupération des pièces : ', error));
    }, [imageId]);

    const handlePieceClick = (pieceId) => {
        console.log("Piece clicked:", pieceId);
        setSelectedPieceId(pieceId);
    };

    const dragStart = (e, pieceIndex) => {
        setDraggedPieceIndex(pieceIndex);
    };

    const dragDrop = (e, cellIndex) => {
        e.preventDefault();
        const draggedPiece = pieces[draggedPieceIndex];
        const draggedPieceId = indices[draggedPieceIndex];

        if (grid.includes(draggedPiece)) {
            return;
        }

        const newGrid = [...grid];

        if (grid[cellIndex] === null) {
            newGrid[cellIndex] = draggedPiece;
            setGrid(newGrid);

            const newPieces = pieces.filter((_, i) => i !== draggedPieceIndex);
            const newIndices = indices.filter((_, i) => i !== draggedPieceIndex);
            setPieces(newPieces);
            setIndices(newIndices);
        } else {
            const temp = newGrid[cellIndex];
            newGrid[cellIndex] = draggedPiece;
            setGrid(newGrid);

            const newPieces = [...pieces.filter((_, i) => i !== draggedPieceIndex), temp];
            const newIndices = [...indices.filter((_, i) => i !== draggedPieceIndex), draggedPieceId];
            setPieces(newPieces);
            setIndices(newIndices);
        }

        setOriginalCellIndex(null);
        setDraggedPieceIndex(null);
    };

    const dragEnter = (e, cellIndex) => {
        setDraggedCellIndex(cellIndex);
    };

    const removePieceFromGrid = (index) => {
        const newGrid = [...grid];
        const removedPiece = newGrid[index];
        newGrid[index] = null;
        setGrid(newGrid);

        if (removedPiece) {
            setPieces([...pieces, removedPiece]);
            setIndices([...indices, indices[index]]);
        }
    };

    const clearGrid = () => {
        setGrid(Array.from({ length: 9 }, () => null));
        setPieces(initialPieces);
        setIndices(initialIndices);
    };

    return (
        <div>
            <button onClick={clearGrid} className="clear-button">
                <FontAwesomeIcon icon={faSync} /> Reset
            </button>
            <div className="piece-gallery">
                <div className="form3">
                    <div className="grid9">
                        {grid.map((piece, index) => (
                            <div
                                key={index}
                                className={`cell9 ${hint === index ? 'hint' : ''}`} 
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
                <div className="pieces9">
                    {pieces.map((piece, index) => (
                        <img
                            key={indices[index]}
                            src={piece}
                            alt={`Piece ${indices[index]}`}
                            className={`piece ${selectedPieceId === indices[index] ? 'selected' : ''}`}
                            draggable
                            onDragStart={(e) => dragStart(e, index)}
                            onClick={() => handlePieceClick(indices[index])}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
}

export default PiecesGallery;

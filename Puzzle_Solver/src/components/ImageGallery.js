import React, { useState, useEffect } from 'react';

function ImageGallery({ onSelectImage }) {
    const [imageData, setImageUrls] = useState([]);
    const [selectedImageId, setSelectedImageId] = useState(null);

    useEffect(() => {
        fetch('http://localhost:5001/api/ImagesCompletes')
          .then(response => response.json()) 
          .then(data => setImageUrls(data))
          .catch(error => console.error('Erreur lors de la récupération des images : ', error));
      }, []);

    const handleClick = (index) => {
        onSelectImage(index); 
        setSelectedImageId(index);
    };

    return (
        <div>
            {imageData.map((image, index) => (
                <img key={index} src={image} alt={`Image ${index}`} className={index === selectedImageId ? "selected-image" : "image"} onClick={() => handleClick(index)} />
            ))}
        </div>
    );
}

export default ImageGallery;

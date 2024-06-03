import React, { useState } from 'react';
import '../App.css';
import back from './back.png';

const Logo = () => {
    const [imageSrc, setImageSrc] = useState('');


    useState(() => {
        setImageSrc(back);
    }, []);

    return (
        <>
            {imageSrc && <img src={imageSrc} alt="Logo" className="img_logo" />}
        </>
    );
    
}

export default Logo;

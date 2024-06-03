import React from 'react';
import '../App.css';

const ButtonCard = ({inside}) => {
    return (

        <div class="inside">
          <div class="button">{inside.icon}</div>
          <h6>{inside.text}</h6>
      
          </div> 
        
    );
}
export default ButtonCard;
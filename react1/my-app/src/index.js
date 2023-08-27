import React from "react";
import  ReactDOM  from "react-dom";


const App= () => {
    const style = {text: 'submit'}
    
    return(
        <div className="ui comments">
            <div className="comment">
            
                <a href="/" className="avatar">
                </a>
            </div>
        </div>
    )   
}

ReactDOM.render(
    
    document.querySelector('#root')
)
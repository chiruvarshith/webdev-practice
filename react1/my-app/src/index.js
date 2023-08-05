import React from "react";
import  ReactDOM  from "react-dom";


const App= () => {
    const style = {text: 'submit'}
    
    return(
        <div>
            <label htmFor="name" class="label">Enter email</label>
            <input id="name" type="text" />
            <button style={{backgroundColor:'red', color:'white'}}>
                { style.text }
            </button>
        </div>
    )
}

ReactDOM.render(
    <App />,
    document.querySelector('#root')
)
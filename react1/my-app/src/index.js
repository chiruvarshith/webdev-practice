import React from "react";
import  ReactDOM  from "react-dom";


const App= () => {
    return(
        <div>
            <label for="name" class="label">Enter email</label>
            <input id="name" type="text" />
            <button style={{backgroundColor:'red', color:'white'}}>submit</button>
        </div>
    )
}

ReactDOM.render(
    <App />,
    document.querySelector('#root')
)
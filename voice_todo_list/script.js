if('SpeechRecognition' in window || 'webkitSpeechRecognition' in window){

    let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    let taskInput = document.querySelector('#taskInput');
    

    let taskList = document.querySelector("#taskList");

    taskInput.addEventListener('focus',()=>{
        recognition.start();
    });

    recognition.onresult = (event)=>{
        let translate = event.results[0][0].transcipt;
        taskInput.value = translate;
        addTask();
    }

    function addTask(){
        let taskText = taskInput.value.trim();

        if(taskText !== ''){
            let taskItem = document.createElement("li");
            taskItem.innerHTML = `
            <span>${taskText}</span><button onclick="deleteTask(this)">Delete</button>
            `;
            taskList.appendChild(taskItem);
            taskInput.value = "";
        }

        recognition.onend = ()=>{
            recognition.stop();
        }

        
    }

    function deleteTask(e){
        let liParent = e.parentNode;
        
        if(window.confirm("Are you sure you want to delete this task???")){
            taskList.removeChild(liParent);
        }
    }


}
else{
    alert("your browser does not support speech recognition!!!")
}
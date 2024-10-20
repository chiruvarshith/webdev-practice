if('SpeechRecognition' in window || 'webkitSpeechRecognition' in window){

    let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    let taskInput = document.querySelector('#taskInput');
    let addTask = document.querySelector("#addTask");

    let taskList = document.querySelector("#taskList");

    taskInput.addEventListener('focus',()=>{
        recognition.start();
    });

    recognition.onresult = (event)=>{
        let translate = event.results[0][0].transcipt;
        taskInput.value = translate;
    }

    function addTask(){
        let taskText = taskInput.value.trim();

        if(taskText !== ''){
            let taskItem = document.createElement("li");
            taskItem.innerHTML = `
            <span>${taskText}</span><button>Delete</button>
            `;
        }
    }


}
else{
    alert("your browser does not support speech recognition!!!")
}
var arithmeticexample = 5+3;
var assignmentexample = 10;
assignmentexample += 5;
var exponentialoperator=5**3;
var comparisionexample= 7 < 4;
var logicalexample= true && false;
var stringexample= 'hello, ' + 'world!';
var ternaryexample=(5 > 3) ? "yes" : "no";


document.getElementById("arithmeticexample").textContent="5+3 =" + arithmeticexample;
document.getElementById("assignmentexample").textContent="Initial value: 10, After += 5:" + assignmentexample;
document.getElementById("exponentialoperator").textcontent="5 to the power 3 ="+exponentialoperator;   
document.getElementById("comparisionexample").textcontent="7 < 4 is " + comparisionexample;
document.getElementById("logicalexample").textcontent="true && false is" +  logicalexample;
document.getElementById("stringexample").textcontent="\"hello, \" + \"world\" = " + stringexample;
document.getElementById("ternaryexample").textcontent="(5 > 3) ? \"yes\" : \"no\" = " + ternaryexample;


var loopingexampletext= "";
for (var i = 1; i<=5; i++) {
    loopingexampletext += "iteration" + i + "<br>";

}

document.getElementById("loopingexample").innerHTML = loopingexampletext;

for (let i = 1; i<=10; i++) {
    console.log(i);
}

let count = 0;
while (count < 5) {
    console.log(`while loop iteration ${count + 1}`);
    count++;
}

let num=6;

do {
    console.log(`Do-While loop iteration ${num + 1}`);
    num++;
} while (num<5)


let day=sunday;
switch(day) {
    case 'monday':
        console.log('it')
}


sayhello();
    function greet(name) {
        return "hello" + name +"!"
    }
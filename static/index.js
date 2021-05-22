import "./styles.css.proxy.js";
console.log("hello world!");

function screenSwitch(request) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/screenSwitch", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({value: request}));
}

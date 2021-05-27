function screenSwitch(request) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/screenSwitch/Live&Off", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({request: request}));
    document.location.href = '/';
}
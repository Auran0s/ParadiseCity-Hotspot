function screenSwitch(request) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/screenSwitch/liveOn", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({request: request}));
    document.location.href = '/livescreencontrol'
}
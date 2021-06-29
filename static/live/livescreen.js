function checkControl(){
    fetch('/api/getData').then(function(response) {
        return response.json();
      }).then(function(data) {
        console.log(data['screensCommands']);
        if (data['screensCommands']['screen1']['Live'] == 'false' && data['screensCommands']['screen2']['Live'] == 'false') {
          document.location.href = '/';
        }
      });
}

var interval = setInterval(function () { checkControl(); }, 1000);
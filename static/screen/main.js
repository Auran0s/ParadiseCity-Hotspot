function checkControl(){
    fetch('/screenSwitch/live').then(function(response) {
        return response.json();
      }).then(function(data) {
        console.log(data['switchScreens']['Live']);
        if (data['switchScreens']['Live'] == true) {
          document.location.href = '/livescreen';
        }
      });
}

var interval = setInterval(function () { checkControl(); }, 1000);
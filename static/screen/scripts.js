function checkControl(){
    fetch('/screenSwitch/liveOn').then(function(response) {
        return response.json();
      }).then(function(data) {
        console.log(data);
        if (data["liveOn"] == true) {
            document.location.href = '/livescreen';
        }
      });
}

var interval = setInterval(function () { checkControl(); }, 1000);
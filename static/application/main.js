function screenSwitch() {
    var requestOptions = {
        method: 'POST',
        redirect: 'follow'
      };
      
      fetch("https://10.96.16.65:5001/api/screenSwitch/Live/On", requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));
    setTimeout(function(){
        document.location.href = '/livecontrol';
    }, 500);
}
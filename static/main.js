import "./styles.css.proxy.js";
let url = '/api/'
function getMesssages(){
    document.querySelectorAll('.card').forEach(function(a){
      a.remove()
    })
    fetch(url+'messages/getData').then(function(response) {
        return response.json();
      }).then(function(data) {
        for (let i in data['Messages']){


          let card = document.createElement('div');
          card.setAttribute('class', 'card');

          let idNumber = ("div" + Number(i)).toString();
          console.log(idNumber);

          let rowCard = document.getElementById(idNumber).appendChild(card);

          card.innerHTML += "<svg xmlns=\"http://www.w3.org/2000/svg\" fill=\"currentColor\" class=\"block w-5 h-5 text-gray-400\" viewBox=\"0 0 975.036 975.036\">\
          <path d=\"M925.036 57.197h-304c-27.6 0-50 22.4-50 50v304c0 27.601 22.4 50 50 50h145.5c-1.9 79.601-20.4 143.3-55.4 191.2-27.6 37.8-69.399 69.1-125.3 93.8-25.7 11.3-36.8 41.7-24.8 67.101l36 76c11.6 24.399 40.3 35.1 65.1 24.399 66.2-28.6 122.101-64.8 167.7-108.8 55.601-53.7 93.7-114.3 114.3-181.9 20.601-67.6 30.9-159.8 30.9-276.8v-239c0-27.599-22.401-50-50-50zM106.036 913.497c65.4-28.5 121-64.699 166.9-108.6 56.1-53.7 94.4-114.1 115-181.2 20.6-67.1 30.899-159.6 30.899-277.5v-239c0-27.6-22.399-50-50-50h-304c-27.6 0-50 22.4-50 50v304c0 27.601 22.4 50 50 50h145.5c-1.9 79.601-20.4 143.3-55.4 191.2-27.6 37.8-69.4 69.1-125.3 93.8-25.7 11.3-36.8 41.7-24.8 67.101l35.9 75.8c11.601 24.399 40.501 35.2 65.301 24.399z\">\</path>\
        </svg>";

          let content = document.createElement('p');
          content.setAttribute('class', 'card-text');

          content.innerHTML = data['Messages'][i]['split_content'];

          rowCard.appendChild(content);

          let tagsA = document.createElement('a');
          tagsA.setAttribute('class', 'tags');
          rowCard.appendChild(tagsA);

          let tags = document.createElement('span');
          
          console.log(data['Messages'][i]['filtre'])

          switch (Number(data['Messages'][i]['filtre'][0])) {
            case 0:
              tags.innerHTML = "les probl\u00e8mes"
              tags.setAttribute('class', 'tags-problems');
              break;
            case 1:
                tags.innerHTML = "besoin d'aide"
                tags.setAttribute('class', 'tags-help');
                break;
            case 2:
                tags.innerHTML = "remonté d'id\u00e9es"
                tags.setAttribute('class', 'tags-ideas');
                break;
            case 3:
                tags.innerHTML =  "\u00e9venements"
                tags.setAttribute('class', 'tags-event');
                break;
            case 4:
                tags.innerHTML = "une simple pens\u00e9e"
                tags.setAttribute('class', 'tags-thinking');
                break;
            default:
              break;
          };

          tagsA.appendChild(tags);
        }
      });
};

function sondage(){
  fetch(url+'sondage').then(function(response) {
    return response.json();
  }).then(function(data) {
    if (data['SondageState'] == 'true') {
      document.getElementById('sondage').classList.remove('invisible');
    }
    else{
      document.getElementById('sondage').classList.add('invisible');
    }
    let sondageText = document.getElementById('sondage-text');
    sondageText.innerHTML = data['Message'];

    let percent = Number(data['Answer']['oui']) * 100 / Number(data['Answer']['non']);
    console.log(Number(Math.round(percent)))
    document.getElementById('percent').style.width = percent + '%';
  });
};

function liveChecking(){
  fetch(url+'notifications').then(function(response) {
    return response.json();
  }).then(function(data) {
    console.log(data['Notification']['askLive'])
    if (data['Notification']['askLive'] == 'true') {
      document.getElementById('liveAlert').classList.remove('invisible');
    }
    else{
      document.getElementById('liveAlert').classList.add('invisible');
    }
  });
};

function checkControl(){
    fetch(url+'getData').then(function(response) {
        return response.json();
      }).then(function(data) {
        console.log(data['screensCommands']);
        if (data['screensCommands']['screen1']['Live'] == 'true' && data['screensCommands']['screen2']['Live'] == 'true') {
            document.location.href = '/livescreen';
        }
      });
}


getMesssages();
var interval = setInterval(function () { sondage(); liveChecking(); checkControl(); }, 1000);
var interval2 = setInterval(function () { getMesssages(); }, 10000);
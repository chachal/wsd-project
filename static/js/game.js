function resizeIframe(obj) {
  obj.style.height = "480px";
  obj.style.width = "640px";
}

window.addEventListener("message", receiveMessage, false);

function receiveMessage(event){
  var origin = event.origin || event.originalEvent.origin
  if(origin !== "http://webcourse.cs.hut.fi"){
    return;
  }
  if(event.data.messageType == "SCORE"){
    setScores(event.data.score);
    setTimeout(getScores, 1000);
  }
  if(event.data.messageType == "SAVE"){
    saveGame(event.data.gameState);
  }
  if(event.data.messageType == "LOAD_REQUEST"){
    loadRequest();
  }
  if(event.data.messageType == "SETTING"){
    document.getElementById("game").width = event.data.options.width;
    document.getElementById("game").height = event.data.options.height;
    getScores();
  }
}

function setScores(scores){
  $.ajax({type:"GET",url:"/setScores/?gameID=" + gmID + "&score=" + scores});
}

function getScores(){
  $.ajax({type:"GET",dataType:"json",url:"/getScores/?gameID=" + gmID,success:function(data){
    inputstr = "";
    for(index = 0; data.length - 1 >= index; ++index){
      inputstr += '<tr><td class="highscore">' + data[index].user__username + '</td><td class="highscore">' + data[index].score + '</td></tr>';
    }
    document.getElementById("scoreboard").innerHTML = inputstr;
  },
  });
}

function saveGame(state){
  var gstate = JSON.stringify(state);
  $.ajax({type:"GET",url:"/saveGame/?gameID=" + gmID + "&gamestate=" + gstate});
}

function loadRequest(){
  var gamewin = document.getElementById("game").contentWindow
  $.ajax({type:"GET",url:"/loadRequest/?gameID=" + gmID,success:function(data){
    if(data != 0) {
      var jsonload = JSON.parse(data);
      var msg = {
            messageType: "LOAD",
            gameState: jsonload
      };
    }
    else{
      var msg = {
            messageType: "ERROR",
            info: "No saved game found"
      };
    }
    gamewin.postMessage(msg, gmURL);
  }
  })
}

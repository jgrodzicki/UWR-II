var time=0.0;
var timeInterval = null;
var shouldGoCenter = false;
var historyArray = new Array();

window.onload = function() {
  reset();

  document.getElementById("main").onmouseover = function() {
    setRed("main");
    if (ifFinished()) {
      clearInterval(timeInterval);
      timeInterval = null;
      historyArray.push(Math.round(time*100)/100);
      historyArray.sort();
      if (historyArray.length > 10) {
        historyArray = historyArray.slice(0, 10);
      }
      setTimeout(function() {reset();}, 1500);
    }
  };

  document.getElementById("main").onmouseout = function() {
    if (!time) {
       timeInterval = setInterval(function() {time+=0.01; document.getElementById("time").innerHTML="TIME: " + parseFloat(Math.round(time*100)/100).toFixed(2) + "s";}, 10)
    }
    shouldGoCenter = false;
  }

  document.getElementById("first").onmouseover = function() {
    if (time != 0) {
      if (checkIfPenalty("first")) {
        applyPenalty("first");
      } else {
        shouldGoCenter = true;
        setRed("first");
        setGray("main");
      }
    }
  };

  document.getElementById("second").onmouseover = function() {
    if (time != 0) {
      if (checkIfPenalty("second")) {
        applyPenalty("second");
      } else {
        shouldGoCenter = true;
        setRed("second");
        setGray("main");
      }
    }
  };

  document.getElementById("third").onmouseover = function() {
    if (time != 0) {
      if (checkIfPenalty("third")) {
        applyPenalty("third");
      } else {
        shouldGoCenter = true;
        setRed("third");
        setGray("main");
      }
    }
  };

  document.getElementById("fourth").onmouseover = function() {
    if (time != 0) {
      if (checkIfPenalty("fourth")) {
        applyPenalty("fourth");
      } else {
        shouldGoCenter = true;
        setRed("fourth");
        setGray("main");
      }
    }
  };
};

setRandomSquares = function() {
  document.getElementById("first").style.left = Math.floor(Math.random()*100) + "px";
  document.getElementById("first").style.top = Math.floor(Math.random()*100) + "px";

  document.getElementById("second").style.right = Math.floor(Math.random()*100) + "px";
  document.getElementById("second").style.top = Math.floor(Math.random()*100) + "px";

  document.getElementById("third").style.left = Math.floor(Math.random()*100) + "px";
  document.getElementById("third").style.bottom = Math.floor(Math.random()*100) + "px";

  document.getElementById("fourth").style.right = Math.floor(Math.random()*100) + "px";
  document.getElementById("fourth").style.bottom = Math.floor(Math.random()*100) + "px";
}

function setRed(id) {
  document.getElementById(id).style.background="red";
}

function setGray(id) {
  document.getElementById(id).style.background="lightgray";
}

function getColor(id) {
  return document.getElementById(id).style.background;
}

function ifFinished() {
  return getColor("first")=="red" && getColor("second")=="red" && getColor("third")=="red" && getColor("fourth")=="red";
}

function reset() {
  setRandomSquares();
  setHistoryInnerHTML();

  time = 0;
  document.getElementById("time").innerHTML="TIME: 0.00s";
  setGray("first");
  setGray("second");
  setGray("third");
  setGray("fourth");
}

function checkIfPenalty(id) {
  return shouldGoCenter && timeInterval!==null;
}

function applyPenalty(id) {
  time += 0.5;
  document.getElementById(id).innerHTML="PENALTY!";
  setTimeout(function() {document.getElementById(id).innerHTML="";}, 1500);
}

function setHistoryInnerHTML() {
  document.getElementById("history").innerHTML = "HISTORY<br>";
  for (var i = 0; i < historyArray.length; i++) {
    document.getElementById("history").innerHTML += historyArray[i] + "s<br>";
  }
}

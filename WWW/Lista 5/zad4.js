var trianglePoints = [[50, 700], [375, 50], [700, 700]];
var dX;
var dY;


var canvas;
var ctx;

drawTriangle = function() {
  ctx.moveTo(trianglePoints[2][0], trianglePoints[2][1]);
  for (var i = 0; i < 3; i++) {
    ctx.lineTo(trianglePoints[i][0], trianglePoints[i][1]);
  }

  ctx.stroke();
}

findFirstPoint = function() {
  do {
    var x = Math.floor(Math.random() * (trianglePoints[2][0] - trianglePoints[0][0])) + trianglePoints[0][0];
    var y = Math.floor(Math.random() * (trianglePoints[2][1] - trianglePoints[1][1])) + trianglePoints[1][1];
  } while (y < 2*x-700 || y < -2*x+800);

  dX = x;
  dY = y;
  // var r1 = Math.random();
  // var r2 = Math.random();
  //
  // dX = (1 - Math.sqrt(r1)) * trianglePoints[1][0] + (Math.sqrt(r1)* (1 - r2)) * trianglePoints[0][0] + (r2 + Math.sqrt(r1)) * trianglePoints[1][0];
  // dY = (1 - Math.sqrt(r1)) * trianglePoints[1][1] + (Math.sqrt(r1)* (1 - r2)) * trianglePoints[0][1] + (r2 + Math.sqrt(r1)) * trianglePoints[1][1];
}

$(document).ready(function() {
  canvas = document.getElementById("canvas");
  ctx = canvas.getContext("2d");
  drawTriangle();

  findFirstPoint();

  var i = 0;
  var interval = setInterval(function() {if (i < 50000) {
    var randPointOfTriangle = Math.floor(Math.random() * 3);
    dX = (dX + trianglePoints[randPointOfTriangle][0]) / 2;
    dY = (dY + trianglePoints[randPointOfTriangle][1]) / 2;
    ctx.fillRect(dX, dY, 1, 1);
    ctx.stroke();
    i++;
  }
  else {
    console.log("Done");
    clearInterval(interval);
  }}, 0);

  // for (i = 0; i < 100000; i++) {
  //   var randPointOfTriangle = Math.floor(Math.random() * 3);
  //     dX = (dX + trianglePoints[randPointOfTriangle][0]) / 2;
  //     dY = (dY + trianglePoints[randPointOfTriangle][1]) / 2;
  //     ctx.fillRect(dX, dY, 2, 2);
  //     // ctx.moveTo(dX, dY);
  //     // ctx.lineTo(trianglePoints[randPointOfTriangle][0], trianglePoints[randPointOfTriangle][1]);
  //     ctx.stroke();
  //     i++;
  // }

})

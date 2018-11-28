var currentImage = 0;
var imgPath = ["img/img1.png", "img/img2.png", "img/img3.png", "img/img4.png"];
var interval;
var intervalValue;
var fadeValue;

switchImage = function() {
  currentImage++;
  if (currentImage > 4) {
    currentImage = 1;
  }

  $("#numberOfImage").html(currentImage + " / 4");
  $("#currentImage").fadeOut(fadeValue, function() {
    $("#currentImage").attr("src", imgPath[currentImage-1]);
  }).fadeIn(fadeValue);
}

change = function() {
  intervalValue = $("#slider").val() * 1000;
  $("#sliderValue").html("Photos change after " +intervalValue/1000 + " second");
  if (intervalValue > 1000) {
    $("#sliderValue").html($("#sliderValue").html() + "s");
  }
  fadeValue = 100 + intervalValue / 10;
  clearInterval(interval);
  interval = setInterval(function() {switchImage();}, intervalValue);
}

setVariables = function() {
  intervalValue = $("#slider").val() * 1000;
  fadeValue = 100 + intervalValue / 10;
  interval = setInterval(function() {switchImage();}, intervalValue);
}


$(document).ready(function() {
  setVariables();
  switchImage();

  $("#sliderValue").html("Photos change after " + intervalValue/1000 + " seconds");

  $("#slider").on("input", function() {change();});

  $("#currentImage").mouseover(function() {
    clearInterval(interval);
  });

  $("#currentImage").mouseout(function() {
    interval = setInterval(function() {switchImage();}, intervalValue);
  });
});

var color;

function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  color = ev.target.style.backgroundColor;
}

function drop(ev) {
  ev.preventDefault();
  ev.target.style.border = "1px solid black";
  ev.target.style.backgroundColor = color;
}

function dragEnter(ev) {
  ev.target.style.border = "2px solid " + color;
}

function dragLeave(ev) {
  ev.target.style.border = "1px solid black";
}

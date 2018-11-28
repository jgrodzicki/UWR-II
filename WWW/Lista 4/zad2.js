function validate() {
  var numerkonta = document.getElementById("numerkonta").value;
  var pesel = document.getElementById("pesel").value;
  var dataUrodzenia = document.getElementById("dataurodzenia").value;
  var email = document.getElementById("email").value;
  var flag = true;


  if (!numerkonta.match(/\d{26}/)) {
    document.getElementById("numerkontaerror").innerHTML = "Niepoprawny numer konta";
    flag = false;
  }
  else {
    document.getElementById("numerkontaerror").innerHTML = "";
  }

  if (!pesel.match(/\d{11}/)) {
    document.getElementById("peselerror").innerHTML = "Niepoprawny numer PESEL";
    flag = false;
  }
  else {
    document.getElementById("peselerror").innerHTML = "";
  }

  if (!dataUrodzenia.match(/\d{4}-\d{2}-\d{2}/)) {
    document.getElementById("dataurodzeniaerror").innerHTML = "Niepoprawna data";
    flag = false;
  }

  if (!email.match(/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]+/)) {
    document.getElementById("emailerror").innerHTML = "Niepoprawny adres email";
    flag = false;
  }

  return flag;
}

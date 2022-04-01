window.onload = function() {
  document.getElementById("container").style.display = "flex";
}


function emptyPasswordFields() {
  document.getElementById("password").value = "";
  document.getElementById("con_pass").value = "";
}

function sendPostRequestToCurrentURL(data) {
  var xhr = new XMLHttpRequest();
  var result = document.getElementById("result");

  xhr.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 200) {
      result.innerHTML = this.responseText;
    }
    else if(this.status == 500){
      result.innerHTML = "Username Exists.";
    }
    else {
      result.innerHTML = "Something Went Wrong.";
    }
  }

  var url = window.location.href;
  xhr.open("POST", url, true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
  xhr.send("username="+data["username"]+"&password="+data["password"]);
}

function validatePasswordAndRegister() {

  var givenPassword = document.getElementById("password").value;
  var confPassword = document.getElementById("con_pass").value;
  var username = document.getElementById("username").value;

  if(givenPassword !== confPassword) {
    alert("Passwords did not match, please re-enter.");
  }

  else {
    data = {username: username, password: givenPassword};
    sendPostRequestToCurrentURL(data);
  }

  emptyPasswordFields();
}

function validateUsernameAndPassword() {
  var xhr = new XMLHttpRequest();
  var result = document.getElementById("result");
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  var url = window.location.href;

  xhr.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 401) {
      result.innerHTML = this.responseText;
    }
    if(this.readyState == 4 && this.status == 200) {
      window.location.href = "/chat";
    }
  }

  xhr.open("POST", url, true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
  xhr.send("username="+username+"&password="+password);
}

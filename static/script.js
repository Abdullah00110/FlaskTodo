function validateTodo() {
    var title = document.getElementById("title").value;
    var desc = document.getElementById("desc").value;
  
    if (title == "" || desc == "") {
      alert("Please fill in all required fields!");
      return false;
    } else {
      return true;
    }
  }


document.querySelector('.grid').addEventListener('click', function(e) {
  if (e.target.tagName === 'IMG') {
    var howmany = this.querySelectorAll('li').length;
    if (howmany > 1) {
      var removeTarget = e.target.parentNode;
      removeTarget.parentNode.removeChild(removeTarget);
    } else {
      var photoTitle = e.target.alt;
      document.querySelector('#art p').innerHTML = "<p>You've picked: " + photoTitle + "</p>";
    } //howmany
  } // check to see that I clicked on IMG only
}, false); // click event

var no=0;

function loadImages(){

  document.querySelector("#im1").src="outputs/model"+no+"/FACIAL-output1.png";
  document.querySelector("#im2").src="outputs/model"+no+"/FACIAL-output2.png";
  document.querySelector("#im3").src="outputs/model"+no+"/FACIAL-output3.png";
  document.querySelector("#im4").src="outputs/model"+no+"/FACIAL-output4.png";
  document.querySelector("#im5").src="outputs/model"+no+"/FACIAL-output5.png";
  document.querySelector("#im6").src="outputs/model"+no+"/FACIAL-output6.png";
  document.querySelector("#im7").src="outputs/model"+no+"/FACIAL-output7.png";
  document.querySelector("#im8").src="outputs/model"+no+"/FACIAL-output8.png";
  document.querySelector("#im9").src="outputs/model"+no+"/FACIAL-output9.png";
  no=(no+1)%4;
}

function changeModel(){
   document.querySelector('#art p').innerHTML = "<p>Pick your favorite glass frame through the process of elimination. Click on the images you like the least until you are left with a single one.</p>";
  const myNode = document.querySelector(".grid");
  while (myNode.firstChild) {
    myNode.removeChild(myNode.lastChild);
  }
  var element=document.createElement("li");
  element.innerHTML=`<img id="im1" alt="Glass 1">`;
  document.querySelector(".grid").appendChild(element);
  document.querySelector("#im1").src="outputs/model"+no+"/FACIAL-output1.png";
  var element=document.createElement("li");
  element.innerHTML=`<img id="im2" alt="Glass 2">`;
  document.querySelector(".grid").appendChild(element);
  document.querySelector("#im2").src="outputs/model"+no+"/FACIAL-output2.png";
  var element=document.createElement("li");
  element.innerHTML=`<img id="im3" alt="Glass 3">`;
  document.querySelector(".grid").appendChild(element);
  document.querySelector("#im3").src="outputs/model"+no+"/FACIAL-output3.png";
  var element=document.createElement("li");
  element.innerHTML=`<img id="im4" alt="Glass 4">`;
  document.querySelector(".grid").appendChild(element);
  document.querySelector("#im4").src="outputs/model"+no+"/FACIAL-output4.png";
  var element=document.createElement("li");
  element.innerHTML=`<img id="im5" alt="Glass 5">`;
  document.querySelector(".grid").appendChild(element);
  document.querySelector("#im5").src="outputs/model"+no+"/FACIAL-output5.png";
  var element=document.createElement("li");
  element.innerHTML=`<img id="im6" alt="Glass 6">`;
  document.querySelector(".grid").appendChild(element);
  document.querySelector("#im6").src="outputs/model"+no+"/FACIAL-output6.png";
  var element=document.createElement("li");
  element.innerHTML=`<img id="im7" alt="Glass 7">`;
  document.querySelector(".grid").appendChild(element);
  document.querySelector("#im7").src="outputs/model"+no+"/FACIAL-output7.png";
  var element=document.createElement("li");
  element.innerHTML=`<img id="im8" alt="Glass 8">`;
  document.querySelector(".grid").appendChild(element);
  document.querySelector("#im8").src="outputs/model"+no+"/FACIAL-output8.png";
  var element=document.createElement("li");
  element.innerHTML=`<img id="im9" alt="Glass 9">`;
  document.querySelector(".grid").appendChild(element);
  document.querySelector("#im9").src="outputs/model"+no+"/FACIAL-output9.png";
  no=(no+1)%4;
}
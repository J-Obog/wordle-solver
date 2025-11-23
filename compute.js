/*const checkElement = setInterval(() => {
    // window.getElementById("board")
    
    console.log(window.document.getElementById('board')); 
    if (window.document.getElementById('board')) {
    clearInterval(checkElement);
    console.log('Element is now visible!');
    // Your code to execute after the element is visible
  }
}, 1000); 
*/


window.onload = function(){
           const checkElement = setInterval(() => {
    // window.getElementById("board")
    
    console.log(window.document.getElementById('board')); 
    if (window.document.getElementById('board')) {
    clearInterval(checkElement);
    console.log('Element is now visible!');
    // Your code to execute after the element is visible
  }
}, 1000);
};




// Check every 100 milliseconds
//const productA = document.querySelector('button[data-key="q"]');
//console.log(productA); // Output: Product A
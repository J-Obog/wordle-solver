
async function foo() {

while (window.localStorage.getItem("wordToGuess") == null || window.localStorage.getItem("solverGuesses") == null) {
    await new Promise(resolve => setTimeout(resolve, 500));
}

console.log("here"); 

//localStorage.getItem("")
//console.log(window.localStorage.getItem("FOOBAR")); 

const wordToGuess = window.localStorage.getItem("wordToGuess").toLocaleUpperCase(); 
const GUESSES = ["brass", "barns", "brain"]; 

const gameAppRoot = window.document.getElementsByTagName("game-app")[0]; 
const gameKeyboardRoot = gameAppRoot.shadowRoot.querySelector("game-keyboard"); 
const gameThemeManagerRoot = gameAppRoot.shadowRoot.querySelector("game-theme-manager");

const board = gameThemeManagerRoot.querySelector("#board-container");


// Create the new element you want to add
const newChild = document.createElement('div');
newChild.innerHTML = `The word to guess is <b>${wordToGuess}</b>`;

// Append the new child as the first child of the parent
board.prepend(newChild);

gameKeyboardRoot.style.display = 'none'; 

for(word of GUESSES) {
    console.log(word);
    for(letter of word) {
        const keyboardBtn = gameKeyboardRoot.shadowRoot.querySelector(`button[data-key="${letter}"]`); 
        await new Promise(resolve => setTimeout(resolve, 500));
        keyboardBtn.click(); 
    }
    
    const enterBtn = gameKeyboardRoot.shadowRoot.querySelector('button[data-key="↵"]');
    enterBtn.click();  
    await new Promise(resolve => setTimeout(resolve, 2000));
}
}

foo(); 


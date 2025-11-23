import json
import random
import webbrowser
import os
import time

candidates = [] 
historical_solutions = set()
allowed_words = set() 

with open("known.json", "r", encoding="utf") as ifile:
    candidates = json.load(ifile)

with open("wordle_solutions.json", "r", encoding="utf-8") as sol_file:
    historical_solutions = set(json.load(sol_file))

with open("wordle_allowed.json", "r", encoding="utf-8") as allowed_file:
    allowed_words = set(json.load(allowed_file))

predefined_target = None

target_word = predefined_target if predefined_target is not None else random.choice(list(historical_solutions))

not_in_target = set()
known_idxs = {}
unknown_idxs = set()

guesses = 0
won = False

def get_feedback(guess_word):
    if len(guess_word) != 5:
        raise Exception("word must be 5 characters")

    mi = {}
    ni = set()
    mc = set()

    for i in range(5):
        if guess_word[i] == target_word[i]:
            matched_char = guess_word[i]
            if matched_char not in mi:
                mi[matched_char] = set()

            mi[matched_char].add(i)
    
    guess_word_set = set(guess_word)
    target_word_set = set(target_word)

    ni = guess_word_set.difference(target_word_set)

    #for simplicity, let's assume the target word doesn't have any repeating letters
    mc = guess_word_set.intersection(target_word_set).difference(set(mi.keys()))

    return {"mi": mi, "ni": ni, "mc": mc}


def should_still_be_considered(word):
    if len(known_idxs) > 0:
        for char in known_idxs:
            idxs = known_idxs[char]
            idx = list(idxs)[0] # the target word should not have repeating characters
            if word[idx] != char: 
                return False

    if len(unknown_idxs) > 0:
        for char in unknown_idxs:
            if char not in word:
                return False

    if len(not_in_target) > 0:
        for char in not_in_target:
            if char in word:
                return False
            
    return True

def update_candidate_words():
    global candidates
    candidates = list(filter(should_still_be_considered, candidates)) 

guessed_words = []

while guesses < 6:
    guess_word = random.choice(candidates)

    # this doesn't give the solver any more information that a person would get if the word is invalid
    is_word_valid = (guess_word in allowed_words) or (guess_word in historical_solutions)

    if is_word_valid:
        guessed_words.append(guess_word)

    if guess_word == target_word:
        won = True
        break

    feedback = get_feedback(guess_word)
    
    not_in_target.update(feedback["ni"])

    for char in feedback["mi"]:
        if char in known_idxs:
            known_idxs[char].update(feedback["mi"][char])
        else:
            known_idxs[char] = feedback["mi"][char]
    
    unknown_idxs.update(feedback["mc"])

    for char in known_idxs:
        unknown_idxs.discard(char)

    update_candidate_words()

    if is_word_valid:
        guesses += 1 
 

jsfile_content = f"const guessArr={guessed_words};\nwindow.localStorage.setItem('solverGuesses', JSON.stringify(guessArr));\nwindow.localStorage.setItem('wordToGuess', '{target_word}');"

with open("storage.js", "w+", encoding="utf-8") as out_js_file:
    out_js_file.write(jsfile_content)
    

time.sleep(1)
#print(os.getcwd())


webbrowser.open_new_tab(f'http://localhost:8009/game.html?tword={target_word}&tries={json.dumps(guessed_words)}')
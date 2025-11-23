import json

candidates = [] 

with open("known.json", "r", encoding="utf") as ifile:
    candidates = json.load(ifile)

target_word = "honor"
start_word = "rinse"

not_in_target = set()
known_idxs = {}
unknown_idxs = set()

guesses = 0
won = False

while guesses < 6:
    guess_word = None
    if guesses == 0:
        guess_word = start_word
    else:
        pass

    if guess_word == target_word:
        won = True
        break

    guesses += 1 


print("won" if won else "lost")
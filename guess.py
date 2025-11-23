import json

candidates = [] 

with open("known.json", "r", encoding="utf") as ifile:
    candidates = json.load(ifile)

target_word = "brain"
start_word = "rinse"

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


while guesses < 6:
    guess_word = None
    if guesses == 0:
        guess_word = start_word
    else:
        pass

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

    guesses += 1 
 

print("won" if won else "lost")
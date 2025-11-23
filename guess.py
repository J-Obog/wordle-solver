import json
import random
from typing import List
import webbrowser
import os
import time
from enum import IntEnum
from dataclasses import dataclass

class LetterFeedbackType(IntEnum):
    NOT_PRESENT = 0
    WRONG_SPOT = 1
    CORRECT = 2

@dataclass
class LetterFeedback:
    feedback_type: LetterFeedbackType
    letter: chr
    letter_index: int

def get_json_from_file(filename):
    with open(filename, "r", encoding="utf-8") as ifile:
        return json.load(ifile)

def get_guess_feedback(guess_word: str, target_word: str) -> List[LetterFeedback]:
    if len(guess_word) != 5:
        raise Exception("word must be 5 characters")
    
    feedback = []

    for i in range(5):
        feedback_type = None
        if guess_word[i] == target_word[i]:
            feedback_type = LetterFeedbackType.CORRECT
        elif guess_word[i] not in target_word:
            feedback_type = LetterFeedbackType.NOT_PRESENT
        else:
            feedback_type = LetterFeedbackType.WRONG_SPOT

        feedback.append(LetterFeedback(feedback_type, guess_word[i], i))

    return feedback

def get_potential_guesses(letter_feedbacks: List[LetterFeedback], known_words: List[str]) -> List[str]:
    not_present_set = set()
    correct_idx_map = {}
    wrong_spot_map = {}

    for letter_feedback in letter_feedbacks:
        if letter_feedback.feedback_type == LetterFeedbackType.CORRECT:
            letter = letter_feedback.letter
            if letter not in correct_idx_map:
                correct_idx_map[letter] = []

            correct_idx_map[letter].append(letter_feedback.letter_index)
        elif letter_feedback.feedback_type == LetterFeedbackType.NOT_PRESENT:
            not_present_set.add(letter_feedback.letter)
        else:
            letter = letter_feedback.letter
            if letter not in wrong_spot_map:
                wrong_spot_map[letter] = []

            wrong_spot_map[letter].append(letter_feedback.letter_index) 


    #print(letter_feedbacks, not_present_set, correct_idx_map, wrong_spot_map)
    candidate_words = []

    for known_word in known_words:
        if len(wrong_spot_map) > 0:
            if any([letter in not_present_set for letter in known_word]):
                continue
        
        if len(correct_idx_map) > 0:
            should_still_consider = True
            for correct_idx_letter in correct_idx_map:
                for idx in correct_idx_map[correct_idx_letter]:
                    if known_word[idx] != correct_idx_letter:
                        should_still_consider = False
            
            if not should_still_consider:
                continue

        if len(wrong_spot_map) > 0:
            should_still_consider = True
            for wrong_spot_letter in wrong_spot_map:
                for idx in wrong_spot_map[wrong_spot_letter]:
                    if known_word[idx] == wrong_spot_letter:
                        should_still_consider = False
            
            if not should_still_consider:
                continue
        
        candidate_words.append(known_word)

    return candidate_words


known_words = get_json_from_file("known.json")
historical_solutions = set(get_json_from_file("wordle_solutions.json"))
allowed_words = set(get_json_from_file("wordle_allowed.json"))
guessed_words = []
target_word = random.choice(list(historical_solutions))
guess_feedbacks: List[LetterFeedback] = []
guesses = 0

#print("TARGET=", target_word)

while guesses < 6:
    potential_guesses = get_potential_guesses(guess_feedbacks, known_words)
    guess_word = random.choice(potential_guesses)

    is_word_valid = (guess_word in allowed_words) or (guess_word in historical_solutions)

    if not is_word_valid:
        continue

    guessed_words.append(guess_word)
    guesses += 1 

    if guess_word == target_word:
        break

    guess_feedbacks.extend(get_guess_feedback(guess_word, target_word))


time.sleep(1)
webbrowser.open_new_tab(f'http://localhost:8009/game.html?tword={target_word}&tries={json.dumps(guessed_words)}')
import json
from datetime import datetime
from random import randint

from dash.exceptions import PreventUpdate


def evaluate(word_to_evaluate, evaluations, previous_guesses):

    if word_to_evaluate is None:
        raise PreventUpdate()
    evaluation_result = _evaluate_word(word_to_evaluate)
    evaluations.append(evaluation_result)
    previous_guesses.append(word_to_evaluate)
    completed_status = evaluations[-1] == ['G', 'G', 'G', 'G', 'G']
    return evaluations, previous_guesses, completed_status


def get_output_classes(evaluation):

    output_classes = []

    if len(evaluation) > 0:
        letter_no = 0
        for l in evaluation:
            letter_no += 1
            if l == 'G':
                class_name = '{}-{}-{}'.format('green-card', 'animation-fade', letter_no)
            elif l == 'Y':
                class_name = '{}-{}-{}'.format('yellow-card', 'animation-fade', letter_no)
            else:
                class_name = '{}-{}-{}'.format('gray-card', 'animation-fade', letter_no)
            output_classes.append(class_name)

    return output_classes


def _evaluate_word(word):

    todays_word = _get_todays_word()
    result = []
    guessed_letters = []

    for i in range(5):
        guessed_letters.append(word[i])
        if word[i] == todays_word[i]:
            result.append('G')
        elif word[i] in todays_word:
            result.append('Y')
        else:
            result.append('_')

    yellow_letter_indices = [x for x in range(5) if result[x] == 'Y']
    green_letter_indices = [x for x in range(5) if result[x] == 'G']
    remaining_letters = [todays_word[x] for x in range(5) if x not in green_letter_indices]

    for i in yellow_letter_indices:
        letter = word[i]
        if letter not in remaining_letters:
            result[i] = '_'
        else:
            remaining_letters[remaining_letters.index(letter)] = '.'

    return result


def _get_todays_word():
    date: str = _get_todays_date()
    assigned_words = _get_assigned_words_dict()
    if date not in assigned_words:
        _assign_new_word(date)
        assigned_words = _get_assigned_words_dict()
    return assigned_words[date]


def _get_assigned_words_dict() -> dict:
    with open('./assigned_words.json', 'r') as f:
        words_dict = json.load(f)
    return words_dict


def _assign_new_word(date: str):
    words_list = _get_words_list()
    assigned_words_dict = _get_assigned_words_dict()
    assigned_words_list = list(assigned_words_dict.values())
    while True:
        index = randint(0, len(words_list))
        new_word = str.upper(words_list[index]).strip()
        if new_word not in assigned_words_list:
            break
    assigned_words_dict[date] = new_word

    with open('./assigned_words.json', 'w') as f:
        json.dump(assigned_words_dict, f)


def _get_words_list():
    with open('./words.txt', 'r') as f:
        words = f.readlines()
    return words


def _get_todays_date() -> str:
    return datetime.now().isoformat().split('T')[0]
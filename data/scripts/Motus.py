import random
#------------------------------------------------------
from data.scripts.Utils import resource_path

def import_word_list() -> dict:
    word_list = open(resource_path(r"data/word_list.txt"),"r").read().split("\n")       
    word_list_by_len = {5:[],6:[],7:[],8:[],9:[]}
    for word in word_list: word_list_by_len[len(word)].append(word)

    return word_list_by_len

def choose_word(word_list_by_len: dict) -> str:
    word_lenght = random.randint(5,8)
    word = random.choice(word_list_by_len[word_lenght])
    
    return word

def check_word(word: str, submit_word: str) -> bool:
    if submit_word == word: return True
    else: return False

def is_word_in_list(word: str, word_list: dict) -> bool:
    if word in word_list[len(word)]: return True
    else: return False

def check_letters_pos(word: str, submit_word: str) -> list:
    tmp_word = list("-"*len(word))
    letters_color = list("-"*len(word))
    
    for i in range(len(submit_word)):
        if submit_word[i] == word[i]:
            tmp_word[i] = submit_word[i]
            letters_color[i] = "green"

    for i in range(len(submit_word)):
        if submit_word[i] in word and submit_word[i] != word[i]:
            if tmp_word.count(submit_word[i]) < word.count(submit_word[i]):
                tmp_word[i] = submit_word[i]
                letters_color[i] = "orange"
   
    return letters_color
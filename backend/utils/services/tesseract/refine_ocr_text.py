import sys
import re
import time






chars_group = (
    ('ب', 'ی', 'پ'),
    ('ن', 'ت'),
    ('ع', 'غ'),
    ('ف', 'ق'),
    ('ص', 'ض'),
    ('ط', 'ظ'),
    ('ت', 'ث'),
    ('ح', 'خ'),
    ('ح', 'ج', 'چ'),
    ('ک', 'گ'),
    ('د', 'ذ'),
    ('ر', 'ز', 'ژ'),
    ('س', 'ش')
    )

t = time.time()

args = sys.argv[1:]  # Get input arguments excluding the script name
input_path = args[0]


input_text = ""
with open(input_path, "r", encoding='utf-8') as input_file:
    input_text = str(input_file.read())

with open("small.txt", "r", encoding='utf-8') as words_file:
    words_text = str(words_file.read())

words_text = f"\n{words_text}\n"

input_words = re.split(r'[\s|\n]', input_text)


for i, w in enumerate(input_words):
    if f"\n{w}\n" in words_text:
        continue
    found_new_word = None
    for j, char in enumerate(w):
        
        for char_g in chars_group:
            if char in char_g:                
                for ch in char_g:
                    new_word = w.replace(char, ch)
                    if f"\n{new_word}\n" in words_text:
                        found_new_word = new_word
                        break

            if found_new_word is not None:
                break
    if found_new_word is not None:
        input_words[i] = found_new_word

with open("output_small.txt", "+w", encoding="utf-8") as output_file:
    output_file.write(" ".join(input_words))

print("Done in ",(time.time() - t), " seconds")
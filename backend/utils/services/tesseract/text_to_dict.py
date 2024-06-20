
import re

input_text = ""
with open("dic.txt", "r", encoding="utf-8") as file:
    input_text = file.read()


#words = re.findall("/^[\u0600-\u06FF\s]+$/", input_text)
words = re.findall("[ء-۹]+", input_text)
words = set(words)
print("Unique words count: ", len(words))

with open("dic_final.txt", "w+", encoding="utf-8") as file:
    file.write("\n".join(words))
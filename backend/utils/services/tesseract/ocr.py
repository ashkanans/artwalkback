import os
import re
import subprocess
import sys
import time
from pathlib import Path

import pymupdf  # imports the pymupdf library


class TesseractError(Exception):
    def __init__(self, message, stdout, stderr):
        super().__init__(message)
        self.stdout = stdout
        self.stderr = stderr

dic_path = "backend/utils/services/tesseract/dic_small.txt"

def replace_func(match):
    text = match.group(0)
    return " "


def ocr_image(input_image):
    global dic_path
    t = time.time()
    tesseract_path = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    command = [str(tesseract_path), '-l', 'fas', str(input_image), str(t)]

    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Tesseract output:", result.stdout.decode())
        print("Tesseract error (if any):", result.stderr.decode())
    except subprocess.CalledProcessError as e:
        raise TesseractError("Tesseract command failed", e.stdout.decode(), e.stderr.decode()) from e

    text_path = str(t) + ".txt"


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


    input_text = ""
    with open(text_path, "r", encoding='utf-8') as input_file:
        input_text = str(input_file.read())

    input_text =  re.sub(r'[$&+,:;=?@#|\'<>.^*()%!-]', replace_func, input_text)
    #input_text = input_text.replace('\u200c', ' ')
    input_text = input_text.replace('\u200c', '')
    #os.remove(text_path)
    with open(dic_path, "r", encoding='utf-8') as words_file:
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
            input_words[i] = found_new_word
        else:
            if w.endswith("های") or w.endswith("ها"):
                w = w.replace("های", "")
                w = w.replace("ها", "")
   
            if f"\n{w}\n" not in words_text:
                for j in range(2, len(w)): 
                    new_word = w[0:j]
                    if (f"\n{w[0:j]}\n" in words_text) and (f"\n{w[j:]}\n" in words_text):
                        input_words[i] = w[0:j] + " " + w[j:]
                        break
                    

    output_file_name = f"out_{t}.txt"
    with open(output_file_name, "+w", encoding="utf-8") as output_file:
        output_file.write(" ".join(input_words))

    print("Done in ",(time.time() - t), " seconds")
    return output_file_name, text_path

  
def ocr_pdf(input_pdf):
    t = time.time()
    refined_output_text = ""
    output_text = ""
    doc = pymupdf.open(input_pdf) # open a document
    for page in doc: # iterate the document pages
        pix = page.get_pixmap(dpi=300)
        output_image = f"outfile{t}.png"
        pix.save(output_image)
        refined_text_path, text_path = ocr_image(output_image)
        with open(refined_text_path, "r", encoding="utf-8") as file:
            refined_output_text += "\n\n\n\n\n" + str(file.read())
        with open(text_path, "r", encoding="utf-8") as file:
            output_text += "\n\n\n\n\n" + str(file.read())

        os.remove(refined_text_path)
        os.remove(text_path)
        os.remove(output_image)
    return refined_output_text, output_text

args = sys.argv[1:]
#input_path = args[0]

# refined_text, text = ocr_pdf("input.pdf")
#
# with open("refined_output.txt", "+w", encoding="utf-8") as output_file:
#     output_file.write(refined_text)
# with open("output.txt", "+w", encoding="utf-8") as output_file:
#     output_file.write(text)
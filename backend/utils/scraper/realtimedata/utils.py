def convert_arabic_to_persian(word):
    arabic_letters = "كي"
    persian_letters = "کی"

    for arabic, persian in zip(arabic_letters, persian_letters):
        word = word.replace(arabic, persian)

    return word


def convert_persian_to_arabic(word):
    persian_letters = "کی"
    arabic_letters = "كي"

    for persian, arabic in zip(persian_letters, arabic_letters):
        word = word.replace(persian, arabic)

    return word

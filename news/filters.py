def censor(text):
    forbidden_words = ["badword1", "badword2", "badword3"]  # Замените на список слов, которые вы хотите цензурировать
    replacement = "[censored]"
    for word in forbidden_words:
        text = text.replace(word, replacement)
    return text

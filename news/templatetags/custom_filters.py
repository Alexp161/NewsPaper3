from django import template


register = template.Library()


@register.filter(name='addSmile')
def addSmile(value, arg):
    if isinstance(value, str) and isinstance(arg, int):
        return value + ')'*arg if 'аха' in value else value
    else:
        raise ValueError(f'Нельзя умножиить {value} на {arg}')


@register.filter(name='postwordEnding')
def postwordEnding(postList):
    word = 'пост'
    endings = ['а', 'ов']
    length = len(postList)
    if 11 <= length <= 20 or 5 <= length % 10 <= 9 or length % 10 == 0:
        res = f'{length} {word + endings[1]}'
    elif length % 10 == 1:
        res = f'{length} {word}'
    else:
        res = f'{length} {word + endings[0]}'
    return res


@register.filter(name='censor')
def censor(text):
    negative_words = ['хрен', 'жопа', 'жопе']
    word_list = text.split()
    for i, word in enumerate(word_list):
        for negative in negative_words:
            if negative in word.lower():
                start_ind = word.lower().find(negative)
                end_ind = start_ind + len(negative)
                word_list[i] = word[:start_ind] + 'Х' * len(negative) + word[end_ind:]
    return ' '.join(word_list)


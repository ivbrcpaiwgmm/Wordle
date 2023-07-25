from random import choice
import string
from colorama import init, Fore, Back

# Блок настроек
print('''Это игра "Wordle"! Вам необходимо отгадать слово за отведенное количество попыток.
В классической версии загадывается слово из 5 букв на Английском языке и отводится 6 попыток.''')
init(autoreset=True)
gmode = input('Выберите язык(rus/eng):  ')
letters = int(input('Укажите желаемое количество букв в слове(цифрой от 3 до 9) включительно:  '))
tries = int(input('Укажите желаемое количество попыток(цифрой):  '))

# Блок создания словаря и выбора слова
if gmode == 'eng':
    with open('engwords.txt') as d:
        l = [i.strip().upper() for i in d.readlines() if len(i.strip()) == letters]
    alf = {key: 0 for key in string.ascii_uppercase}
elif gmode == 'rus':
    with open('russian_nouns.txt', encoding='utf-8') as d:
        l = [i.strip().upper() for i in d.readlines() if len(i.strip()) == letters]
    alf = {chr(key): 0 for key in range(ord('А'), ord('Я') + 1)} | {'Ё': 0}
x = choice(l)

# Основная часть. Блок базовых проверок.
spisok = []
while tries > 0:
    move = input('Введите слово:  ').upper()
    if move == 'СДАЮСЬ':
        print(f'Было загадано слово: ', Fore.BLUE + f"'{x}'", end='')
        break
    if move == 'ПОКАЖИ СЛОВАРЬ':
        print(l)
        continue
    if len(move) != letters:
        print(f'Неверное количество букв! Введите слово из {letters} букв.)))')
        continue
    if move not in l:
        print("Слово не найдено. Попробуйте другое слово.")
        continue

    # Блок обработки алфавита.
    for i in range(letters):
        if move[i] == x[i]:
            alf[move[i]] = 3
        if alf[move[i]] != 3 and alf[move[i]] != 1:
            if move[i] in x:
                alf[move[i]] = 2
            else:
                alf[move[i]] = 1

    # Блок обработки слова.
    tries -= 1
    zamenax = x
    mnind = set()
    word = []
    print('\n' * 30)
    for i in range(letters):
        if move[i] == zamenax[i]:
            word.append([move[i], 3, i])
            mnind.add(i)
            zamenax = zamenax.replace(move[i], '^', 1)
    for i in range(letters):
        if i in mnind:
            continue
        if move[i] in zamenax:
            zamenax = zamenax.replace(move[i], '^', 1)
            word.append([move[i], 2, i])
        else:
            word.append([move[i], 1, i])
    spisok.append(sorted(word, key=lambda y: y[2]))

    # Блок вывода слова.
    for i in spisok:
        for bukva in i:
            if bukva[1] == 3:
                print(Back.GREEN + bukva[0], end='')
            elif bukva[1] == 2:
                print(Back.YELLOW + bukva[0], end='')
            elif bukva[1] == 1:
                print(Back.WHITE + bukva[0], end='')
        print()
    print()

    # Блок вывода алфавита.
    for key, value in alf.items():
        if value == 3:
            print(Back.GREEN + key, end=' ')
        elif value == 2:
            print(Back.YELLOW + key, end=' ')
        elif value == 1:
            print(Back.WHITE + key, end=' ')
        elif value == 0:
            print(key, end=' ')
    print()
    print(f'Осталось попыток: {tries}')

    # Блок вывода результата.
    if move == x:
        print('Вы выиграли!', end='')
        break
else:
    print(Fore.RED + 'Вы проиграли. Загадано было слово:', Fore.BLUE + f"'{x}'", end='')

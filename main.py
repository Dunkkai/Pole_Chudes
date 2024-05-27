import math
import random, time
from dicts import prizes, db

class ExpectedError(Exception):
    pass


def switch_player(curr_player, player1, player2):
    if curr_player == player1:
        return player2
    else:
        return player1


def show_result(guessed: dict, word: str) -> str:
    square = "⏹"
    ans = ""
    for i in word:
        if guessed.get(i.lower(), False):
            ans += i
        else:
            ans += square
    return ans


def guess_all_word(guess: str, word: str) -> bool:
    if guess == word:
        return True
    else:
        return False

def prize(player: str) -> int:
    #доделать выход из приза, просто дальше крутить
    des = input("Вам выпал сектор приз, вы хотите участвовать или крутите барабан дальше?\n0-участвовать 1-крутить дальше")
    if des == 0:
        flag = 0
        prizes = ["Ключ от автомобиля", "Телевизор", "Мп3 плеер", "Путевка в Рузаевку",
                  "Тыква", "Ноутбук", "Бутылка водки", "Игрушечна машинка", "Тапочки",
                  "Ничего"]
        print(f"Сектор приз на барабане!")
        your_price = random.choice(prizes)
        x = input(f"{player}, вы выбираете приз или деньги? (три тысячи рублей)\n1-приз 2-деньги\n")
        if x == '1':
            y = input("А если я предложу вам пять тысяч рублей\n1-приз! 2-деньги\n")
            if y == "1":
                z = input("А что вы скажете, если я дам вам семь тысяч?\n1-приз! 2-деньги\n")
                if z == "1":
                    ans = f"Поздравляю, {player}, в качестве приза вы получаете {your_price} и выходите из игры\n"
                    flag = 1
                else:
                    ans = f"{player}, вы получаете семь тысяч рублей!\n"
                    flag = 7000
            else:
                ans = f"{player}, вы получаете пять тысяч рублей!\n"
                flag = 5000
        else:
            ans = f"{player}, вам достается три тысячи рублей!\n"
            flag = 3000
        print(ans)
        return flag
    else:
        return -1

def key(player: str) -> int:
    des = int(input("Вам выпал сектор ключ, вы хотите поучаствовать или хотите играть дальше и  назвать букву?\n0-угадать ключ 1-крутить дальше"))
    if des == 1:
        return -1
    else:
        right_key = random.randint(1, 6)
        choise = int(input("Выберите ключ от 1 до 6"))
        return choise == right_key

def plus(player: str, word: str):
    pos = int(input("напишите какую букву вы хотите открыть"))
    return word[pos - 1].lower()

def wheel_spin(player):
    v = ['П', "+", "Ключ", "Б", "O", "350", "400", "450", "500", "600", "650", "700", "750", "800", "850", "950",
         "1000"]
    spin = random.choice(v)
    return spin

def turn(choise: int) -> bool:
    ans = False
    if choise == 0:  # выбираем букву
        return False
    elif choise == 1:  # угадываем все слово
        return True
    else:
        raise ExpectedError("Ошибка в выборе")
def game(player1: str, player2: str, word: str):
    bank = []
    points = {player1: 0,
              player2: 0,
              }
    guessed = {letter.lower(): False for letter in word}
    current_player = player1
    while not all(guessed.values()):
        print(f"Ход игрока {current_player}")
        print(show_result(guessed, word))
        wheel_spin_res = wheel_spin(current_player)
        if wheel_spin_res.isdigit():
            point = int(wheel_spin_res)
            print(f"{current_player}, вы крутите барабан и вам выпадает {wheel_spin_res}")
            if not turn(int(input("Выберите что вы хотите назвать\n0-букву 1-все слово\n"))):
                letter = input(f"{current_player}, введите букву: ").lower()
                if letter in bank:
                    print(f"{current_player}, эту букву уже называли, нужно быть внимательнее!")
                    switch_player(current_player, player1, player2)
                elif letter in word.lower() and not guessed[letter]:
                    print("Есть такая буква!")
                    guessed[letter] = True
                    bank.append(letter)
                    points[current_player] += point
                else:
                    print(f"Увы, такой буквы нет")
                    bank.append(letter)
                    current_player = switch_player(current_player, player1, player2)
            else:
                print(f"{current_player}, назовите все слово целиком!")
                full_ans = input().lower()
                time.sleep(1)
                print(".")
                time.sleep(1)
                print("..")
                time.sleep(1)
                print("...")
                time.sleep(1)
                if full_ans == word.lower():
                    print(f"абсолюто верно, {current_player}, вы"
                          f" правильно назвали слово и выиграли в нашей игре!")
                    points[current_player] += point
                    points[current_player] += 1000
                    break
                else:
                    print(f'f увы, {current_player}, вы оказались не правы'
                          f'и вы выбываете')
                    current_player = switch_player(current_player, player1, player2)
                    break
        else:
            if wheel_spin_res == 'П':

                g = prize(current_player)
                if g:
                    current_player = switch_player(current_player, player1, player2)
                    points[current_player] += int(g // 10)
                else:
                    current_player = switch_player(current_player, player1, player2)

            elif wheel_spin_res == "+":
                print(f"сектор плюс на барабане!")
                lett = plus(current_player, word)
                guessed[lett] = True
                bank.append(lett)

            elif wheel_spin_res == "Ключ":
                des = key(current_player)
                if des == 1:
                    print(f"{current_player}, поздравляем!\nвы выиграли автобоми-и-и-иль!!!")
                    current_player = switch_player(current_player, player1, player2)
                elif des == 0:
                    print(f"{current_player}, увы ключ не подошел, продолжаем игру")
                    current_player = switch_player(current_player, player1, player2)
                else:
                    pass

            elif wheel_spin_res == "Б":
                print(f'увы, выпал банкрот. Ваши баллы о')
                points[current_player] = 0
                current_player = switch_player(current_player, player1, player2)

            elif wheel_spin_res == 'O':
                print(f"на барабане 0! ход переходит к следующему игроку")
                current_player = switch_player(current_player, player1, player2)

    print(f"Игра окончена! Слово было '{word}', победил игрок {current_player}")
    return current_player, points[current_player]


def game(player1: str, player2: str, word: str) -> tuple:
    bank = []
    points = {player1: 0,
              player2: 0,
              }
    guessed = {letter.lower(): False for letter in word}
    current_player = player1
    while not all(guessed.values()):
        print(f"Ход игрока {current_player}")
        print(show_result(guessed, word))
        wheel_spin_res = wheel_spin(current_player)
        if wheel_spin_res.isdigit():
            point = int(wheel_spin_res)
            print(f"{current_player}, вы крутите барабан и вам выпадает {wheel_spin_res}")
            if not turn(int(input("Выберите что вы хотите назвать\n0-букву 1-все слово\n"))):
                letter = input(f"{current_player}, введите букву: ").lower()
                if letter in bank:
                    print(f"{current_player}, эту букву уже называли, нужно быть внимательнее!")
                    switch_player(current_player, player1, player2)
                elif letter in word.lower() and not guessed[letter]:
                    print("Есть такая буква!")
                    guessed[letter] = True
                    bank.append(letter)
                    points[current_player] += point
                else:
                    print(f"Увы, такой буквы нет")
                    bank.append(letter)
                    current_player = switch_player(current_player, player1, player2)
            else:
                print(f"{current_player}, назовите все слово целиком!")
                full_ans = input().lower()
                time.sleep(1)
                print(".")
                time.sleep(1)
                print("..")
                time.sleep(1)
                print("...")
                time.sleep(1)
                if full_ans == word.lower():
                    print(f"абсолюто верно, {current_player}, вы"
                          f" правильно назвали слово и выиграли в нашей игре!")
                    points[current_player] += point
                    points[current_player] += 1000
                    break

                else:
                    print(f'f увы, {current_player}, вы оказались не правы'
                          f'и вы выбываете')
                    current_player = switch_player(current_player, player1, player2)
                    break
        else:
            if wheel_spin_res == 'П':
                g = prize(current_player)
                if g == 1:
                    current_player = switch_player(current_player, player1, player2)
                    points[current_player] += int(g // 10)
                elif g == -1:
                    print(f"{current_player}, продолжаем игру с вами")
                else:
                    current_player = switch_player(current_player, player1, player2)

            elif wheel_spin_res == "+":
                print(f"сектор плюс на барабане!")
                lett = plus(current_player, word)
                guessed[lett] = True
                bank.append(lett)

            elif wheel_spin_res == "Ключ":
                des = key(current_player)
                if des == 1:
                    print(f"{current_player}, поздравляем!!!\nвы выиграли а-а-автобоми-и-и-иль!!!")
                    current_player = switch_player(current_player, player1, player2)
                elif des == 0:
                    print(f"{current_player}, увы ключ не подошел, продолжаем игру")
                    current_player = switch_player(current_player, player1, player2)
                else:
                    print(f"{current_player}, продолжаем игру с вами")

            elif wheel_spin_res == "Б":
                print(f'увы, выпал банкрот. Ваши баллы обнулены')
                points[current_player] = 0
                current_player = switch_player(current_player, player1, player2)

            elif wheel_spin_res == 'O':
                print(f"на барабане 0! ход переходит к следующему игроку")
                current_player = switch_player(current_player, player1, player2)

    print(f"Игра окончена! Слово было '{word}', победил игрок {current_player}")
    return current_player, points[current_player]


def super_game(player, word) -> None:
    bank = []
    letters_to_open = math.ceil(len(word) / 4)
    print(f"{player}, вы можете назвать {letters_to_open} букв и мы покажем их если они есть!")
    guessed = {letter.lower(): False for letter in word}
    print(show_result(guessed, word))
    for i in range(letters_to_open):
        lettter = input("Назовите букву\n")
        if lettter in word.lower() and not guessed[lettter]:
            print("Есть такая буква!")
            guessed[lettter] = True
            bank.append(lettter)
            print(show_result(guessed, word))
        else:
            print("Нет такой буквы")
            print(show_result(guessed, word))
    answer = input(f"{player}, вы назвали все буквы, очень хорошо подумайте и напишите слово\n").lower()
    time.sleep(1)
    print('.')
    time.sleep(2)
    print('..')
    time.sleep(3)
    print('...')
    if answer == word.lower():
        print(f"{player}, и это правильный ответ!!! вы выиграли в нашей суперигре")
    else:
        print(f"{player}, увы это неверный ответ, вы потеряли все призы =(")


def main() ->None:
    player1 = input("Введите имя игрока 1\n")
    player2 = input("Введите имя игрока 2\n")

    keys = list(db.keys())
    x = (random.choice(keys))
    print(db[x])

    winner, points = game(player1, player2, x)
    print(winner)
    print(points)
    time.sleep(2)
    print(f'{winner}, выберите призы из предложенныx:\n')
    for prize, value in prizes.items():
        print(f"{prize} - {value}")

    selected_prizes = []

    while points >= 300:
        choice = int(input(f"Выберите номер вашего приза, оставшиеся очки: {points}\n"))
        if choice in prizes and prizes[choice][1] <= points:
            points -= prizes[choice][1]
            selected_prizes.append(prizes[choice][0])
        else:
            print("ошибка выбора")

    solution = int(input((f"{winner}, еще раз поздравляем вас с победой!\nНа данный момент у вас есть {', '.join(selected_prizes)}\n вы хотите сыграть в супер игру?\n1-да 2-нет\n")))
    y = random.choice(keys)
    while y == x:
        y = random.choice(keys)

    print(db[y])
    super_game(winner, y)

if __name__ == "__main__":
    main()
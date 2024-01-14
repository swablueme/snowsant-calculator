class Colors:
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    GREY = "\033[90m"


HELLO = r"""
   _____                                     _    
  / ____|                                   | |   
 | (___  _ __   _____      _____  __ _ _ __ | |_  
  \___ \| '_ \ / _ \ \ /\ / / __|/ _` | '_ \| __| 
  ____) | | | | (_) \ V  V /\__ \ (_| | | | | |_  
 |_____/|_| |_|\___/ \_/\_/ |___/\__,_|_| |_|\__| 
    _____      _            _       _             
  / ____|    | |          | |     | |            
 | |     __ _| | ___ _   _| | __ _| |_ ___  _ __ 
 | |    / _` | |/ __| | | | |/ _` | __/ _ \| '__|
 | |___| (_| | | (__| |_| | | (_| | || (_) | |   
  \_____\__,_|_|\___|\__,_|_|\__,_|\__\___/|_|   

"""

ALERT = r"""
=============================================================
|                                                           |
|  If you encounter Connection closed upon startup,         |
|        you can try again later                            |
|                                                           |
============================================================="""

# print(Colors.RED + ALERT + Colors.RESET)
print(Colors.CYAN + HELLO + Colors.RESET)


def input_int(prompt, valid=None):
    while True:
        try:
            value = int(input(prompt))
            if isinstance(valid, (range, list)):
                valid = tuple(valid)
            if isinstance(valid, tuple):
                assert value in valid, f"[!] The entered value is not within the legal range：{valid}"
            if isinstance(valid, int):
                assert value % valid == 0, f"[!] The entered value needs to be a multiple of {valid}"
            return value
        except AssertionError as e:
            print(Colors.RED + str(e) + Colors.RESET)
        except Exception:
            print(Colors.RED +
                  "[!] Incorrect input, please re-enter。" + Colors.RESET)


def input_ints(prompt, nums, sum_to):
    while True:
        try:
            values = tuple(map(int, input(prompt).strip().split(" ")))
            assert len(
                values) == nums, f"[!] The number entered is incorrect, please re-enter."
            assert sum(
                values) == sum_to, f"[!] The total purchase quantity does not match the customer quantity, please re-enter"
            return values
        except AssertionError as e:
            print(Colors.RED + str(e) + Colors.RESET)
        except Exception:
            print(Colors.RED +
                  "[!] Incorrect input, please re-enter" + Colors.RESET)


good_stage = input_int(
    "[*] Which stage of the product is the product being sold today？(1-4) ", range(1, 5))

if good_stage == 1:
    buy_drink = [20, 28, 38]
    buy_snack = [10, 20, 32]
    buy_token = [50, 100, 200]
    sell_base_drink = 50
    sell_base_snack = 40
    sell_base_token = 1000

elif good_stage == 2:
    buy_drink = [30, 42, 57]
    buy_snack = [15, 30, 48]
    buy_token = [50, 100, 200]
    sell_base_drink = 100
    sell_base_snack = 80
    sell_base_token = 1000

elif good_stage == 3:
    buy_drink = [40, 56, 76]
    buy_snack = [20, 40, 64]
    buy_token = [50, 100, 200]
    sell_base_drink = 200
    sell_base_snack = 160
    sell_base_token = 1000

elif good_stage == 4:
    buy_drink = [50, 70, 95]
    buy_snack = [25, 50, 80]
    buy_token = [50, 100, 200]
    sell_base_drink = 250
    sell_base_snack = 200
    sell_base_token = 1000

customer_drink = input_int("[*] How many drink lovers are there today?", 90)
customer_snack = input_int("[*] How many meal lovers are there today?", 90)
customer_token = input_int("[*] How many souvenir lovers are there today?", 10)
customer = [customer_drink, customer_snack, customer_token]
buy_prices = [buy_drink, buy_snack, buy_token]
stock_drink = customer_drink
stock_snack = customer_snack
stock_token = customer_token

remain_me = input_int(
    "[*] How much souvenir inventory does Snow Pheasant Store have (just fill in 0 if you don't know)？")
remain_rival = input_int(
    "[*] How much souvenir inventory does Time Store have (if you don't know, just fill in 0)?")
remain_strategy = input_int(
    "[*] Is it allowed to exchange less current day income for more expected future income? It takes longer to calculate. 0 means no, 1 means yes (0/1)", (0, 1))
if remain_strategy:
    print(Colors.RED +
          "[!] Please note that subsequent expected returns include possible future returns on souvenir inventory." + Colors.RESET)

# aaa = (30, 30, 30)
# aab = (36, 36, 18)
# abb = (36, 27, 27)
# abc = (40, 30, 20)
# aa = (5, 5)
# ab = (6, 4)

sell_drink = list(range(sell_base_drink - 5, sell_base_drink + 6, 1))
sell_snack = list(range(sell_base_snack - 5, sell_base_snack + 6, 1))
sell_token = list(range(sell_base_token - 50, sell_base_token + 51, 10))
sell = [sell_drink, sell_snack, sell_token]

# ============================================================


from itertools import product


def average_with_weight(pairs):
    return sum([x[0] * x[-1] for x in pairs]) / sum([x[-1] for x in pairs])


# ============================================================


import datetime

end_time = datetime.datetime(2023, 8, 22, 4, 0)
now_time = datetime.datetime.now()
countdown = (end_time - now_time).days + 1


future_token_sell_cache = {}


def future_token_sell(day, stock):
    if day == 0:
        return 0
    if (day, stock) in future_token_sell_cache:
        return future_token_sell_cache[(day, stock)]
    unit = min(stock_token // 10 + (countdown - day), 14)
    my_stock, rival_stock = stock
    __value = []
    for rival_price in range(11):
        __best_action = -1e9
        for my_price in range(11):
            if my_price > rival_price:
                ratio = (4, 6)
            elif my_price == rival_price:
                ratio = (5, 5)
            elif my_price < rival_price:
                ratio = (6, 4)
            my_sold = min(my_stock, unit * ratio[0])
            rival_sold = min(rival_stock, unit * ratio[1])
            my_income = sell_token[my_price] * my_sold
            rival_income = sell_token[rival_price] * rival_sold
            my_income += 5000 if my_income >= rival_income else 2000
            __best_action = max(
                __best_action,
                future_token_value(
                    day - 1, (my_stock - my_sold, rival_stock - rival_sold)
                )
                + my_income,
            )
        __value.append(__best_action)
    __value = sum(__value) / len(__value)

    future_token_sell_cache[(day, stock)] = __value
    return __value


future_token_value_cache = {}


def future_token_value(day, stock):
    if day == 0:
        return 0
    if (day, stock) in future_token_value_cache:
        return future_token_value_cache[(day, stock)]
    unit = min(stock_token // 10 + (countdown - day), 14)
    my_stock, rival_stock = stock
    __value = []
    for rival_strategy in range(3):
        __best_action = -1e9
        for my_strategy in range(3):
            if my_strategy > rival_strategy:
                ratio = (6, 4)
            elif my_strategy == rival_strategy:
                ratio = (5, 5)
            elif my_strategy < rival_strategy:
                ratio = (4, 6)
            __best_action = max(
                __best_action,
                future_token_sell(
                    day, (my_stock + unit * ratio[0],
                          rival_stock + unit * ratio[1])
                )
                - buy_token[my_strategy] * unit * ratio[0],
            )
        __value.append(__best_action)
    __value = sum(__value) / len(__value)

    future_token_value_cache[(day, stock)] = __value
    return __value


def future_value_exp(day, stock):
    if stock[0] == 0:
        return 0
    return future_token_value(day, stock) - future_token_value(day, (0, stock[1]))


# ============================================================

sell_result_cache = {}


def sell_result(bid, me) -> int:
    if (bid, me) in sell_result_cache:
        return sell_result_cache[(bid, me)]
    ranks = [sum([1 for y in bid if y < x]) for x in bid]
    sorted_ranks = sorted(ranks)
    if sorted_ranks == [0, 0, 0]:
        ret = 30
    elif sorted_ranks == [0, 0, 2]:
        ret = [36, None, 18][ranks[bid.index(me)]]
    elif sorted_ranks == [0, 1, 1]:
        ret = [36, 27][ranks[bid.index(me)]]
    elif sorted_ranks == [0, 1, 2]:
        ret = [40, 30, 20][ranks[bid.index(me)]]
    elif sorted_ranks == [0, 0]:
        ret = 5
    elif sorted_ranks == [0, 1]:
        ret = [6, 4][ranks[bid.index(me)]]
    else:
        raise NotImplementedError
    sell_result_cache[(bid, me)] = ret
    return ret


def sell_conflict_checker(statement, info) -> bool:
    if len(info) == 0:
        return True
    if len(info) == 1:
        return info == statement
    if len(info) == 2:
        if info == (None, None):
            return True
        elif None not in info:
            return info == statement
        elif info[0] == None:
            return info[1] == statement[1] and info[1] >= statement[0]
        elif info[1] == None:
            return info[0] == statement[0] and info[0] >= statement[1]
        else:
            raise NotImplementedError
    return False


sell_action_cache = {}


def sell_action(gid, num, rival_num, info):
    num += remain_me * (gid == 2)

    if (gid, num, rival_num, info) in sell_action_cache:
        return sell_action_cache[(gid, num, rival_num, info)]

    # print(num, rival_num, info, gid)
    statements = [
        statement
        for statement in product(range(11), repeat=[2, 2, 1][gid])
        if sell_conflict_checker(statement, info)
    ]

    best_income, best_choice = -1e9, None
    for c in range(11):
        incomes = []
        sameprice = None
        for statement in statements:
            customer_base = customer[gid] // [90, 90, 10][gid]
            customer_num = customer_base * sell_result(statement + (c,), c)
            my_sold = min(customer_num, num)
            income = my_sold * sell[gid][c]
            income_rank = 0
            for _c, _n in zip(statement, rival_num):
                _n += remain_rival * (gid == 2)
                rival_customer_num = customer_base * \
                    sell_result(statement + (c,), _c)
                rival_sold = min(rival_customer_num, _n)
                rival_income = rival_sold * sell[gid][_c]
                if rival_income > income:
                    income_rank += 1
            # print(c, statement + (c,), sell_result(statement + (c,), c), sell[gid][c], income, income_rank)
            if income_rank == 0:
                income += 5000
            elif income_rank == 1:
                income += 2000
            else:
                income += 1000
            if remain_strategy and gid == 2:
                income += future_value_exp(
                    countdown - 1, (num - my_sold, rival_num[0] - rival_sold)
                )
            incomes.append(income)
            if len(info) == 2 and None in info and statement[0] == statement[1]:
                sameprice = income
        if sameprice is not None:
            exp_income = (sum(incomes) - 0.5 * sameprice) / \
                (len(incomes) - 0.5)
        else:
            exp_income = sum(incomes) / len(incomes)
        # print(c, incomes, sameprice, exp_income)
        if exp_income > best_income:
            best_income, best_choice = exp_income, (c,)

    # print(gid, info, best_income, best_choice, statements)
    sell_action_cache[(gid, num, rival_num, info)] = (best_income, best_choice)
    return best_income, best_choice


sell_stage_cache = {}


def sell_stage(clues, gid, nums, rival_nums, info):
    if gid == 3:
        return -clues, -1, None
    if (clues, gid, nums[gid:], rival_nums[gid:], info) in sell_stage_cache:
        return sell_stage_cache[(clues, gid, nums[gid:], rival_nums[gid:], info)]

    best_income, best_choice = sell_action(
        gid, nums[gid], rival_nums[gid], info)
    best_income += sell_stage(clues, gid + 1, nums, rival_nums, ())[0]

    if clues:
        if info == ():
            if gid != 2:
                pry_income = average_with_weight(
                    [
                        sell_stage(clues - 1, gid, nums, rival_nums, (i, None))
                        for i in range(11)
                    ]
                    + [
                        sell_stage(clues - 1, gid, nums, rival_nums, (None, i))
                        for i in range(11)
                    ]
                )
                if pry_income > best_income:
                    best_income, best_choice = pry_income, -1
            else:
                pry_income = average_with_weight(
                    [
                        sell_stage(clues - 1, gid, nums, rival_nums, (i,))
                        for i in range(11)
                    ]
                )
                if pry_income > best_income:
                    best_income, best_choice = pry_income, -1
        elif None in info:
            __idx = 1 - info.index(None)
            pry_income = average_with_weight(
                [
                    sell_stage(
                        clues - 1,
                        gid,
                        nums,
                        rival_nums,
                        (i, info[1]) if __idx == 1 else (info[0], i),
                    )
                    for i in range(info[__idx] + 1)
                ]
            )
            if pry_income > best_income:
                best_income, best_choice = pry_income, -1

    statements = [
        statement
        for statement in product(range(11), repeat=[2, 2, 1][gid])
        if sell_conflict_checker(statement, info)
    ]

    statements_num = len(statements)
    if len(info) == 2 and None in info:
        statements_num -= 0.5

    sell_stage_cache[(clues, gid, nums[gid:], rival_nums[gid:], info)] = (
        best_income,
        best_choice,
        statements_num,
    )
    return best_income, best_choice, statements_num


# ============================================================


buy_result_cache = {}


def buy_result(bid, me):
    if (bid, me) in buy_result_cache:
        return buy_result_cache[(bid, me)]
    ranks = [sum([1 for y in bid if y > x]) for x in bid]
    sorted_ranks = sorted(ranks)
    if sorted_ranks == [0, 0, 0]:
        ret = 30
    elif sorted_ranks == [0, 0, 2]:
        ret = [36, None, 18][ranks[bid.index(me)]]
    elif sorted_ranks == [0, 1, 1]:
        ret = [36, 27][ranks[bid.index(me)]]
    elif sorted_ranks == [0, 1, 2]:
        ret = [40, 30, 20][ranks[bid.index(me)]]
    elif sorted_ranks == [0, 0]:
        ret = 5
    elif sorted_ranks == [0, 1]:
        ret = [6, 4][ranks[bid.index(me)]]
    else:
        raise NotImplementedError
    buy_result_cache[(bid, me)] = ret
    return ret


def buy_conflict_checker(statement, info):
    if len(info) == 0 or statement == info:
        return True
    if len(info) == 1:
        return info[0] == statement[0]
    return False


def buy_action(clues, infos):
    statements = [
        statement
        for statement in product(range(3), repeat=5)
        if buy_conflict_checker(statement[0:2], infos[0])
        and buy_conflict_checker(statement[2:4], infos[1])
        and buy_conflict_checker(statement[4:5], infos[2])
    ]

    if len(statements) == 0:
        print(clues, infos)

    best_income, best_choice = -1e9, None
    for c in product(range(3), repeat=3):
        incomes = []
        for statement in statements:
            drink_nums = stock_drink // 90 * \
                buy_result(statement[0:2] + (c[0],), c[0])
            snack_nums = stock_snack // 90 * \
                buy_result(statement[2:4] + (c[1],), c[1])
            token_nums = stock_token // 10 * \
                buy_result(statement[4:5] + (c[2],), c[2])
            costs = (
                drink_nums * buy_drink[c[0]]
                + snack_nums * buy_snack[c[1]]
                + token_nums * buy_token[c[2]]
            )
            nums = (drink_nums, snack_nums, token_nums)
            __sd = stock_drink // 90
            __ss = stock_snack // 90
            __st = stock_token // 10
            rival_nums = (
                (
                    __sd * buy_result(statement[0:2] + (c[0],), statement[0]),
                    __sd * buy_result(statement[0:2] + (c[0],), statement[1]),
                ),
                (
                    __ss * buy_result(statement[2:4] + (c[1],), statement[2]),
                    __ss * buy_result(statement[2:4] + (c[1],), statement[3]),
                ),
                (__st * buy_result(statement[4:5] + (c[2],), statement[4]),),
            )
            sell_income = sell_stage(clues, 0, nums, rival_nums, ())[0]
            incomes.append(sell_income - costs)
        exp_income = sum(incomes) / len(incomes)
        if exp_income > best_income:
            best_income, best_choice = exp_income, c
    return best_income, best_choice


buy_stage_cache = {}


def buy_stage(clues, infos):
    if (clues, infos) in buy_stage_cache:
        return buy_stage_cache[(clues, infos)]

    best_income, best_choice = buy_action(clues, infos)

    if clues:
        if len(infos[0]) < 2:
            pry_income = average_with_weight(
                [
                    buy_stage(clues - 1, (infos[0] + (i,), infos[1], infos[2]))
                    for i in range(3)
                ]
            )
            if pry_income > best_income:
                best_income, best_choice = pry_income, 0

        if len(infos[1]) < 2:
            pry_income = average_with_weight(
                [
                    buy_stage(clues - 1, (infos[0], infos[1] + (i,), infos[2]))
                    for i in range(3)
                ]
            )
            if pry_income > best_income:
                best_income, best_choice = pry_income, 1

        if len(infos[2]) < 1:
            pry_income = average_with_weight(
                [
                    buy_stage(clues - 1, (infos[0], infos[1], infos[2] + (i,)))
                    for i in range(3)
                ]
            )
            if pry_income > best_income:
                best_income, best_choice = pry_income, 2

    statements = [
        statement
        for statement in product(range(3), repeat=5)
        if buy_conflict_checker(statement[0:2], infos[0])
        and buy_conflict_checker(statement[2:4], infos[1])
        and buy_conflict_checker(statement[4:5], infos[2])
    ]

    buy_stage_cache[(clues, infos)] = (
        best_income, best_choice, len(statements))
    return (best_income, best_choice, len(statements))


# ============================================================

import sys


def action_confirm():
    input(Colors.GREY +
          "Press the Enter key after the action is completed..." + Colors.RESET)
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")


clues = input_int(
    "[*] Please enter the number of times you can find out：", (4, 5, 6))
infos = ((), (), ())
print("Please wait, calculation is in progress...")
while True:
    ret = buy_stage(clues, infos)
    print(Colors.GREEN +
          f"[+] The current expected return is：{ret[0]}" + Colors.RESET)
    if isinstance(ret[1], int):
        goods = ["Drinks", "Meals", "Souvenirs"][ret[1]]
        print(Colors.YELLOW +
              f"[A] Please inquire about {goods} (select the first unexplored store from top to bottom)" + Colors.RESET)
        action_confirm()
        choice = input_int(
            "[*] What is the store's purchasing strategy? 1 conservative, 2 steady, 3 aggressive (1-3)", range(1, 4))
        infos = list(infos)
        infos[ret[1]] = infos[ret[1]] + (choice - 1,)
        infos = tuple(infos)
        clues -= 1
    else:
        strategy = [["conservative", "robust", "aggressive"][ret[1][i]]
                    for i in range(3)]
        print(Colors.YELLOW + "[A] The purchase strategy has been determined:" +
              "，".join(strategy) + Colors.RESET)
        action_confirm()
        break

print("[+] Please tell us the purchase quantity of each product, separated by spaces between stores.")
print("[+] Note that the order of the store needs to be a specific order, not the order on the purchase quantity ranking list.")

drink = input_ints(
    "[*] Drink purchase quantity (the three numbers in order are Snow Pheasant Store, Cocktail Store, Time Store, separated by spaces):", 3, customer_drink)
snack = input_ints(
    "[*] Meal purchase quantity (the three numbers in order are Snow Pheasant Store, Ice Cream Store, Time Store, separated by spaces):", 3, customer_snack)
token = input_ints(
    "[*] Purchase quantity of souvenirs (the two numbers in order are Snow Pheasant Store and Time Store, separated by spaces)", 2, customer_token)

nums = (drink[0], snack[0], token[0])
rival_nums = (drink[1:], snack[1:], token[1:])

cost = sum([nums[i] * buy_prices[i][ret[1][i]] for i in range(3)])
income = 0

print("Drink sales stage.")
info = ()
while True:
    ret = sell_stage(clues, 0, nums, rival_nums, info)
    print(Colors.GREEN +
          f"[+] The current expected income is: {ret[0] - cost + income}" + Colors.RESET)
    if isinstance(ret[1], int):
        print(Colors.YELLOW +
              f"[A] Please conduct a message inquiry." + Colors.RESET)
        action_confirm()
        rival = input_int(
            "[*] Which store did you get information about? 1 is a cocktail store, 2 is a time store (1-2)", (1, 2))
        price = input_int(
            "[*] What is the selling price they gave?", sell_drink)
        price_idx = list(sell_drink).index(price)
        if info == ():
            info = (None, None)
        info = list(info)
        info[rival - 1] = price_idx
        info = tuple(info)
        clues -= 1
    else:
        price = sell_drink[ret[1][0]]
        print(Colors.YELLOW +
              f"[A] The beverage sales strategy has been determined. Please set the price to: {price}" + Colors.RESET)
        action_confirm()
        break
income += input_int(
    "[*] Please enter the income from beverage sales (including incentive rewards):")


print("Meal sales stage。")
info = ()
while True:
    ret = sell_stage(clues, 1, nums, rival_nums, info)
    print(Colors.GREEN +
          f"[+] The current expected income is:：{ret[0] - cost + income}" + Colors.RESET)
    if isinstance(ret[1], int):
        print(Colors.YELLOW +
              f"[A] Please conduct a message inquiry." + Colors.RESET)
        action_confirm()
        rival = input_int(
            "[*] Which store did you get information about? 1 is the ice cream store, 2 is the time store (1-2) ", (1, 2))
        price = input_int(
            "[*] What is the selling price they gave?", sell_snack)
        price_idx = list(sell_snack).index(price)
        if info == ():
            info = (None, None)
        info = list(info)
        info[rival - 1] = price_idx
        info = tuple(info)
        clues -= 1
    else:
        price = sell_snack[ret[1][0]]
        print(Colors.YELLOW +
              f"[A] The food sales strategy has been determined. Please set the price to: {price}" + Colors.RESET)
        action_confirm()
        break
income += input_int("[*] Please enter the income from meal sales (including incentive rewards):")


print("Souvenir sales stage。")
info = ()
while True:
    ret = sell_stage(clues, 2, nums, rival_nums, info)
    print(Colors.GREEN +
          f"[+] The current expected income is:{ret[0] - cost + income}" + Colors.RESET)
    if isinstance(ret[1], int):
        print(Colors.YELLOW +
              f"[A] Please conduct a message inquiry." + Colors.RESET)
        action_confirm()
        price = input_int(
            "[*] What is the selling price given by Time Store?", sell_token)
        price_idx = list(sell_token).index(price)
        info = (price_idx,)
        clues -= 1
    else:
        price = sell_token[ret[1][0]]
        print(Colors.YELLOW +
              f"[A] The souvenir sales strategy has been determined. Please set the price as: {price}" + Colors.RESET)
        action_confirm()
        break
income += input_int(
    "[*] Please enter the income from souvenir sales (including incentive rewards):")

sold_token_me = input_int(
    "[*] Please enter the quantity of souvenirs sold in the Snow Pheasant Shop:")
sold_token_rival = input_int(
    "[*] Please enter the quantity of souvenirs sold in Time Shop:")
new_remain_me = remain_me + nums[-1] - sold_token_me
new_remain_rival = remain_rival + rival_nums[-1][-1] - sold_token_rival
print(Colors.GREEN +
      f"[+] The souvenir inventory of Snow Pheasant Shop is:{new_remain_me}" + Colors.RESET)
print(Colors.GREEN +
      f"[+] The souvenir inventory of Time Store is：{new_remain_rival}" + Colors.RESET)
if new_remain_rival < 0:
    print(Colors.RED + f"[!]It seems that Time Store had it in stock before! It doesn't matter, they most likely have it out of stock now =v=" + Colors.RESET)
print("Please record the above information")

print("Finally...")

print(Colors.GREEN +
      f"[+] The actual income is：{income - cost}" + Colors.RESET)
if new_remain_me:
    future_value = future_value_exp(
        countdown - 1, (new_remain_me, new_remain_rival))
    print(Colors.GREEN +
          f"[+] The future expected return of the inventory is：{future_value}" + Colors.RESET)

print("It's over！")
action_confirm()

from rdutil.rditem import *


DATA = RDs()


def print_c(string):
    print(MENU_ITEM_FORMAT.format(string))


def printf(fmt, *args):
    print(fmt.format(*args))


def modify_rd():
    series = int(input(MENU_ITEM_FORMAT.format("Select series : ")))
    series_rd = DATA.get_top_r(select_all=True, select_series=series)
    print_c("Select id from following items")
    for i in series_rd:
        printf(RD_FORMAT_WITH_ID, str(i.rid), str(i))
    choice = int(input(MENU_ITEM_FORMAT.format("Choice : ")))
    rd_item = DATA.get_r(choice)
    print_c(f"Selected RD item with id : {choice}")
    print(RD_HEADER)
    print(str(rd_item))
    print_c("S : Series\nD : Date\nA : Amount\nT : Tenure")
    modify = str(input(MENU_ITEM_FORMAT.format("Enter first letter of property to modify :"))).upper()
    val = None
    if modify == 'S':
        val = input(MENU_ITEM_FORMAT.format("Series : "))
    elif modify == 'D':
        val = list(map(int, input(MENU_ITEM_FORMAT.format("Date ( DD MM YYYY ) : ")).split(" ")))
        val = datetime(val[2], val[1], val[0])
    elif modify == 'A':
        val = int(MENU_ITEM_FORMAT.format(input("Amount : ")))
    elif modify == 'T':
        val = int(input(MENU_ITEM_FORMAT.format("Tenure : ")))
    print(DATA.modify_r(r_id=choice, param=modify, val=val))


def print_menu():
    for choice in range(0, len(MENU), 2):
        print(COMPACT_MENU_ITEM.format(f"{choice+1}. {MENU[choice]}", f"{choice+2}. {MENU[choice+1]}"))
    print(SEPARATOR)
    return int(input(MENU_ITEM_FORMAT.format("Enter your choice here : ")))


def add_new_entry():
    series = int(input(MENU_ITEM_FORMAT.format("Series : ")))
    if series in DATA.s_list:
        print(MENU_ITEM_FORMAT.format("Series exists, using existing Amount and tenure"))
        amount = DATA.s_list[series].r_list[0].amount
        tenure = DATA.s_list[series].r_list[0].tenure
    else:
        amount = int(input(MENU_ITEM_FORMAT.format("Amount : ")))
        tenure = int(input(MENU_ITEM_FORMAT.format("Tenure : ")))
    date = list(map(int, input(MENU_ITEM_FORMAT.format("Date ( DD MM YYYY ) : ")).split(" ")))
    date = datetime(date[2], date[1], date[0])
    DATA.add_r(series=series, amount=amount, start=date, tenure=tenure)
    print_c("Entry added.")


def print_r(select_all=False, select_series=None):
    print(RD_HEADER)
    for i in DATA.get_top_r(select_all=select_all, select_series=select_series):
        print(str(i))
    print(SEPARATOR)


def print_all_diff():
    for series in DATA.s_list:
        print(MENU_ITEM_FORMAT.format(f"Series Number : {series}"))
        print_r(select_series=series, select_all=True)


def run_main():
    while 1:
        choice = print_menu()
        print(SEPARATOR)
        if choice == CHOICE_QUIT:
            try:
                warn = int(input(MENU_ITEM_FORMAT.format("Are you sure? 0/1 : ")))
                if warn == 1:
                    break
            except ValueError:
                continue
        elif choice == CHOICE_SCHEDULED:
            DATA.recommend_r()
        elif choice == CHOICE_ADD:
            add_new_entry()
            print_r()
        elif choice == CHOICE_SERIES:
            s = int(input(MENU_ITEM_FORMAT.format("Select series : ")))
            print_r(True, s)
        elif choice == CHOICE_VIEW:
            print_c("Premium dates : ")
            DATA.upcoming_prem()
        elif choice == CHOICE_ALL:
            print_all_diff()
        elif choice == CHOICE_CLOSING_SOON:
            print_c("Closing soon : ")
            print_r()
        elif choice == CHOICE_MODIFY:
            modify_rd()


run_main()

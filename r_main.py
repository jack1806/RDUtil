from rdutil.rditem import *


DATA = RDs()


def print_menu():
    for choice in range(len(MENU)):
        print(MENU_ITEM_FORMAT.format(f"{choice+1}. {MENU[choice]}"))
    return int(input(MENU_ITEM_FORMAT.format("Enter your choice here : ")))


def add_new_entry():
    series = input(MENU_ITEM_FORMAT.format("Series : "))
    amount = int(MENU_ITEM_FORMAT.format(input("Amount : ")))
    date = list(map(int, input(MENU_ITEM_FORMAT.format("Date ( DD MM YYYY ) : ").split(" "))))
    date = datetime(date[2], date[1], date[0])
    tenure = int(input(MENU_ITEM_FORMAT.format("Tenure : ")))
    DATA.add_r(series=series, amount=amount, start=date, tenure=tenure)
    print("Entry added.")


def print_r(select_all=False, select_series=None):
    print(RD_HEADER)
    for i in DATA.get_top_r(select_all=select_all, select_series=select_series):
        print(str(i))
    print(SEPARATOR)


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
            print(MENU_ITEM_FORMAT.format("Premium dates : "))
            DATA.upcoming_prem()
        elif choice == CHOICE_ALL:
            print_r(select_all=True)
        elif choice == CHOICE_CLOSING_SOON:
            print(MENU_ITEM_FORMAT.format("Closing soon : "))
            print_r()


run_main()

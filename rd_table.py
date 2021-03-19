import csv
import datetime
from dateutil.relativedelta import relativedelta

TOP_NUMBER = 6
FILE_NAME = "rd_data.rdx"
ID = 0
DATE = 1
TENURE = 2
SERIES = 3
AMOUNT = 4
MATURITY = 5
STATUS = 6
DATA = {}
COLUMN_NAMES = ['id', 'date', 'tenure', 'series', 'amount', 'maturity', 'status']
MENU = ['View Upcoming', 'Select series', 'Add new', 'Exit']
CHOICE_VIEW = 1
CHOICE_SERIES = 2
CHOICE_ADD = 3
CHOICE_QUIT = 4
TODAY = datetime.datetime.now()
STATUS_OPEN = "Open"
STATUS_CLOSED = "Closed"


def load_data():
    with open(FILE_NAME) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            row_data = {}
            for value in COLUMN_NAMES:
                row_data[value] = row[value]
            DATA[int(row_data['id'])] = row_data


def write_data():
    with open(FILE_NAME, mode='w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=COLUMN_NAMES)
        csv_writer.writeheader()
        for rid in DATA:
            csv_writer.writerow(DATA[rid])


def print_menu():
    for choice in range(len(MENU)):
        print(f"{choice+1}. {MENU[choice]}")
    return int(input("-----> User choice : "))


def add_new_entry():
    series = input("Series : ")
    amount = int(input("Amount : "))
    date = list(map(int, input("Date ( DD MM YYYY ) : ").split(" ")))
    date = datetime.datetime(date[2], date[1], date[0])
    tenure = int(input("Tenure : ")) + 1
    maturity = date + relativedelta(months=tenure)
    status = STATUS_OPEN
    if maturity.timestamp() <= TODAY.timestamp():
        status = STATUS_CLOSED
    rid = len(DATA)
    DATA[rid] = {
        COLUMN_NAMES[ID]: rid,
        COLUMN_NAMES[SERIES]: series,
        COLUMN_NAMES[AMOUNT]: amount,
        COLUMN_NAMES[DATE]: date.timestamp(),
        COLUMN_NAMES[STATUS]: status,
        COLUMN_NAMES[TENURE]: tenure,
        COLUMN_NAMES[MATURITY]: maturity.timestamp()
    }
    write_data()
    print("Entry added.")
    print("Printing summary now")


def print_summary():
    time_remain_data = {}
    for rid in DATA:
        data = DATA[rid]
        if data[COLUMN_NAMES[STATUS]] == STATUS_OPEN:
            time_remain_data[float(data[COLUMN_NAMES[MATURITY]]) - TODAY.timestamp()] = data
    remain_times = sorted(time_remain_data.keys())
    for i in range(min(TOP_NUMBER, len(remain_times))):
        print_rdata(int(time_remain_data[remain_times[i]][COLUMN_NAMES[ID]]))


def print_rdata(rid):
    print(f" --> {DATA[rid][COLUMN_NAMES[SERIES]]} | "
          f"{str(datetime.datetime.fromtimestamp(float(DATA[rid][COLUMN_NAMES[DATE]]))).split(' ')[0]} | "
          f"{str(datetime.datetime.fromtimestamp(float(DATA[rid][COLUMN_NAMES[MATURITY]]))).split(' ')[0]} | "
          f"{DATA[rid][COLUMN_NAMES[AMOUNT]]} | {DATA[rid][COLUMN_NAMES[TENURE]]}")


def print_series():
    series_data = {}
    for rid in DATA:
        rdata = DATA[rid]
        if rdata[COLUMN_NAMES[SERIES]] in series_data:
            series_data[rdata[COLUMN_NAMES[SERIES]]].append(rdata)
        else:
            series_data[rdata[COLUMN_NAMES][SERIES]] = [rdata]
    print("All Series ")


def run_main():
    load_data()
    while 1:
        choice = print_menu()
        if choice == CHOICE_QUIT:
            warn = int(input("Are you sure? 0/1"))
            if warn == 1:
                break
        elif choice == CHOICE_ADD:
            add_new_entry()
            print_summary()
        elif choice == CHOICE_VIEW:
            print_summary()
        elif choice == CHOICE_SERIES:
            print_series()


run_main()

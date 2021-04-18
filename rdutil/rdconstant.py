TOP_NUMBER = 3
FILE_NAME = "rd_data.rdx"
MENU = ['Scheduled', 'Modify', 'View Upcoming', 'Select series', 'Add new', 'View all', 'View closing soon', 'Exit']
CHOICE_SCHEDULED = 1
CHOICE_MODIFY = 2
CHOICE_VIEW = 3
CHOICE_SERIES = 4
CHOICE_ADD = 5
CHOICE_ALL = 6
CHOICE_CLOSING_SOON = 7
CHOICE_QUIT = 8
STATUS_OPEN = "Open"
STATUS_CLOSED = "Closed"
PREMIUM_FORMAT = " "*1+"{:^10s}{:^15s}{:^10s}{:^15s}"
PREMIUM_HEADER = PREMIUM_FORMAT.format('Series', 'Date', 'Amount', 'Breaking')
MENU_ITEM_FORMAT = " "*1+"{:30s}"
COMPACT_MENU_ITEM = " "*1+"{:30s}"+" "*5+"{:30s}"
RD_HEADER_FORMAT = " "*1+"{:^8s}{:^14s}{:^14s}{:^8s}{:^8s}{:^8s}"
RD_FORMAT_WITH_ID = " "*1+"{:^10s}{:^50s}"
RD_HEADER = RD_HEADER_FORMAT.format('Series', 'Date', 'Maturity', 'Amount', 'Tenure', 'Status')
SEPARATOR = " "*1+"-"*60

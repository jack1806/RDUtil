import pickle
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .rdconstant import *


class RDitem:

    def __init__(self, rid, series, amount, start, tenure):
        self._rid = int(rid)
        self._amount = float(amount)
        self._tenure = int(tenure)
        self._start_date = start
        self._series = int(series)
        self._status = None
        self._maturity_date = None
        self._remaining_time = None
        self.refresh()

    def __str__(self):
        return (RD_HEADER_FORMAT.format(str(self.series), self.start_date.strftime('%d %b %Y'),
                                        self.maturity_date.strftime('%d %b %Y'), str(self.amount),
                                        str(self.tenure), self.status))

    def refresh(self):
        self._series = int(self.series)
        self._status = STATUS_OPEN
        self._maturity_date = self._start_date + relativedelta(months=self.tenure)
        self._remaining_time = self.maturity_date.timestamp() - datetime.today().timestamp()
        if self._remaining_time < 0:
            self._status = STATUS_CLOSED

    @property
    def status(self):
        return self._status

    @property
    def remaining_time(self):
        return self._remaining_time

    @property
    def rid(self):
        return self._rid

    @property
    def amount(self):
        return self._amount

    @property
    def tenure(self):
        return self._tenure

    @property
    def start_date(self):
        return self._start_date

    @property
    def series(self):
        return self._series

    @property
    def maturity_date(self):
        return self._maturity_date

    @amount.setter
    def amount(self, value):
        self._amount = float(value)

    @tenure.setter
    def tenure(self, value):
        self._tenure = int(value)

    @start_date.setter
    def start_date(self, value):
        self._start_date = value

    @maturity_date.setter
    def maturity_date(self, value):
        self._maturity_date = value

    @series.setter
    def series(self, value):
        self._series = int(value)

    @rid.setter
    def rid(self, value):
        self._rid = int(value)

    @remaining_time.setter
    def remaining_time(self, value):
        self._remaining_time = value

    @status.setter
    def status(self, value):
        self._status = value


class Series:

    def __init__(self, s_number=None):
        self._s_number = s_number
        self._r_list = []
        self._s_amount = []
        self._last_r = None
        self.refresh()

    def refresh(self):
        temp_dict = {}
        for r in self.r_list:
            if r.status == STATUS_OPEN:
                temp_dict[r.start_date.timestamp()] = r
                self._last_r = temp_dict[max(list(temp_dict.keys()))]

    @property
    def s_amount(self):
        return self._s_amount

    @property
    def last_r(self):
        return self._last_r

    @property
    def s_number(self):
        return self._s_number

    @s_number.setter
    def s_number(self, value):
        self._s_number = value

    def add_r(self, r_obj):
        self._r_list.append(r_obj)
        self.refresh()

    @property
    def r_list(self):
        return self._r_list

    def get_latest_r(self):
        if self._last_r:
            last_date = self._last_r.start_date
            last_date += relativedelta(months=1, days=1)
            temp_rd = RDitem(self.last_r.rid, self.last_r.series, self.last_r.amount, last_date, self.last_r.tenure)
            print(str(temp_rd))


class RDs:

    def __init__(self):
        self._r_list = []
        self._s_list = {}
        self.refresh()

    def refresh(self, read_from_file=True):
        self._s_list = {}
        if read_from_file:
            with open(FILE_NAME, 'rb') as csv_file:
                self._r_list = pickle.load(csv_file)
        for r in self._r_list:
            r.refresh()
        for r in self._r_list:
            if r.series not in self._s_list:
                self._s_list[r.series] = Series(r.series)
            self._s_list[r.series].add_r(r)

    def write_data(self):
        with open(FILE_NAME, 'wb') as csv_file:
            pickle.dump(self._r_list, csv_file)
        self.refresh()

    def add_r(self, series, amount, start, tenure):
        r_obj = RDitem(len(self._r_list), series, amount, start, tenure)
        self._r_list.append(r_obj)
        self.write_data()

    def get_r(self, r_id):
        for r in self._r_list:
            if r.rid == r_id:
                return r

    def modify_r(self, r_id, param, val):
        if val is None:
            return "Invalid datatype"
        index = 0
        for r in range(len(self.r_list)):
            if self.r_list[r].rid == r_id:
                index = r
                break
        if param == 'S':
            self._r_list[index].series = val
        elif param == 'D':
            self._r_list[index].start_date = val
        elif param == 'A':
            self._r_list[index].amount = val
        elif param == 'T':
            self._r_list[index].tenure = val
        else:
            return "Invalid input given.\nResuming to main menu"
        self.refresh(read_from_file=False)
        self.write_data()
        return "Modified successfully"

    def get_top_r(self, select_all=False, select_series=None):
        temp_dict = {}
        result = []
        list_to_use = self.r_list.copy()
        if isinstance(select_series, int):
            list_to_use = self.s_list[select_series].r_list.copy()
        max_count = [TOP_NUMBER, len(list_to_use)][select_all]
        for r in list_to_use:
            if r.status == STATUS_CLOSED:
                continue
            if r.remaining_time not in temp_dict:
                temp_dict[r.remaining_time] = []
            temp_dict[r.remaining_time].append(r)
        sorted_time = sorted(temp_dict.keys())
        for time in sorted_time:
            for r in temp_dict[time]:
                result.append(r)
                if len(result) >= max_count:
                    return result
        return result

    def upcoming_prem(self):
        print(PREMIUM_HEADER)
        current = datetime.today()
        print_dict = {}
        for r in self.r_list:
            if r.status == STATUS_OPEN and r.start_date.day > datetime.today().day:
                is_breaking = "No"
                maturity_month = r.maturity_date.month
                premium_date = datetime(day=r.start_date.day, month=current.month,
                                        year=current.year)
                if maturity_month == current.month:
                    is_breaking = "Yes"
                if premium_date not in print_dict:
                    print_dict[premium_date.timestamp()] = []
                print_dict[premium_date.timestamp()].append([str(r.series), premium_date.strftime('%d %b %Y'),
                                                             str(r.amount), is_breaking])
        for time_stamp in sorted(print_dict.keys()):
            for r_data in print_dict[time_stamp]:
                print(PREMIUM_FORMAT.format(r_data[0], r_data[1], r_data[2], r_data[3]))
        print(SEPARATOR)

    def recommend_r(self):
        print(RD_HEADER)
        for s in sorted(self.s_list.keys()):
            self.s_list[s].get_latest_r()
        print(SEPARATOR)

    @property
    def r_list(self):
        return self._r_list

    @property
    def s_list(self):
        return self._s_list

from bs4 import BeautifulSoup
import locale
locale.setlocale(locale.LC_ALL, 'de_DE')
from tabulate import tabulate
import subprocess, os, re
from timeit import default_timer as timer
from datetime import date
from datetime import datetime
from pprint import pprint
import itertools, sys

from credentials import *
import calendar
num_to_month = {k: v for k,v in enumerate(calendar.month_name)}

wd = os.path.dirname(os.path.realpath(__file__))

from proc_read import proc_read


from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer, AdaptiveETA, AdaptiveTransferSpeed

def colorize(string, color):
    return color + string + bcolors.ENDC

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    GREY ='\033[1;30m'

weekdays='Thu Fri Sat Sun Mon Tue Wed'.split()

def get():
    lines = proc_read('coffee crawl.coffee {} {}'.format(username,password),
            {'DEBUG': 'nightmare'})
    start = timer()

    html_raw=''
    # symbol = bcolors.OKGREEN + u"\u25b0" + bcolors.ENDC
    symbol = "\u25b0"
    with ProgressBar(
            widgets=[FormatLabel('%(value)d/10s '), Bar(symbol, '|', '|')],
            maxval=10) as progress:
        for line in lines:
            if any(line.startswith(weekday) for weekday in weekdays):
                i=timer() - start
                if i>10: i = 10
                progress.update(i)
            else:
                # print(line)
                html_raw+=line
        print(html_raw)

    return html_raw

def extract_data(html_raw):
    soup = BeautifulSoup(html_raw)
    # print(soup.prettify())
    # return 1
    result = []

    # at start
    boilerplate = """
    Lastschrift Barzauszahlung Belastung SEPA Gutschrift
    SB-SEPA-Ueberweisung POS Last. SEPA-DA-Gutschrift COR1
    """.split()
    # whole words in middle of
    boilerplate2 = """
    et c ie s.a.r.l. mref+ms mref+ eref+zv cd ec ic ek fc
    """.split()

    # part words
    boilerplate3 = """
    mref iban svwz kref eref cred+ bic
    """.split()


    for row in soup.find_all('tr')[1:]:
        try:
            date, _, description, amount = \
                    [col.string for col in row.find_all('td')]
        except:
            continue

        description = description.replace('  ', '').strip('\n').split()
        while 1:
            if description[0] in boilerplate:
                description.pop(0)
            else:
                break
        description = ' '.join(description)
        description = re.sub(r'(\d\d\d\d\d*)', ' ', description)
        description =' '.join([t for t in description.lower().split()[0:4]
            if t not in boilerplate2 and not any(b in t for b in boilerplate3)])
        description=description[:23]
        yield date, description, amount

def _month(datestring):
    """return month as int from datestring that looks like date_format"""
    date_format = '%d.%m.%Y'
    encoded = datetime.strptime(datestring, date_format)
    return encoded.timetuple()[1]

def _day(datestring):
    """return month as int from datestring that looks like date_format"""
    date_format = '%d.%m.%Y'
    encoded = datetime.strptime(datestring, date_format)
    return str(encoded.timetuple()[2])

def _groupby(func,iterable):
    """ the itertools one is broken """
    sorted_items = sorted(iterable, key=func)
    groups = itertools.groupby(sorted_items, key=func)
    for group, content in groups:
        yield group, list(content)



if __name__ == '__main__':
    nrows=160
    html_raw = get()
    open('raw.html', 'w').write(html_raw)
    data = extract_data(open('raw.html').read())

    def color_amount(amount):
        return locale.atof(amount), \
               colorize(amount, bcolors.OKGREEN) if locale.atof(amount) > 0 else \
               colorize(amount[1:], bcolors.GREY)
    def colorize_sum(sum_):
       return colorize(sum_, bcolors.HEADER) if locale.atof(sum_) > 0 else \
           colorize(sum_, bcolors.FAIL)

    def color_category(description):
        return colorize(description, bcolors.OKGREEN) if \
            any(foo in description for foo in 'rewe edeka penny'.split()) else \
                colorize(description, bcolors.GREY)

    # colorcode pos/neg
    data = reversed([(a,b,color_amount(amount)) for a,b,amount in data][:nrows])

    def _date(datestring):
        date_format = '%d.%m.%Y'
        encoded = datetime.strptime(datestring, date_format)
        return datetime.strftime(encoded,'%d')

    by_month = list(_groupby(lambda row: _month(row[0]), data))

    # show only day
    data = [(_date(date),_,_2) for date, _, _2 in data]

    filters='edeka rewe penny aldi'.split()

    for month, content in by_month:
        month_string=' '+(colorize((num_to_month[month]), bcolors.WARNING))+' '
        # content = [(_,descr,_2) for _,descr,_2 in content if
                # any(f in descr for f in filters)]
        sum_ = sum(col[2][0] for col in content)
        content = [(_day(date),_,amount[1]) for date,_,amount in content]


        # month header
        print('\n\n'+month_string.rjust(30,'.')+'...............')

        # rows
        formatted=tabulate(content, ['','',''],tablefmt='plain')
        print(formatted)

        # sum. the following is an utterly ridiculous to get the minus sign to align
        # properly
        if formatted:
            len_last_row = len(list(formatted.splitlines()[-1]))
            start_format_string_from_end = list(reversed(formatted.splitlines()[-1])).index('[', 3)
            start_pos=len_last_row-start_format_string_from_end-3
            sum_formatted = colorize_sum(str(locale.format('%.2f',sum_)))
            if sum_ > 0: start_pos+1
            print(start_pos*' ' + sum_formatted)

        # start_format_amount =
        # print(len_last_row)
        # content.append(('','',
    # for item in data:
        # print(item)

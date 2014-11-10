from flask import *
import markdown
from subprocess import call
import subprocess
from datetime import datetime
import time
import os
import multiprocessing
from time import sleep

from extract import extract
app = Flask(__name__)
wd = os.path.dirname(os.path.realpath(__file__))
dateformat = '%d.%m.%Y'
date_output_format = '%a, %d.%m'

def process_html(html_raw):

# html_raw = subprocess.check_output(
            # ['coffee', os.path.join(wd,'crawl.coffee'), username, password])
    days = extract(html_raw)
    content = "###Today: {}\n\n".format(time.strftime(date_output_format))
    for date, events in days:
        date_ = datetime.strptime(date, dateformat)
        if datetime.now() <= date_ and events:
            date_formatted = date_.strftime(date_output_format)
            if datetime.now() == date_:
                content += '\n###{}\n\n'.format(date_formatted)
            else:
                content += '\n**{}**\n\n'.format(date_formatted)
            for event in events:
                content += '* {}\n'.format(event)
            content += '\n'

    return content.decode('utf8', 'replace')

def spawn_crawling(username, password):
    d = multiprocessing.Process(name='daemon', target=daemon, args=(username, password))
    d.daemon = True
    d.start()
    return d

def daemon(username, password):
    # subprocess.Popen(['./crawl.sh', username, password], cwd=wd, shell=True )
    subprocess.Popen('./crawl.sh {} {}'.format(username, password), cwd=wd, shell=True )


@app.route("/")
def main():
    username = request.args.get('username')
    password = request.args.get('password')
    proc = spawn_crawling(username, password)

    f=os.path.join(wd,'crawl-{}.out'.format(username))
    if not os.path.isfile(f):
        while not os.path.isfile(f): sleep(.1)

    html_raw = open(f).read()
    content = Markup(markdown.markdown(process_html(html_raw)))
    return render_template('index.html', **locals())


if __name__ == "__main__":
    app.debug = True
    app.run()

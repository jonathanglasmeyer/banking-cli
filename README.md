# banking-cli

Scrapes data from your banking website with Nightmare.JS and displays it in a CLI.

Note: currently only scraping for [Haspa](www.haspa.de) is implemented; feel free to add more.

![screenshot](http://i.imgur.com/XjpgPEl.png)

The yellow captions are months. The colums from left to right: day of month, description field of transaction (but with all the usual boilerplate stuff removed), color-coded amount. + a sum for each month beneath.

# dependencies
`sudo npm install -g phantomjs coffeescript`

# install

```
npm install
virtualenv -p `which python3` .env
.env/bin/pip install -r requirements.txt
```

# configuration
add a file `credentials.py` with the following content, wheree foo and bar is the login to your HASPA account:

```
username='foo'
password='bar'
```

# run
add a script like the following to your `~/bin` (or similar) folder, where `$script_location` is the path of this cloned repo; call it `banking-cli`. ;)

```bash
cd $script_location
.env/bin/python extract.py
```


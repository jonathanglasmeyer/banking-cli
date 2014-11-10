Nightmare = require 'nightmare'
fs = require 'fs'

$ = require 'jquery'

args = process.argv.slice(2)
username = args[0]
password = args[1]

login_page = 'https://ssl2.haspa.de/OnlineFiliale/banking/authenticate/login'
overview_page = 'https://ssl2.haspa.de/OnlineFiliale/banking/services/giro/transactionList?accountId=1265401826&period=90'
id_field = 'input[title="Bitte tragen Sie hier Ihre Identifikationskontonummer ein. "]'
pin_field = 'input[title="Geben Sie bitte Ihre PIN ein ( bis zu 12 Zeichen )."]'
login_btn = 'input[type="submit"]'

crawl = ->
  new Nightmare({sslProtocol: 'tlsv1', loadImages: false})
    .goto login_page
    .wait id_field
    .type id_field, username
    .wait pin_field
    .type pin_field, password
    .click login_btn
    .wait()
    .goto overview_page
    .wait()
    .evaluate (
      (page) -> $('table.tab-1').html()),
      (res) -> console.log res
    .run (err, nightmare) ->
      if (err) then console.log '' else console.log ''

crawl()



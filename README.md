webpac-tools
============

A collection of CLI and RESTful interfaces to Millennium WebPAC.


CLI: webpac
------------------------------

This tools provides a command line interface to WebPAC functions.

You must specify the Millennium server, either through the `--server` parameter, or by setting the environment variable `WEBPAC_SERVER`.

Other environment variables supported:
* `WEBPAC_PORT` -- sets the web server port for the WebPAC server (default: 443)

### webpac
```
$ webpac --help

usage: webpac [-h] [--server SERVER] [--port PORT] [--no_ssl] [--debug]
              {change_pin,modify_contact_info,register,get_contact_info} ...

Provides a CLI wrapper to Millennium WebPAC functions.

positional arguments:
  {change_pin,modify_contact_info,register,get_contact_info}
                        sub-command help
    change_pin          change patron's PIN
    modify_contact_info
                        modify patron's contact information
    register            register a new patron
    get_contact_info    get patron's current contact information

optional arguments:
  -h, --help            show this help message and exit
  --server SERVER       hostname or IP of Millennium server
  --port PORT           remote WebPAC port on the Millennium server (default:
                        443)
  --no_ssl              disable server connection
  --debug               enable diagnostic output
```

### webpac change_pin
```
$ webpac change_pin --help

usage: webpac change_pin [-h] --barcode BARCODE --pin PIN NEW_PIN

positional arguments:
  NEW_PIN            new PIN

optional arguments:
  -h, --help         show this help message and exit
  --barcode BARCODE  patron's barcode
  --pin PIN          patron's PIN
```

### webpac modify_contact_info
```
$ webpac modify_contact_info --help

usage: webpac modify_contact_info [-h] --barcode BARCODE --pin PIN
                                  ADDRESS_LINE_1 ADDRESS_LINE_2 TELEPHONE
                                  EMAIL LOCATION_CODE

positional arguments:
  ADDRESS_LINE_1     address line one
  ADDRESS_LINE_2     address line two
  TELEPHONE          telephone number
  EMAIL              email address
  LOCATION_CODE      default branch location code

optional arguments:
  -h, --help         show this help message and exit
  --barcode BARCODE  patron's barcode
  --pin PIN          patron's PIN
```

### webpac get_contact_info
```
usage: webpac get_contact_info [-h] --barcode BARCODE --pin PIN

optional arguments:
  -h, --help         show this help message and exit
  --barcode BARCODE  patron's barcode
  --pin PIN          patron's PIN
```

### webpac register
```
$ webpac register --help

usage: webpac register [-h]
                       FIRST_NAME MIDDLE_NAME LAST_NAME MAILING_ADDRESS
                       MAILING_CITY MAILING_STATE MAILING_ZIPCODE
                       STREET_ADDRESS STREET_CITY STREET_STATE STREET_ZIPCODE
                       TELEPHONE_AREA TELEPHONE_PREFIX TELEPHONE_LINENUMBER
                       EMAIL BIRTH_MONTH BIRTH_DAY BIRTH_YEAR

positional arguments:
  FIRST_NAME            first name
  MIDDLE_NAME           middle name
  LAST_NAME             last name
  MAILING_ADDRESS       mailing address line
  MAILING_CITY          mailing address city
  MAILING_STATE         mailing address state
  MAILING_ZIPCODE       mailing address zipcode
  STREET_ADDRESS        street address line
  STREET_CITY           street address city
  STREET_STATE          street address state
  STREET_ZIPCODE        street address zipcode
  TELEPHONE_AREA        telephone area code
  TELEPHONE_PREFIX      telephone prefix code
  TELEPHONE_LINENUMBER  telephone line number
  EMAIL                 email address
  BIRTH_MONTH           birthdate month
  BIRTH_DAY             birthdate day
  BIRTH_YEAR            birthdate year

optional arguments:
  -h, --help            show this help message and exit
```

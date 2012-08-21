"""This module provides an API to access Millennium WebPAC
functions through the use of web scraping techniques.
"""
__author__ = "Andrew Livesay <andrewl@multco.us>"
__license__ = "Public Domain"

import urllib, urllib2
from BeautifulSoup import BeautifulSoup
import re


class WebPACSession:
  """Provides access to WebPAC functions, maintaining web
  sessions where required.
  """

  def __init__(self, url, debug=False):
    self.url = url
    self.debug = debug
    
    if debug:
      self.__setup_debug()

    self.user_id = None
    self.logged_in = False
    self.cookie = None
    self.new_session()


  def __setup_debug(self):
    if self.url.upper.startswith('HTTPS'):
      urllib2.install_opener(urllib2.build_opener(urllib2.HTTPSHandler(debuglevel=1)))
    else:
      urllib2.install_opener(urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1)))


  def __request(self, resource, params=None):
    """ Manages web request to WebPAC server. """
    
    request_url = self.url + resource

    if params:
      request = urllib2.Request(request_url, urllib.urlencode(params))
    else:
      request = urllib2.Request(request_url)

    request.add_header('Referrer', request_url)

    if self.cookie:
      request.add_header('cookie', self.cookie)

    if self.debug:
      print 'request: %s\n' % request.get_full_url()

    return urllib2.urlopen(request)


  def new_session(self):
    """ Gets a fresh WebPAC session cookie. """

    response = self.__request('/')
    self.cookie = response.headers.get('Set-Cookie')


  def login(self, code, pin):
    """ Logs into a WebPAC session. """

    login_resource = '/patroninfo'

    params = { 'code': code, 'pin': pin, 'submit.x': '0', 'submit.y': '0' }

    response = self.__request(login_resource, params)
    soup = BeautifulSoup(response)

    loggedInMessage = soup.find('span', { 'class': 'loggedInMessage'})

    if loggedInMessage:
      try:
        self.user_id = re.search(r'(\d+)(?!.*\d)', response.url).group(0)
      except AttributeError:
        raise Exception('userid not found')
      self.logged_in = True
    else:
      raise Exception('login failed')


  def change_pin(self, pin, new_pin):
    """ Changes a patron's PIN. """

    if not self.logged_in:
      raise Exception('not logged in')

    newpin_resource = '/patroninfo/' + self.user_id + '/newpin'

    params = { 'pin': pin, 'pin1': new_pin, 'pin2': new_pin,
               'submit.x' : '0', 'submit.y' : '0'}
   
    response = self.__request(newpin_resource, params)
    soup = BeautifulSoup(response)

    errormessage = soup.find('span', { 'class': 'errormessage' })

    if errormessage:
      raise Exception(errormessage.text)

  
  def modify_contact_info(self, address_line_1, address_line_2,
                          telephone, email, location_code):
    """ Sets patron's contact information. """

    if not self.logged_in:
      raise Exception('not logged in')
    
    modpinfo_resource = '/patroninfo/' + self.user_id + '/modpinfo'

    params = { 'addr1a': address_line_1, 'addr1b': address_line_2, 'tele1': telephone,
               'email': email, 'locx00': location_code.ljust(5),
               'submit.x': '0', 'submit.y': '0' }

    response = self.__request(modpinfo_resource, params)
    soup = BeautifulSoup(response)


  def register(self, first_name, middle_name, last_name,
               mailing_address, mailing_city, mailing_state, mailing_zipcode,
               street_address, street_city, street_state, street_zipcode, 
               telephone_area, telephone_prefix, telephone_linenumber,
               email, birth_month, birth_day, birth_year):
    """ Registers a new patron. """
    
    params = { 'nfirst': first_name, 'nmiddle': middle_name, 'nlast': last_name,
               'stre_aaddress': mailing_address.upper(), 'city': mailing_city.upper(),
               'state': mailing_state.upper(), 'zipcode': mailing_zipcode, 'city_aaddress': '',
               'stre_aaddress2': street_address.upper(), 'city2': street_city.upper(),
               'state2': street_state.upper(), 'zipcode2': street_zipcode, 'city_aaddress2': '',
               'Phone_1': telephone_area, 'Phone_2': telephone_prefix, 'Phone_3': telephone_linenumber,
               'tphone1': '', 'zemailaddr': email,
               'birthdate1': birth_month, 'birthdate2': birth_day, 'birthdate3': birth_year,
               'F051birthdate': '' }

  def get_contact_info(self):
    """ Gets the patron's current contact information. """

    modpinfo_resources = '/patroninfo/' + self.user_id + '/modpinfo'

    response = self.__request(modpinfo_resources)
    soup = BeautifulSoup(response)
    
    values = ['addr1a', 'addr1b', 'tele1', 'email']
    inputs = dict((value, soup.find('input', { 'name': value })) for value in values) 
    loc_select = soup.find('option', { 'selected': 'selected' })

    contact_info = dict((k,v.get('value') if v else '') for (k,v) in inputs.iteritems())
    contact_info['locx00'] = loc_select.get('value') if loc_select else ''
    
    return contact_info


if __name__ == "__main__":
  wpsession = WebPACSession('https://catalog.example.com', debug=False)

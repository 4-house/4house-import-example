#!/usr/bin/python

"""
TEST IMPORT EXAMPLE

More info:
- visit https://developers.4.house/sreality.html
- mailto: import@4.house
"""

# pylint: disable=too-few-public-methods
import copy
import time
import sys
import hashlib
import xmlrpc.client as xc
import logging

NOW = int(time.time())

# seller/agent
TEST_SELLER = {\
	'client_login': 'test+sreality-%s@4.house' % NOW,\
	'client_domain': '4.house',\
	'client_name': 'Jan Tester',\
	'contact_gsm': '+420%s' % str(NOW)[-6:],\
	'client_id': str(NOW)[-9:],\
	'contact_email': 'test+sreality-%s@4.house' % NOW,\
	'makler_note': 'Testovani makler test=%s' % NOW,\
}
TEST_SELLER_ID = 2973
TEST_SELLER_RKID = ''

# location
TEST_LOCATIONS = [\
	{'city': 'Praha', 'citypart':'Smíchov', 'street':'Radlická 180/50',\
		'latitude':50.0663614, 'longitude':14.4005557, 'inaccuracy_level':1},\
	{'city': 'Praha', 'citypart':'Smíchov', 'street':'Radlická 180/50',\
		'latitude':50.0663614, 'longitude':14.4005557, 'inaccuracy_level':2},\
	{'city': 'Praha', 'citypart':'Smíchov', 'street':'Radlická 180/50',\
		'latitude':50.0663614, 'longitude':14.4005557, 'inaccuracy_level':3},\
	{'city': 'Praha', 'citypart':'Smíchov', 'street':'', 'latitude':50.0663614,\
		'longitude':14.4005557, 'inaccuracy_level':3},\
	{'city': 'Barcelona, Španělsko', 'citypart':'', 'street':'', 'latitude':0, 'longitude':0},\
	{'city': 'Nice, Francie', 'citypart':'', 'street':'', 'latitude':0, 'longitude':0},\
]

# advert_function
# 1 Prodej
# 2 Pronájem
# 3 Drazby

# advert_type
# 1 Byty
# 2 Domy
# 3 Pozemky
# 4 Komercní ˇ
# 5 Ostatní

TEST_TYPES = [\
	{'advert_function':1, 'advert_type':1},\
	{'advert_function':1, 'advert_type':2},\
	{'advert_function':2, 'advert_type':1},\
	{'advert_function':2, 'advert_type':2},\
]

# price
TEST_PRICE_VALUE = 123000
TEST_PRICE_CURRENCY = 1

TEST_ADVERT = {\
	'advert_function': 1,\
	'advert_lifetime': 1,\
	'advert_price': TEST_PRICE_VALUE,\
	'advert_price_currency': TEST_PRICE_CURRENCY,\
	'advert_price_unit': 2,\
	'advert_type': 1,\
	'floor_number': 1,\
	'garage': False,\
	'loggia': False,\
	'balcony': False,\
	'terrace': False,\
	'ownership': 1,\
	'parking_lots': True,\
	'advert_subtype': 4,\
	'usable_area': 54,\
	'building_type': 2,\
	'building_condition': 1,\
	'cellar': True,\
	'heating': (3, 4),\
	'telecommunication': (1, 2, 4),\
	'description': 'Testovací inzerát z importu sreality API',\
	'seller_rkid': TEST_SELLER_RKID,\
	'seller_id': TEST_SELLER_ID,\
	#'ready_date':'18.11.2020',\
	#'ready_date':None,\
	#'ready_date':'',\
	'ready_date':'20211111T00:00:00+0000',\
}

SREALITY_APIS = {\
	'prod' : 'https://prod-api-impsreality.4.house/RPC2',\
	'develop': 'https://develop-api-impsreality.4house.dev/RPC2'}


INFO = 'info'
DEBUG = 'debug'
ERROR = 'error'


class ImportExample:
	""" Example for """

	def __init__(self, env, client_id, sw_key, md5_passwd):
		""" init """

		self.env = env
		self.md5_passwd = md5_passwd
		self.sw_key = sw_key
		self.__msg('init: client_id=%s, md5_heslo=%s, sw_key=%s' % \
			(client_id, md5_passwd, sw_key), DEBUG)

		# log
		logging.getLogger().setLevel(logging.INFO)

		# sreality url
		sreality_url = SREALITY_APIS.get(env)
		if not sreality_url:
			self.__msg('Wrong env=%s -> choose: develop or prod' % env, ERROR)
			raise 'sreality_url_notexist'

		# connect
		self.__client_id = int(client_id)
		self.__client = xc.Server(sreality_url, allow_none=True)


	def __msg(self, msg, msg_type=DEBUG):
		""" debug message """

		if not msg:
			return False

		print('%s [%s]: %s' % (msg_type.upper(), self.env, msg))
		return True


	def __response_type(self, response):
		""" response_type """
		# pylint: disable=no-self-use

		response_type = INFO
		if response['status'] != 200:
			response_type = ERROR

		return response_type


	# --- advert ---

	def __add_advert(self, session_id, advert):
		""" Add new offer or edit existing one """
		self.__msg('__add_advert(session_id=%s, advert=%s)' % \
			(session_id, advert), DEBUG)

		response = self.__client.addAdvert(session_id, advert)
		self.__msg('__add_advert(session_id=%s, advert=%s) -> response=%s' % \
			(session_id, advert, response), self.__response_type(response))
		return response


	def __list_advert(self, session_id):
		""" Print the whole list of offers """

		response = self.__client.listAdvert(session_id)
		self.__msg('__list_advert(session_id=%s) -> response=%s' % \
			(session_id, response), self.__response_type(response))
		return response


	# --- seller ---

	def __list_seller(self, session_id):
		""" Print the whole list of sellers """

		response = self.__client.listSeller(session_id)
		self.__msg('__list_seller(session_id=%s) -> response=%s' % \
			(session_id, response), self.__response_type(response))
		return response

	def __add_seller(self, session_id, seller):
		""" add seller """
		self.__msg('__add_seller(session_id=%s, seller=%s)' % \
			(session_id, seller), DEBUG)

		response = self.__client.addSeller(session_id, 0, '', seller)
		self.__msg('__add_seller(session_id=%s, seller=%s) -> response=%s' % \
			(session_id, seller, response), self.__response_type(response))
		return response


	# -- login ---

	def __new_session_id(self, old_id, passwd, key):
		""" new session id """

		var_part = hashlib.md5()
		var_part.update(old_id.encode('utf-8') + passwd.encode('utf-8') + key.encode('utf-8'))

		session_id = old_id[0:48] + var_part.hexdigest()
		self.__msg('__new_session_id(old_id=%s, passwd=%s, key=%s) -> session_id=%s' % \
			(old_id, passwd, key, session_id))
		return session_id


	def __login(self):
		""" login """

		# session
		get_hash = self.__client.getHash(self.__client_id)
		session_id = self.__new_session_id(\
			get_hash['output'][0]['sessionId'], self.md5_passwd, self.sw_key)

		# login
		self.__msg('__login() -> client.login(%s)' % session_id, DEBUG)
		response = self.__client.login(session_id)
		if response['status'] != 200:
			self.__msg('logged in, response=%s' % response, ERROR)
			return None

		self.__msg('logged in, response=%s' %  response, INFO)
		session_id = self.__new_session_id(session_id, self.md5_passwd, self.sw_key)
		return session_id


	def test(self):
		""" tests """

		rets = []
		self.__msg('start', INFO)

		# login
		session_id = self.__login()
		if not session_id:
			return False
		print()

		# add seller
		seller = self.__add_seller(session_id, TEST_SELLER)
		rets.append(['addSeller', seller])
		print()

		# offers for tests
		offers = []
		for locality in TEST_LOCATIONS:
			offer = copy.deepcopy(TEST_ADVERT)
			locs = []
			for key in tuple(locality.keys()):
				offer['locality_%s' % key] = locality[key]
				locs.append('%s=%s' % (key, locality[key]))

			offer['description'] = '%s. Localita: %s, test=%s' % \
				(offer['description'], ', '.join(locs), int(time.time()))

			offer['seller_id'] = seller['output'][0]['seller_id']
			offer['seller_rkid'] = ''
			offers.append(offer)


		for testtype in TEST_TYPES:
			offer = copy.deepcopy(TEST_ADVERT)

			locs = []
			for key in TEST_LOCATIONS[0]:
				offer['locality_%s' % key] = TEST_LOCATIONS[0][key]
				locs.append('%s=%s' % (key, TEST_LOCATIONS[0][key]))

			types = []
			for key in tuple(testtype.keys()):
				types.append('%s=%s' % (key, testtype[key]))

			offer['description'] = '%s. Localita: %s, Typ: %s, test=%s' % (\
				offer['description'], ', '.join(locs), ', '.join(types), int(time.time()))

			offer['seller_id'] = seller['output'][0]['seller_id']
			offer['seller_rkid'] = ''

		# add advert
		for offer in offers:
			rets.append(['addAdvert', self.__add_advert(session_id, offer)])
			print()

		# list advert
		rets.append(['listAdvert', self.__list_advert(session_id)])
		print()

		# list seller
		rets.append(['listSeller', self.__list_seller(session_id)])
		print()

		# summary
		print('--- Summary --- ')
		for ret in rets:
			print('%s: %s %s -> %s' % (ret[0], ret[1].get('status'),\
				ret[1].get('statusMessage'), ret[1].get('output')))

		self.__msg('finish -> true', INFO)
		return True


if __name__ == '__main__':

	if len(sys.argv) != 5:
		logging.error('Wrong count of input arguments')
		logging.info('RUN: python3 test_import.py CLIENT_ID MD5_HESLO SW_KEY ENV')
		logging.info('exit!')
		sys.exit(1)

	CLIENT_ID = sys.argv[1]  # ID klienta
	SW_KEY = sys.argv[2] # importni klic
	MD5_PASSWD = sys.argv[3]  # heslo zakryptovane pres md5
	ENV = sys.argv[4] # env pro napojeni: develop nebo prod

	IMPORT_EXAMPLE = ImportExample(ENV, CLIENT_ID, SW_KEY, MD5_PASSWD,)
	IMPORT_EXAMPLE.test()

#!/usr/bin/python

"""
TEST IMPORT EXAMPLE
"""


import sys
import hashlib
import xmlrpc.client as xc
import logging

# pylint: disable=too-few-public-methods

logging.getLogger().setLevel(logging.INFO)


TEST_ADVERT = {\
		'advert_function': 1,\
		'advert_lifetime': 1,\
		'advert_price': 123000.0,\
		'advert_price_currency': 1,\
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
		"description": "Pekny byt s vyhledem na zahradu.\
		Pekny byt s vyhledem na zahradu.Pekny byt s vyhledem na zahradu.\
		Pekny byt s vyhledem na zahradu.",\
		"locality_city": "Praha",\
		'locality_street': 'Prazska',\
		'locality_citypart': 'Zizkov',\
		'locality_latitude': 50.073658,\
		'locality_longitude': 14.418540,\
		'locality_inaccuracy_level': 2,\
		# nebo 'seller_rkid'
		'seller_id': 2973}


class ImportExample:
	""" Example for """

	@staticmethod
	def __add_advert(session_id, client, advert):
		""" Add new offer or edit existing one """

		response = client.addAdvert(session_id, advert)
		print(f'__add_advert(session_id={session_id}, advert={advert}) -> response: {response}')

	@staticmethod
	def __list_advert(session_id, client):
		""" Print the whole list of offers """

		response = client.listAdvert(session_id)
		print(f'__list_advert(session_id={session_id}) -> response: {response}')

	@staticmethod
	def __list_seller(session_id, client):
		""" Print the whole list of sellers """

		response = client.listSeller(session_id)
		print(f'__list_seller(session_id={session_id}) -> response: {response}')

	@staticmethod
	def __new_session_id(old_id, password, key):
		""" new session id """

		var_part = hashlib.md5()
		var_part.update(old_id.encode('utf-8') + password.encode('utf-8') + key.encode('utf-8'))

		return old_id[0:48] + var_part.hexdigest()

	def connection(self, client_id, md5_heslo, sw_key, env):
		""" Make connection """
		# pylint: disable=invalid-name

		if env not in ('develop', 'prod'):
			print(f'Wrond env={env} -> choose: develop or prod')
			return

		IMPORT_SOFT = "https://%s-api-impsreality.4.house/RPC2" % env

		client = xc.Server(IMPORT_SOFT)
		getHash = client.getHash(int(client_id))

		session_id = self.__new_session_id(getHash["output"][0]["sessionId"], md5_heslo, sw_key)
		response = client.login(session_id)
		if response["status"] / 100 == 2:
			logging.info("logged in")

		session_id = self.__new_session_id(session_id, md5_heslo, sw_key)

		# self.__add_advert(session_id, client, TEST_ADVERT)
		self.__list_advert(session_id, client)
		self.__list_seller(session_id, client)


if __name__ == '__main__':

	IMPORT_EXAMPLE = ImportExample()

	if len(sys.argv) != 5:
		logging.error('Wrong count of input arguments')
		logging.info('RUN: python3 test_import.py clientId md5_heslo sw_key env')
	else:
		CLIENT_ID = sys.argv[1]  # ID klienta
		MD5_HESLO = sys.argv[2]  # heslo zakryptovane pres md5
		SW_KEY = sys.argv[3] # importni klic
		ENV = sys.argv[4] # env pro napojeni: develop nebo prod

		IMPORT_EXAMPLE.connection(CLIENT_ID, MD5_HESLO, SW_KEY, ENV)

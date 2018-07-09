#!/usr/bin/env python3
#
# MIT License
#
# Copyright (c) 2018 Olivier Girard
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import re
import string
import random

#--------------------------------------------------------------------
# UTILITIES
#--------------------------------------------------------------------
def rotate_wheel(myKey, myList):
	idx  = myList.index(myKey)
	return myList[idx:] + myList[:idx]

def get_wheels(myKey):

	# Init the wheels
	alpha   = list(string.ascii_lowercase)
	wheel1  = ["%02d" %i for i in range( 1,  27)]
	wheel2  = ["%02d" %i for i in range(27,  53)]
	wheel3  = ["%02d" %i for i in range(53,  79)]
	wheel4  = ["%02d" %i for i in range(79, 100)]+['00', 'v1', 'v2', 'v3', 'v4'] # Recode (INQ) as V4

	# Pre-format key to symplify things
	myKey   = myKey.replace("(INQ)", "v4")
	myKey   = re.sub('\s+', '', myKey)
	myKey   = myKey.lower()

	# Rotate the wheels
	alpha   = rotate_wheel(myKey[0]  , alpha )
	wheel1  = rotate_wheel(myKey[1:3], wheel1)
	wheel2  = rotate_wheel(myKey[3:5], wheel2)
	wheel3  = rotate_wheel(myKey[5:7], wheel3)
	wheel4  = rotate_wheel(myKey[7:9], wheel4)

	return [alpha, wheel1, wheel2, wheel3, wheel4]

def print_wheels(alpha, wheel1, wheel2, wheel3, wheel4):

	print('   {0}'.format('     '.join(str(i) for i in alpha)))
	print(wheel1)
	print(wheel2)
	print(wheel3)
	print(wheel4)
	print('')


#--------------------------------------------------------------------
# INQ DECODING
#--------------------------------------------------------------------
def decode_inq(key, message, verbose=False):

	# Get the Wheels
	alpha, wheel1, wheel2, wheel3, wheel4 = get_wheels(myKey=key)

	# Pre-format message
	message = message.replace("(INQ)", "v4")
	message = re.sub('\s+', '', message)
	message = message.lower()

	# Decode the stuff
	decoded_message = ''
	while message:
		code    = message[0:2]
		message = message[2:]

		if code in wheel1:
			index = wheel1.index(code)
		elif  code in wheel2:
			index = wheel2.index(code)
		elif  code in wheel3:
			index = wheel3.index(code)
		elif  code in wheel4:
			index = wheel4.index(code)
		else:
			print('ERROR: bad message code: {0}'.format(code))

		decoded_message = decoded_message + alpha[index]

	# Some printing for debugging
	if verbose:
		print_wheels(alpha, wheel1, wheel2, wheel3, wheel4)

	return decoded_message


#--------------------------------------------------------------------
# INQ ENCODING
#--------------------------------------------------------------------
def encode_inq(key, message, verbose=False):

	# Get the Wheels
	alpha, wheel1, wheel2, wheel3, wheel4 = get_wheels(myKey=key)

	# Pre-format message
	message = re.sub('\s+', '', message)
	message = message.lower()

	encoded_message = ''
	while message:
		character = message[0:1]
		if character in alpha:
			index = alpha.index(character)
		else:
			print('ERROR: unsupported message character: {0}'.format(character))

		message         = message[1:]
		codes           = [wheel1[index], wheel2[index], wheel3[index], wheel4[index]]
		code_select     = random.randint(0,3)
		encoded_message = encoded_message + codes[code_select] + ' '

	if verbose:
		print_wheels(alpha, wheel1, wheel2, wheel3, wheel4)

	return encoded_message


#--------------------------------------------------------------------
# SOME TESTING
#--------------------------------------------------------------------
if __name__ == "__main__":

	#
	# SOME DECODING
	#
	print('------- SOME DECODING -------')

	key               = 'J 11 42 60 (INQ)'
	message           = '33 15 98 95 20 77 13 73 12 26 51 88 09 95 64 78 97 07 47 68 91 12 52 04 40 V3 46 V1'
	message_corrected = '33 15 98 95 20 77 13 73 02 26 51 88 09 95 64 79 87 07 47 68 91 02 52 04 40 V3 46 V1'
	#                                             |                    |  |              |
	print(decode_inq(key=key, message=message_corrected, verbose=False))

	key               = 'E 09 33 53 95'
	message           = '06 85 23 85 22 33 24 19 78 22 57 18 V1 03 43 68 66 79 50 29 16 48 99 (INQ) 09'
	message_corrected = '06 95 23 85 22 33 24 19 78 22 57 18 V1 03 43 69 66 79 50 29 16 48 99 (INQ) 09'
	#                        |                                         |
	print(decode_inq(key=key, message=message_corrected, verbose=False))

	key               = 'Q 17 44 61 79'
	message           = '04 53 07 75 46 82 09 V3 14 29 93 77 36 V2 81 97 41 20 78 75 V1 V3 65 82 08'
	print(decode_inq(key=key, message=message,           verbose=False))

	key               = 'U 14 48 56 V2'
	message           = '22 V2 11 02 76 00 70 55 18'
	print(decode_inq(key=key, message=message,           verbose=False))

	key               = 'G 04 33 73 V1'
	message           = '35 40 14 47 74 16 06 17 V2 89 31'
	message_corrected = '35 40 14 47 75 16 06 17 V3 90 31'
	#                                 |           |  |
	print(decode_inq(key=key, message=message_corrected, verbose=False))

	key               = 'Z 02 52 72 90'
	message           = '22 10 77 20 77 03 44 95 V3 17 82 31 18 58 \
	                     91 (INQ) 95 83 11 40 22 10 07 17 05 95 03 \
	                     16 22 54 77 40 22 34 77 64 95 91 82 31 21 \
	                     47 74 V3 73 64 55 (INQ) 77 45 99 16 66 10 \
	                     07 45 V1 01'
	print(decode_inq(key=key, message=message,           verbose=False))

	key               = 'W 21 49 65 79'
	message           = '72 13 71 00 25 84 V1 62 76 91 40 53 88 77 17 34 27 16 03 32 10 81 07 56 33'
	print(decode_inq(key=key, message=message,           verbose=False))

	key               = 'D 05 31 78 91'
	message           = '20 77 96 32 62 04 92'
	print(decode_inq(key=key, message=message,           verbose=False))

	key               = 'M 10 33 78 94'
	message           = '(INQ) 73 82 V1 90 03 70 42 51 15 80 35 11 02 07 V2 33 13 86 01 24 17 54 95 49 02'
	print(decode_inq(key=key, message=message,           verbose=False))

	#
	# SOME ENCODING
	#
	print('------- SOME ENCODING -------')

	key               = 'U 14 48 56 V2'
	message           = 'Comment ca va Vsause'
	encoded_message   = encode_inq(key=key, message=message,           verbose=False)
	decoded_message   = decode_inq(key=key, message=encoded_message,   verbose=False)
	print(key)
	print(encoded_message)
	print(decoded_message)


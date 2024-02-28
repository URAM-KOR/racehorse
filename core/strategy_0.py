
if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		print(path.dirname( path.dirname( path.abspath(__file__) ) ))
		sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))

from interface.upbit import buycoin_mp, sellcoin_mp


sellcoin_mp("KRW-XRP", str(7.34034744))
import base64
import struct
import bb64

if __name__=='__main__':
	key = 'AIWFFIHkk/ke/sZAIt8njF6HJ35mUvH4yd3MDnHvFHHaZW8eexIYh4MJw1Lj4eU8BVB2DFusT1sqfv6ST1XEWtfYfOeR2JQTbs7eqECNvSHYCXkcvFGSaHR/IllZqeCLeZJyGFuSr9DW1NOqbu4gphcokDVEH248CWNGRAc0LkC3'
	s = base64.b64decode(key.encode())
	n = int.from_bytes(s, byteorder='big')
	print(n)
	print(int(bb64.b64tohex(key),16))
	print(str(base64.b64encode(str(n).encode('utf8')).decode()))

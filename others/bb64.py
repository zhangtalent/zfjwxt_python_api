import rsa
import binascii

b64map="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
b64pad="=";
BI_RM = "0123456789abcdefghijklmnopqrstuvwxyz";

def int2char(n): 
	return BI_RM[n]

def b64tohex(s):
	ret = ""
	k = 0
  # b64 state, 0-3
	for i in range(0,len(s),1):
		if(s[i] == b64pad): 
			break
		v = b64map.index(s[i]);
		if(v < 0): 
			continue
		if(k == 0): 
			ret += (int2char(v >> 2))
			slop = v & 3
			k = 1
		elif(k == 1): 
			ret += int2char((slop << 2) | (v >> 4));
			slop = v & 0xf;
			k = 2;
    
		elif (k == 2): 
			ret += int2char(slop);
			ret += int2char(v >> 2);
			slop = v & 3;
			k = 3;
    
		else: 
			ret += int2char((slop << 2) | (v >> 4));
			ret += int2char(v & 0xf);
			k = 0;
    
	if(k == 1):
		ret += int2char(slop << 2);
	return ret;

def hex2b64(h):
  
	ret = ""
	for i in range(0, len(h), 3):
		c = int(h[i:i+3],16)
		ret += b64map[c >> 6] + b64map[c & 63]
  
	if(i+1 == len(h)):
		c = int(h[i:i+1],16)
		ret += b64map[c << 2]
  
	elif(i+2 == len(h)):
		c = int(h[i:i+2],16)
		ret += b64map[c >> 2] + b64map[(c & 3) << 4]
	while((len(ret) & 3) > 0): 
		ret += b64pad;
	return ret;	
	
	
def get_pwd_rsa(n,pwd):
        #"""
        #   Get rsa2 encrypted password, using RSA module from https://pypi.python.org/pypi/rsa/3.1.1, documents can be accessed at
        #    http://stuvel.eu/files/python-rsa-doc/index.html
        #"""
        #n, n parameter of RSA public key, which is published by WEIBO.COM
        #hardcoded here but you can also find it from values return from prelogin status above
        #weibo_rsa_n = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'

        #e, exponent parameter of RSA public key, WEIBO uses 0x10001, which is 65537 in Decimal
	weibo_rsa_e = 65537
	message = str(pwd).encode()
	
	
	rsa_n = binascii.b2a_hex(binascii.a2b_base64(n))
	print(rsa_n)
        #construct WEIBO RSA Publickey using n and e above, note that n is a hex string
	key = rsa.PublicKey(int(rsa_n, 16), weibo_rsa_e)
		
        #get encrypted password
	encropy_pwd = rsa.encrypt(message, key)
        #trun back encrypted password binaries to hex string
	return binascii.b2a_base64(encropy_pwd) 
	
	

	
	
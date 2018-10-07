import rsa
import binascii
import bb64

def get_pwd_rsa(pwd):
        """
            Get rsa2 encrypted password, using RSA module from https://pypi.python.org/pypi/rsa/3.1.1, documents can be accessed at
            http://stuvel.eu/files/python-rsa-doc/index.html
        """
        #n, n parameter of RSA public key, which is published by WEIBO.COM
        #hardcoded here but you can also find it from values return from prelogin status above
        weibo_rsa_n = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'

        #e, exponent parameter of RSA public key, WEIBO uses 0x10001, which is 65537 in Decimal
        weibo_rsa_e = 65537
        message = str(pwd)

        #construct WEIBO RSA Publickey using n and e above, note that n is a hex string
        key = rsa.PublicKey(int(weibo_rsa_n, 16), weibo_rsa_e)

        #get encrypted password
        encropy_pwd = rsa.encrypt(message.encode('utf-8'), key)
        #trun back encrypted password binaries to hex string
        return str(bb64.hex2b64(binascii.b2a_hex(encropy_pwd))) 

if __name__ == '__main__':
		print(get_pwd_rsa('123'))
    
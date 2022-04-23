'''Script to create and test public,private keys for use in rsa encryption'''
import rsa

def save_key(public_key, private_key):
    '''Save the public_key'''
    with open("App/public_key", "wb") as public_file:
        public_file.write(public_key.save_pkcs1())

    '''Save the private_key''' #pylint:disable=pointless-string-statement
    with open("App/private_key", "wb") as private_file:
        private_file.write(private_key.save_pkcs1())

def load_key():
    '''Read the public_key'''
    with open("App/public_key", "rb") as public_file:
        public_key = rsa.PublicKey.load_pkcs1(public_file.read())

    '''Read the private_key''' #pylint:disable=pointless-string-statement
    with open("App/private_key", "rb") as private_file:
        private_key = rsa.PrivateKey.load_pkcs1(private_file.read())

    return public_key, private_key

# Test the functions
public_key1, private_key1 = rsa.newkeys(4098)
save_key(public_key1, private_key1)
public_key2, private_key2 = load_key()
assert public_key1 == public_key2
assert private_key1 == private_key2

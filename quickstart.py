import keyring


def testKey(service_name, name):
    print(keyring.get_password(service_name, name))

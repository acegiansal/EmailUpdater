import keyring
from quickstart import testKey
import schedule

if __name__ == '__main__':
    name = "GO_SENS_GO"
    service_id = "test_keyring"

    keyring.set_password(service_id, name, 'ZUUUUUUB')
    testKey(service_id, name)

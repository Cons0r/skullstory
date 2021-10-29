import uuid
import hashlib
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

def newkey() -> str:
    if open(f'{dir_path}\\.keyval', 'r').read() == "True":
        return open(f'{dir_path}\\.key', 'r').read()
    retval = str(str(hashlib.sha512(f'{uuid.uuid1()}./\\/./\\/{uuid.uuid5(uuid.NAMESPACE_URL, "https://google.com/")}'.encode()).hexdigest()) + str(hashlib.sha512(f'{uuid.uuid1()}./\\/./\\/{uuid.uuid5(uuid.NAMESPACE_URL, "https://herokuapp.com/")}'.encode()).hexdigest()) + str(hashlib.sha512(f'{uuid.uuid1()}./\\/./\\/\n{uuid.uuid1()}'.encode()).hexdigest()) + str(hashlib.sha512(f'{uuid.uuid1()}./\\/\n./\\/{uuid.uuid5(uuid.NAMESPACE_URL, "https://stackoverflow.com/")}'.encode()).hexdigest()) * 3)
    open(f'{dir_path}\\.key', 'w').write(retval)
    open(f'{dir_path}\\.keyval', 'w').write("True")
    return retval
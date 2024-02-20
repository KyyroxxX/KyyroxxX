from timeit import default_timer    # https://docs.python.org/3/library/timeit.html
from random import choice   # https://docs.python.org/3/library/random.html?highlight=random#module-random
from string import ascii_letters, digits # https://docs.python.org/3/library/string.html?highlight=string#module-string
import secrets

used_passwords = set()
used_passwords.clear()


def zip_file_path():
    return "test"    # Poner aqui que quieres descifrar.

def extraction_path():
    return "script"          
def is_max_tries_reached(tries_count, max_tries):
    return bool(tries_count == max_tries)

def generate_random_password(password_length):

    return ''.join(secrets.choice(ascii_letters) for _ in range(password_length))

def is_password_used(word):
    if word not in used_passwords:
        used_passwords.add(word)
        return False
    else:
        print("___ALREADY USED PASSWORD___")
        return True

def attempt_to_unzip(word):
    try:
        with RarFile(zip_file_path(), mode='r') as rar_file:
            rar_file.setpassword(word)
            rar_file.extractall(path=extraction_path())
        return True
    except:
        return False

def unzip_success():
    stop_time = default_timer()
    print(f"THIS OPERATION HAS TAKEN: {round(stop_time - start_time)} seconds")
    print(f"DISCOVERED AFTER {tries_count} TRIES")
    print(f"THE PASSWORD IS: {word}")
    quit()

def unzip_failure():
    stop_time = default_timer()
    print(f"THIS OPERATION HAS TAKEN: {stop_time - start_time} seconds")
    print(f"TRIED {tries_count} COMBINATIONS")
    quit()


start_time = default_timer() 
tries_count = 0 
password_length = 1  


while True:

    max_tries = (52**password_length)

    if is_max_tries_reached(tries_count, max_tries) is True:
        print("INCREASING PASSWORD RANGE")
        password_length += 1
        used_passwords.clear()    

    word = generate_random_password(password_length)
    print("Generating Password")
    print(f"Trying: {word}")

    if is_password_used(word) is True:
        continue
    else:
        print(f"Trying: {word}")
        if attempt_to_unzip(word) is True:
            unzip_success()
        else:
            tries_count += 1
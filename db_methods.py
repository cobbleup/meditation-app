import sqlalchemy as sql
import db_functions
from classes import User
import hashlib


db_functions.global_init('data/baZa.db')


db_sess = db_functions.create_session()


def get_name(id: int):
    # get user login from user id
    db = db_sess.query(User)

    if db_sess.query(sql.exists().where(User.id == id)).scalar():
        return db.filter(User.id == id).first().login
    
    else:
        return f"unable to locate user with id {id}"


def get_id(login: str):
    # get user id from login
    db = db_sess.query(User)

    if db_sess.query(sql.exists().where(User.login == login)).scalar():
        return db.filter(User.login == login).first().id
    
    else:
        return f"unable to find user with login {login}"


def add_user_data(login: str, password: str, *username):
    # new user
    user = User()
    user.login = login
    user.passwordhash = hashlib.md5(password.encode()).hexdigest()

    if username:
        user.username = username[0]

    db_sess.add(user)
    print('user added')
    

def login(login: str, password: str):
    # check password and check for profile with said login
    pw = hashlib.md5(password.encode()).hexdigest()

    if db_sess.query(sql.exists().where(User.login == login)).scalar():
        db = db_sess.query(User)
        user = db.filter(User.login == login).first()

        if user.passwordhash == pw:
            return True
        
        else:
            print('incorrect password')
            return False
    
    else:
        print(f'no user with name {login}. sign up first')
        return False


def set_username(usrlogin: str, password: str, newusername: str):

    if login(usrlogin, password):
        user = db_sess.query(User).filter(User.login == usrlogin).first()
        user.username = newusername

        db_sess.commit()
        print('username set successfully')
    
    else:
        return


def change_password(usrlogin: str, oldpassword: str, newpassword):

    if login(usrlogin, oldpassword):
        usr = db_sess.query(User).filter(User.login == usrlogin).first()
        usr.passwordhash = hashlib.md5(newpassword.encode()).hexdigest()

        db_sess.commit()
        print('password changed successfully')

    else:
        return


def add_recently_played(usrlogin: str, track_name: str):

    user = db_sess.query(User).filter(User.login == usrlogin).first()

    if user.rp:
        rp = user.rp.split()
    else:
        rp = []
    
    rp.append(track_name)
    if len(rp) > 5:
        rp = rp[1::]

    user.rp = ' '.join(rp)
    db_sess.commit()


def add_favourite(usrlogin: str, track_name: str):

    user = db_sess.query(User).filter(User.login == usrlogin).first()

    if user.favourite:
        fav = set(user.favourite.split())
    else:
        fav = set()
    
    fav.add(track_name)
    fav = ' '.join(fav)

    user.favourite = fav
    db_sess.commit()

    


# print(get_id('test1'), get_name(1))
# print(get_id('lel'), get_name(2))

set_username(input('input login: '), input('input password: '), input('input new username: '))

# change_password(input('input login: '), input('input old password: '), input('input new password: '))

# add_recently_played('me', 'rawr.xdd')

add_favourite('me', 'top10mcrsongs.mp3')

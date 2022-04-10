from database.db import DB
from user.user_details import User

class UserDal:
    def __init__(self):
        self.db = DB()
    def getUserById(self, id):
        _SQL = f"""
                SELECT * FROM users WHERE id={id}
        """
        row = self.db.do_fetch_one(_SQL)
        if row is not None:
            return User(row[0], row[1], row[2], row[3])
        else:
            return None
    
    def getUserByUsername(self, username):
        _SQL = f"""
                SELECT * FROM users WHERE username='{username}'
        """
        row = self.db.do_fetch_one(_SQL)
        if row is not None:
            return User(row[0], row[1], row[2], row[3])
        else:
            return None

    def create(self, username, password):
        _SQL = f"""
                INSERT INTO users(username, password, category) 
                values('{username}', '{password}', 0)
        """
        _lastId = self.db.do_insert(_SQL)
        self.reset_increment()
        self.db.close()
        return _lastId
    
    def update(self, username, _username, _password):
        _SQL = f"""
                UPDATE users 
                SET username='{_username}', password='{_password}' 
                WHERE username='{username}'
        """
        self.db.do_update(_SQL)
        self.db.close()
    
    def reset_increment(self):
        _SQL = "SET @num := 0"
        self.db.do_update(_SQL)
        _SQL = "UPDATE users SET id = @num := (@num+1)"
        self.db.do_update(_SQL)
        _SQL = "ALTER TABLE users AUTO_INCREMENT = 1"
        self.db.do_update(_SQL)
        self.db.close()
    

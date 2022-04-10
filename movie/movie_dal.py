from database.db import DB
from movie.movie_edit import MovEdit

class MovDal:

    def __init__(self):
        self.db = DB()

    def create(self, mov):
        _SQL = f"INSERT INTO movies(name,schedule) values('{mov.name}','{mov.schedule}')"
        _lastId = self.db.do_insert(_SQL)
        self.reset_increment()
        self.db.close()
        return _lastId
    
    def getAll(self):
        _SQL = "SELECT * FROM movies"
        rows = self.db.do_fetch_all(_SQL)
        movies = []
        for row in rows:
            movies.append(MovEdit(row[0], row[1], row[2]))

        self.db.close()
        return movies

    def getMovById(self, id):
        _SQL = f"SELECT * FROM movies WHERE id={id}"
        row = self.db.do_fetch_one(_SQL)
        if row is not None:
            mov = MovEdit(row[0], row[1], row[2])
        else:
            mov = []
        self.db.close()
        return mov
    
    def getMovByTitle(self, title):
        _SQL = f"SELECT * FROM movies WHERE name LIKE '%{title}%'"
        rows = self.db.do_fetch_all(_SQL)
        self.db.close()
        movies = []
        for row in rows:
            mov = MovEdit(row[0], row[1], row[2])
            movies.append(mov)
        return movies
    
    def getOneMovByTitle(self, title):
        _SQL = f"SELECT * FROM movies WHERE name='{title}'"
        row = self.db.do_fetch_one(_SQL)
        self.db.close()
        if row is not None:
            mov = MovEdit(row[0], row[1], row[2])
            return mov
        else:
            return None
    
    def getAllMovBySchedule(self, schedule):
        _SQL = f"SELECT * FROM movies WHERE schedule='{schedule}'"
        rows = self.db.do_fetch_all(_SQL)
        movies = []
        for row in rows:
            mov = MovEdit(row[0], row[1], row[2])
            movies.append(mov)
        self.db.close()
        return movies

    def update(self, data):
        _SQL = f"UPDATE movies SET name='{data.name}', schedule='{data.schedule}' WHERE id={data.id}"
        self.db.do_update(_SQL)
        self.db.close()

    def delete(self, id):
        _SQL = f"DELETE FROM movies WHERE id = {id}"
        self.db.do_update(_SQL)
        self.reset_increment()
        self.db.close()
        
    def validate(self, name):
        _SQL = f"SELECT * FROM movies WHERE name='{name}'"
        row = self.db.do_fetch_one(_SQL)
        if row is None:
            return True
        else:
            return False
    def reset_increment(self):
        _SQL = "SET @num := 0"
        self.db.do_update(_SQL)
        _SQL = "UPDATE movies SET id = @num := (@num+1)"
        self.db.do_update(_SQL)
        _SQL = "ALTER TABLE movies AUTO_INCREMENT = 1"
        self.db.do_update(_SQL)
        self.db.close()
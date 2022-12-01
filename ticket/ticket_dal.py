from database.db import DB
from ticket.ticket_edit import TicketEdit

class TicketDal:
    def __init__(self):
        self.db = DB()

    def create(self, mov):
        for x in range(5):
            _SQL = f"INSERT INTO tickets(movie_id, schedule, seat_code, bought) values({mov.id}, '{mov.schedule}', '{x+1}', 0)"
            _lastId = self.db.do_insert(_SQL)
            print(x)
        self.reset_increment()
        self.db.close()
        return _lastId
    
    def update(self, data):
        _SQL = f"UPDATE tickets SET bought='{data.bought}' WHERE id={data.id}"
        self.db.do_update(_SQL)
        self.db.close()
    
    def update_schedule(self, data):
        _SQL = f"UPDATE tickets SET schedule='{data.schedule}' WHERE movie_id={data.id}"
        self.db.do_update(_SQL)
        self.db.close()
    
    def delete(self, movId):
        _SQL = f"DELETE FROM tickets WHERE movie_id={movId}"
        self.db.do_update(_SQL)
        self.reset_increment()
        self.db.close()

    def getAll(self):
        _SQL = "SELECT * FROM tickets"
        rows = self.db.do_fetch_all(_SQL)
        tickets = []
        for row in rows:
            tickets.append(TicketEdit(row[0], row[1], row[2], row[3], row[4]))

        self.db.close()
        return tickets
    
    def getTicketById(self, id):
        id = int(id)
        _SQL = f"SELECT * FROM tickets WHERE id={id}"
        
        row = self.db.do_fetch_one(_SQL)
 
        ticket = TicketEdit(row[0], row[1], row[2], row[3], row[4])

        return ticket

    def getAllByMovId(self, movId):
        movId = int(movId)
        if movId != 0:
            _SQL = f"SELECT * FROM tickets WHERE movie_id={movId}"
        
        rows = self.db.do_fetch_all(_SQL)

        tickets = []
        for row in rows:
            tickets.append(TicketEdit(row[0], row[1], row[2], row[3], row[4]))

        return tickets
    
    def validate(self, movId):
        _SQL = f"SELECT * FROM tickets WHERE movie_id={movId}"
        row = self.db.do_fetch_one(_SQL)
        if row is None:
            return True
        else:
            return False

    def reset_increment(self):
        _SQL = "SET @num := 0"
        self.db.do_update(_SQL)
        _SQL = "UPDATE tickets SET id = @num := (@num+1)"
        self.db.do_update(_SQL)
        _SQL = "ALTER TABLE tickets AUTO_INCREMENT = 1"
        self.db.do_update(_SQL)
        self.db.close()
from flask import Flask, render_template, request, redirect, session, url_for, Response

from movie.movie_edit import MovEdit
from movie.movie_dal import MovDal
from ticket.ticket_dal import TicketDal
from user.user_dal import UserDal
import boto3

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
S3_BUCKET_PUBLIC = "darren-aws-project-public-bucket"
S3_BUCKET_PRIVATE = "darren-aws-project-private-bucket"
app.config['S3_KEY'] = "ASIA6Q2SL6JE6VB4YMWR"
app.config['S3_SECRET'] = "UYVgW1yKb7BjV7RtJNQQY6AtJBuycZU5ZgB9M5UP"

s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config['S3_KEY'],
    aws_secret_access_key=app.config['S3_SECRET'],
    # aws_session_token=app.config['S3_TOKEN']
)

@app.route('/download-private', methods=['POST'])
def download_private():
    filename = request.args.get("filename")
    file = s3.get_object(Bucket=f'{S3_BUCKET_PRIVATE}.s3.amazonaws.com', Key={filename})
    return Response(
        file['Body'].read(),
        mimetype='text/plain',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
        )

@app.route('/upload-public', methods=['POST'])
def success_upload_public():
    if request.method == 'POST':
        f = request.files['file']

        if f.filename == "":
            return "Please select a file"

        # Uncomment to find your file is stored in disk
        # f.save(f.filename)

        file_url = upload_file_to_s3(f, S3_BUCKET_PUBLIC, 'public-read')
        # file_url = "None"

        return render_template(
            "home.html", user=None
        )

@app.route('/upload-private', methods=['POST'])
def success_upload_private():
    if request.method == 'POST':
        f = request.files['file']

        if f.filename == "":
            return "Please select a file"

        # Uncomment to find your file is stored in disk
        # f.save(f.filename)

        file_url = upload_file_to_s3(f, S3_BUCKET_PRIVATE, 'private-read')
        # file_url = "None"

        return render_template(
            "home.html", user=None
        )


def upload_file_to_s3(file, bucket_name, acl):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        app.config['S3_BUCKET'] = bucket_name
        app.config['S3_LOCATION'] = f'{bucket_name}.s3.amazonaws.com/img'
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type  # Set appropriate content type as per the file
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(app.config["S3_LOCATION"], file.filename)


@app.route('/')
@app.route('/home')
def home():
    if 'user' in session:
        user = session['user']
    else:
        user = None 
    return render_template('home.html', user=user)

@app.route('/login')
@app.route('/login/<cond>')
def login(cond=''):
    if cond == 'failed':
        warning = True
    elif cond == 'confirm':
        warning = -1
    else:
        warning = False
    if 'user' in session:
        user = session['user']
    else:
        user = None 
    return render_template('/user/login.html', warning=warning, user=user)

@app.route('/login/', methods=['POST'])
def login_action():
    _username = request.form['username']
    _password = request.form['pass']
    dal = UserDal()
    user = dal.getUserByUsername(_username)
    if user is not None:
        if user.getPassword() == _password:
            dict_user = user.__dict__
            session['user'] = dict_user
            user = session['user']
            if 'cart' in session:
                if 'order' in session:
                    mov_id = session['order']
                    return redirect(f'/movies/order/{mov_id}')
            return render_template('home.html', user=user)
        else:
            return redirect('/login/failed')
    else:
        return redirect('/login/failed')

@app.route('/logout')
def logout():
    session.pop('user', None)
    if 'cart' in session:
        session.pop('cart', None)
    if 'order' in session:
        session.pop('order', None)
    if 'seats' in session:
        session.pop('seats', None)
    return redirect('/home')

@app.route('/register')
@app.route('/register/<cond>')
def register(cond=''):
    if cond == 'failed':
        warning = True
    else:
        warning = False
    if 'user' in session:
        user = session['user']
    else:
        user = None 
    return render_template('/user/register.html', warning=warning, user=user)

@app.route('/register/', methods=['POST'])
def register_action():
    _username = request.form['username']
    _password = request.form['pass']
    dal = UserDal()
    user = dal.getUserByUsername(_username)
    if user is None:
        dal.create(_username, _password)
        return """
                Registrasi berhasil, klik di <a href='/login'>sini</a> untuk login
        """
    else:
        return redirect('/register/failed')

@app.route('/change')
@app.route('/change/<cond>')
def change(cond=''):
    user = session['user']
    if cond == 'failed':
        warning = True
    else:
        warning = False
    return render_template('/user/change.html', warning=warning, user=user)

@app.route('/change/', methods=['POST'])
def change_action():
    user = session['user']
    _cpass = request.form['cpassword']
    _newpass = request.form['npassword']
    _newusername = request.form['nusername']
    if _newpass == '':
        _newpass = _cpass
    dal = UserDal()
    user = dal.getUserByUsername(user['username'])
    if user.getPassword() == _cpass:
        dal.update(user.username, _newusername, _newpass)
        return """
                Penggantian berhasil, klik di <a href='/login'>sini</a> untuk login ulang
        """
    else:
        return redirect('/change/failed')

@app.route('/movies')
def movies():
    if 'user' in session:
        user = session['user']
    else:
        user = None 
    dal = MovDal()
    movies = dal.getAll()
    return render_template('/movie/movie.html', movies=movies, user=user)

@app.route('/movies/search', methods=['GET'])
def movies_search():
    if 'user' in session:
        user = session['user']
    else:
        user = None 
    if request.method == "GET":
        _title = request.args['mov_title']
        dal = MovDal()
        movies = dal.getMovByTitle(_title)
    else:
        movies = []

    return render_template('/movie/movie.html', movies=movies, user=user)

@app.route('/movies/by/schedule/<schedule>')
def movies_schedule(schedule):
    if 'user' in session:
        user = session['user']
    else:
        user = None 
    dal = MovDal()
    movies = dal.getAllMovBySchedule(schedule)
    return render_template('/movie/movie.html', movies=movies, user=user)

@app.route('/admin')
def admin():
    if 'user' in session:
        user = session['user']
    else:
        user = None 
    return render_template('admin.html', user=user)

@app.route('/admin/movies')
def movies_admin():
    if 'user' in session:
        user = session['user']
    else:
        user = None 
    dal = MovDal()
    movies = dal.getAll()
    return render_template('/movie/movie_admin.html', movies=movies, user=user)

@app.route('/admin/movies/edit', defaults={'id': 0}, methods=['GET', 'POST'])
@app.route('/admin/movies/edit/<id>', methods=['GET', 'POST'])
def movie_edit(id=0):
    if 'user' in session:
        user = session['user']
    else:
        user = None 
    if request.method == 'POST':
        dal = MovDal()
        id = int(id)

        _name = request.form['name']
        _schedule = request.form['schedule']
        
        if id == 0:
            if dal.validate(_name) == True:
                movie = MovEdit(id, _name, _schedule)
                dal.create(movie)
                ticketDal = TicketDal()
                dal = MovDal()
                movie = dal.getMovByTitle(_name)[0]
                if ticketDal.validate(movie.id):
                    ticketDal.create(movie)
                else:
                    return "Tiket untuk film itu sudah ada"
                return redirect('/admin/movies')
            else:
                error = "Nama film tidak valid (sudah tersedia)" 
                return error

        else:
            prev_movie = dal.getMovById(id)
            movie = MovEdit(id, _name, _schedule)
            if movie.name != prev_movie.name:
                dal = MovDal()
                if dal.validate(movie.name) == True:

                    dal.update(movie)
                    if movie.schedule != prev_movie.schedule:
                        ticketDal = TicketDal()
                        ticketDal.update_schedule(movie)
                    return redirect('/admin/movies')
                else:
                    # Return Back with error message
                    error = "Nama film tidak valid (sudah tersedia)"   
                    return error 
            else:
                dal = MovDal()
                # Save to DB
                dal.update(movie)
                if movie.schedule != prev_movie.schedule:
                    ticketDal = TicketDal()
                    ticketDal.update_schedule(movie)
                return redirect('/admin/movies')
    else:
        # GET HTTP REQUEST
        if id == 0:
            movie = MovEdit(0, '', '')
        else:
            dal = MovDal()
            movie = dal.getMovById(id)

        return render_template('/movie/movie_edit.html', movie=movie, user=user)

@app.route('/admin/movies/delete/<id>')
def movie_delete(id):
    dal = MovDal()
    dal.delete(id)
    ticketDal = TicketDal()
    ticketDal.delete(id)

    return redirect('/admin/movies')

@app.route('/admin/tickets')
def ticket():
    if 'user' in session:
        user = session['user']
    else:
        user = None 
    dal = MovDal()
    movie = dal.getAll()
    return render_template('ticket/ticket_movielist.html', movies=movie, user=user)

@app.route('/admin/tickets/by/mov-id/<movId>')
def tickets_by_mov_id(movId):
    if 'user' in session:
        user = session['user']
    else:
        user = None 
    ticketDal = TicketDal()
    tickets = ticketDal.getAllByMovId(movId)

    return render_template('ticket/ticket_admin.html', tickets=tickets, movId=movId, user=user)

@app.route('/admin/tickets/generate/<movId>')
def generate_tickets(movId):
    movieDal = MovDal()
    movie = movieDal.getMovById(movId)
    ticketDal = TicketDal()
    if ticketDal.validate(movId):
        ticketDal.create(movie)
    else:
        return "Tiket untuk film itu sudah ada"

    return redirect(f'/admin/tickets/by/mov-id/{movId}')

@app.route('/admin/tickets/edit/<id>', methods=['GET', 'POST'])
def ticket_edit(id):
    if 'user' in session:
        user = session['user']
    else:
        user = None 
    if request.method == 'POST':
        dal = TicketDal()
        id = int(id)
        # Get FORM data
        _bought = request.form['bought']
        ticket = dal.getTicketById(id)
        ticket.bought = _bought
        dal.update(ticket)
        return redirect(f'/admin/tickets/by/mov-id/{ticket.mov_id}')

    else:
        # GET HTTP REQUEST
        dal = TicketDal()
        ticket = dal.getTicketById(id)

        return render_template('/ticket/ticket_edit.html', ticket=ticket, user=user)

@app.route('/admin/tickets/delete/<id>')
def ticket_delete(id):
    dal = TicketDal()
    dal.delete(id)
    return redirect(f'/admin/tickets/by/mov-id/{id}')

@app.route('/schedule')
def schedule():
    if 'user' in session:
        user = session['user']
    else:
        user = None 
    return render_template('schedule.html', user=user)

@app.route('/movies/order/<movId>')
def order_ticket(movId):
    if 'user' in session:
        user = session['user']
    else:
        user = None 

    if 'cart' in session:
        if session['order'] == movId:
            cart = session['cart']
        else:
            cart= []
            session['cart'] = cart
            session.pop('seats', None)
    else:
        cart = []
        session['cart'] = cart
    
    if 'seats' in session:
        selected_seats =  session['seats']
    else:
        selected_seats = []
        session['seats'] = selected_seats
    session['order'] = movId

    ticketDal = TicketDal()
    tickets = ticketDal.getAllByMovId(movId)
    movDal = MovDal()
    movie = movDal.getMovById(movId)
    return render_template('/order/order_tickets.html', tickets=tickets, cart=cart, selected_seats=selected_seats, movie=movie, user=user)

@app.route("/ticket/add/mov-id/<ticketId>")
def add_ticket(ticketId):
    cart = session['cart']
    selected_seats = session['seats']

    ticketDal = TicketDal()
    item = ticketDal.getTicketById(ticketId)
    dict_item = item.__dict__
    cart.append(dict_item)
    selected_seats.append(item.seat)
    session['seats'] = selected_seats
    session['cart'] = cart
    return redirect(f'/movies/order/{item.mov_id}')

@app.route("/ticket/remove/mov-id/<ticketId>")
def remove_ticket(ticketId):
    cart = session['cart']
    selected_seats = session['seats']
    ticketDal = TicketDal()
    item = ticketDal.getTicketById(ticketId)
    dict_item = item.__dict__
    cart.remove(dict_item)
    selected_seats.remove(item.seat)
    session['seats'] = selected_seats
    session['cart'] = cart

    return redirect(f'/movies/order/{item.mov_id}')

@app.route('/order/checkout/<id>')
def checkout(id):
    id = int(id)
    movId = session['order']
    if id == 0:
        session.pop('cart', None)
        session.pop('seats', None)
        print('ahoyyy')
        return redirect(f'/movies/order/{movId}')

    if 'user' in session:
        cart = session['cart']
        if id == 1:
            for item in cart:
                dal = TicketDal()
                ticket = dal.getTicketById(item['id'])
                ticket.bought = 1
                dal.update(ticket)
            session.pop('cart', None)
            session.pop('seats', None)
            return redirect(f'/movies/order/{movId}')
    else:
        return redirect('/login/confirm')
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
def login_sql(username, password):

    import mysql.connector
    db = mysql.connector.connect(
        host="bvwcazdymm6qdepa5rcb-mysql.services.clever-cloud.com",
        user="uuuqheofqeyxs1pa",
        passwd="vXANkayef0bL3Z2zseF5",
        database="bvwcazdymm6qdepa5rcb"
        )

    mycursor = db.cursor()
    mycursor.execute("select password from user where username= '{}';".format(username))
    check=mycursor.fetchone()

    if check==None:
        return 'invalid'
        #returns 'invalid' if username does not exist
    
    elif check[0]==password:
        return True
        #returns True if password matches

    else:
        return False
        #returns False if password does not match

def signup_sql(username, email, password):

    import mysql.connector
    import smtplib
    from email.message import EmailMessage        

    db = mysql.connector.connect(
        host="bvwcazdymm6qdepa5rcb-mysql.services.clever-cloud.com",
        user="uuuqheofqeyxs1pa",
        passwd="vXANkayef0bL3Z2zseF5",
        database="bvwcazdymm6qdepa5rcb")
    mycursor = db.cursor()

    try:
        mycursor.execute(f"insert into user values('{username}', '{email}', '{password}')")
        db.commit()
    except mysql.connector.IntegrityError:
        return False
        #returns False if username duplication occurs

    try:
        msg = EmailMessage()
        msg['Subject'] = 'FilmPy: Confirmation'
        msg['From'] = 'film.py89@gmail.com'
        msg['To'] = email
        msg.set_content(f'''\
Hello, {username.title()}!

This email is to confirm that you have successfully made an account with us (don't worry there's no button to click or link to follow).

Welcome to FilmPy, we hope you enjoy your stay here.

Thank you for using FilmPy!''')

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login('film.py89@gmail.com', 'sreeram1')
            smtp.send_message(msg)

    except smtplib.SMTPRecipientsRefused:
        mycursor.execute(f"delete from user where username='{username}'")
        db.commit()
        db.close()
        return 'invalid email'
        #returns 'invalid email' if email does not exist
 
    db.close()
    return True
    #returns True if no duplicaton occurs


def pwdrecovery_sql(username):
    try:
        import smtplib
        from email.message import EmailMessage
        import mysql.connector
        db = mysql.connector.connect(
            host="bvwcazdymm6qdepa5rcb-mysql.services.clever-cloud.com",
            user="uuuqheofqeyxs1pa",
            passwd="vXANkayef0bL3Z2zseF5",
            database="bvwcazdymm6qdepa5rcb"
            )
        mycursor = db.cursor()
        mycursor.execute(f"select email, password from user where username='{username}';") 
        creds = mycursor.fetchone()
        db.close()

        if creds == None:
            #Returns False if username does not exist
            return False
        else:
            email, password = creds
    
        msg = EmailMessage()
        msg['Subject'] = 'FilmPy: Password Recovery'
        msg['From'] = 'film.py89@gmail.com'
        msg['To'] = email
        msg.set_content(f'''\
Hello, {username.title()}!

Your Password is: {password}

Thank you for using FilmPy!''')

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login('film.py89@gmail.com', 'sreeram1')
            smtp.send_message(msg)

        #Returns True if email is successful
        return True

    except:
        pass 

def reviewwrite_sql(username, movieid, review, rating):
    
    import mysql.connector
    import imdb
    
    db=mysql.connector.connect(
        host="bvwcazdymm6qdepa5rcb-mysql.services.clever-cloud.com",
        user="uuuqheofqeyxs1pa",
        passwd="vXANkayef0bL3Z2zseF5",
        database="bvwcazdymm6qdepa5rcb"
        )
    mycursor = db.cursor()
    
    ia = imdb.IMDb().get_movie(movieid)
    imgurl, title = ia.get('full-size cover url',""), ia.get('title')
    
    def tosql(str):
        return str.replace('"' , '####').replace("'" , '$$$$')

    review = tosql(review)
    title = tosql(title)

    query1 = f'''insert into review values(
    '{username}{movieid}',
    '{username}',
    '{movieid}',
    '{review}',
    {rating},
    convert_tz(now(), '+00:00', '+05:30'),
    '{imgurl}',
    '{title}'
    )'''

    
    query2 = f'''update review set
    review='{review}',
    rating='{rating}',
    datetime = convert_tz(now(), '+00:00', '+05:30')
    where reviewid='{username}{movieid}'
    '''


    try:
        mycursor.execute(query1)
        db.commit()
        return True
        #returns True if everything is successful
    
    except mysql.connector.IntegrityError:
        mycursor.execute(query2)
        db.commit()
        return True
    
    except mysql.connector.DataError:
        return 'out of bounds'
        #returns 'out of bounds' if review exceeds 1100 characters

    db.close()

def moviedesc_sql(movieid,chars = 1000):

    import imdb
    ia = imdb.IMDb()
    mov = ia.get_movie(movieid)
    dictt={}
    cast=[]

    for i in ['genres', 'plot outline', 'title', 'year', 'director', 'full-size cover url']:
        dictt[i] = mov.get(i, "-")

    if len(dictt['plot outline']) > 1000:
        dictt['plot outline'] = dictt['plot outline'][:chars] + '...'
        
    if mov.get('cast') != None:
        for i in mov.get('cast')[0:9]:
            cast.append(i.get('name', "-"))
    else:
        cast.append("-")

    dictt['director'] = mov.get('director', "-")
    if dictt['director'] != "-":
        dictt['director'] = dictt['director'][0]['name']
    
    dictt['cast'] = cast
    return dictt

def getbymovie_sql(movieid):

    import mysql.connector
    import datetime
    
    db = mysql.connector.connect(
        host="bvwcazdymm6qdepa5rcb-mysql.services.clever-cloud.com",
        user="uuuqheofqeyxs1pa",
        passwd="vXANkayef0bL3Z2zseF5",
        database="bvwcazdymm6qdepa5rcb"
        )

    mycursor = db.cursor()
    mycursor.execute(f"select username, rating, review, datetime, imgurl, title from review where movieid = '{movieid}';")
    revs = mycursor.fetchall()
    reviews=[]

    def fromsql(str):
        return str.replace('####','"').replace('$$$$',"'").replace('\n', " ")
    
    for rev in revs:
        revd = dict(zip(('username', 'rating', 'review', 'title') , (rev[0], rev[1], fromsql(rev[2]), fromsql(rev[5]))))
        revd['datetime'] = rev[3].strftime('%H:%M %d-%m-%Y')
        revd['image url'] = rev[4]
        reviews.append(revd)
    return reviews

def getbyuser_sql(username):

    import mysql.connector
    import datetime
    
    db = mysql.connector.connect(
        host="bvwcazdymm6qdepa5rcb-mysql.services.clever-cloud.com",
        user="uuuqheofqeyxs1pa",
        passwd="vXANkayef0bL3Z2zseF5",
        database="bvwcazdymm6qdepa5rcb"
        )

    mycursor = db.cursor()
    mycursor.execute(f"select username, rating, review, datetime, imgurl, title from review where username = '{username}';")
    revs = mycursor.fetchall()
    reviews=[]

    def fromsql(str):
        return str.replace('####','"').replace('$$$$',"'").replace('\n', " ")
    
    for rev in revs:
        revd = dict(zip(('username', 'rating', 'review', 'title') , (rev[0], rev[1], fromsql(rev[2]), fromsql(rev[5]))))
        revd['datetime'] = rev[3].strftime('%H:%M %d-%m-%Y')
        revd['image url'] = rev[4]
        reviews.append(revd)
    return reviews

def getrandom_sql(m=4):
    
    from random import randint
    import mysql.connector
    import datetime
    
    db = mysql.connector.connect(
        host="bvwcazdymm6qdepa5rcb-mysql.services.clever-cloud.com",
        user="uuuqheofqeyxs1pa",
        passwd="vXANkayef0bL3Z2zseF5",
        database="bvwcazdymm6qdepa5rcb"
        )
    
    mycursor = db.cursor()
    mycursor.execute(f"select username, rating, review, datetime, imgurl, title from review")
    revs = mycursor.fetchall()
    reviews=[]

    def fromsql(str):
        return str.replace('####','"').replace('$$$$',"'").replace('\n', " ")

    for i in range(m):
        if len(revs) == 0:
            break
        n = randint(0, len(revs)-1)
        rev = revs.pop(n)
        revd = dict(zip(('username', 'rating', 'review', 'title') , (rev[0], rev[1], fromsql(rev[2]), fromsql(rev[5]))))
        revd['datetime'] = rev[3].strftime('%H:%M %d-%m-%Y')
        revd['image url'] = rev[4]
        reviews.append(revd)

    return reviews

def search_sql(query):    
    import imdb
    ia = imdb.IMDb()
    search = ia.search_movie(query, results=5)
    lst=[]    
    for movie in search:
        dct={}        
        if movie['kind']=='movie':            
            for i in ['title', 'year', 'full-size cover url']:            
                try:
                    dct[i] = movie[i]
                except KeyError:
                    dct[i] = None
                    #Value for respective key is None if information does not exist
                dct['movieid']=movie.getID()                
            lst.append(dct)            
    return lst

def maingenres_sql(username, genres):
    import mysql.connector
    db = mysql.connector.connect(
        host="bvwcazdymm6qdepa5rcb-mysql.services.clever-cloud.com",
        user="uuuqheofqeyxs1pa",
        passwd="vXANkayef0bL3Z2zseF5",
        database="bvwcazdymm6qdepa5rcb"
        )
    mycursor = db.cursor()

    query = f"insert into genres(username) values('{username}')"
    mycursor.execute(query)
    db.commit()
    
    for genre in genres:
        genre = genre.replace('-', '_')
        query = f"update genres set {genre} = {genre} + 10 where username = '{username}'"
        mycursor.execute(query)
        db.commit()
    db.close()

def reviewgenres_sql(username, movieid, rating):
    import mysql.connector
    import imdb

    db=mysql.connector.connect(
        host="bvwcazdymm6qdepa5rcb-mysql.services.clever-cloud.com",
        user="uuuqheofqeyxs1pa",
        passwd="vXANkayef0bL3Z2zseF5",
        database="bvwcazdymm6qdepa5rcb"
        )    
    mycursor = db.cursor()

    gens = ['DRAMA', 'CRIME', 'ACTION','THRILLER',
            'BIOGRAPHY', 'HISTORY', 'SPORT',
            'ADVENTURE', 'FANTASY', 'WESTERN',
            'ROMANCE', 'SCI-FI', 'MYSTERY',
            'HORROR', 'FAMILY', 'COMEDY',
            'WAR', 'ANIMATION', 'MUSIC',
            'MUSICAL', 'FILM-NOIR', 'DOCUMENTARY']

    ia = imdb.IMDb()    
    genres = ia.get_movie(movieid)['genres']

    for genre in genres:
        if genre.upper() in gens:
            genre = genre.replace('-', '_')
            points = rating - 5
            query = f"update genres set {genre} = {genre} + {points} where username = '{username}';"
            mycursor.execute(query)
            db.commit()

    db.close()

def suggest_sql(username, file, k=3):
    
    import mysql.connector
    import pickle
    import imdb
    from random import randint
    
    db = mysql.connector.connect(
        host="bvwcazdymm6qdepa5rcb-mysql.services.clever-cloud.com",
        user="uuuqheofqeyxs1pa",
        passwd="vXANkayef0bL3Z2zseF5",
        database="bvwcazdymm6qdepa5rcb"
        )
    mycursor = db.cursor()

    #getting points from sql
    query = f"select * from genres where username = '{username}';"
    mycursor.execute(query)
    points = mycursor.fetchone()

    #getting column names from sql
    query2 = "desc genres;"
    mycursor.execute(query2)
    table = mycursor.fetchall()

    #wrapping as a dict
    gen = []
    for col in table:
        gen.append(col[0])
    genretemp=dict(zip(gen[1:], points[1:]))

    #removing genres with points = 0
    genres = dict(genretemp)
    for g in genretemp:
        if genretemp[g] == 0:
            del genres[g]

    #gettiing dataset from local file
    with open(file, 'rb') as f:
        dataset = pickle.load(f)

    #comparing dataset with genres
    result = []
    
    for m_id in dataset: #parsing dataset
        result.append([0,m_id])
        
        for genr in dataset[m_id]: #travelling through genres
            genfixed = genr.upper().replace('-' , '_')
            
            if genfixed in genres: #matching genres
                result[-1][0] += genres[genfixed]
                
        result.sort(reverse = True)
        if len(result)>10:
            del result[10]

    suggests = []
    for p in range(k):
        n = randint(0,len(result)-1)
        suggests.append(result.pop(n)[1])

    return suggests
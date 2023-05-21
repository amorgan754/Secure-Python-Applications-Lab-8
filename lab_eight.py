"""This project is to show the use of html code within python"""

#imports
from datetime import datetime
import re
import sqlite3 as sql
from flask import Flask, request, render_template, redirect


CURRENTDATE = datetime.now()


connection = sql.connect('database', check_same_thread=False)
cur = connection.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users ([username] VARCHAR2(30), [password]
    VARCHAR2(30))''')
cur.execute('''INSERT INTO user VALUES ('admin', 'admin')''')
connection.commit()

app = Flask(__name__)


CommonPasswords = ["password", "123456", "12345678", "1234", "qwerty", "12345",
"dragon", "baseball", "football", "letmein", "monkey", "abc123", "mustang", "michael",
"shadow", "master", "jennifer", "111111", "2000", "jordan", "superman", "harley", "1234567",
"hunter", "trustno1", "ranger", "buster", "thomas","robert", "soccer", "batman", "test", "pass",
"killer", "hockey", "george", "charlie", "andrew", "michelle", "love", "sunshine", "jessica",
"pepper", "daniel", "access", "123456789", "654321","joshua", "maggie", "starwars", "silver",
"william", "dallas", "yankees", "123123", "ashley", "666666", "hello", "amanda", "orange",
"biteme", "freedom", "computer", "sexy", "thunder", "nicole", "ginger", "heather", "hammer",
"summer", "corvette", "taylor", "austin", "1111", "merlin", "matthew", "121212", "golfer",
"cheese", "princess", "martin", "chelsea", "patrick", "richard", "diamond", "yellow", "bigdog",
"secret", "asdfgh", "sparky", "cowboy", "camaro", "anthony",  "matrix", "falcon", "iloveyou",
"bailey", "guitar", "jackson", "purple", "scooter", "phoenix", "aaaaaa", "morgan", "tigers",
"porsche", "mickey", "maverick", "cookie", "nascar", "peanut", "justin", "131313" ,"money",
"samantha", "steelers", "joseph", "snoopy", "boomer", "whatever", "iceman", "smokey", "gateway",
"dakota", "cowboys", "eagles", "chicken", "black", "zxcvbn", "please", "andrea", "ferrari",
"knight", "hardcore", "melissa", "compaq", "coffee", "booboo", "johnny", "bulldog", "xxxxxx",
"welcome", "james", "player", "ncc1701", "wizard", "scooby", "charles", "junior", "internet",
"mike", "brandy", "tennis", "banana", "monster", "spider", "lakers", "miller", "rabbit", "enter",
"mercedes", "brandon", "steven", "fender", "john", "yamaha", "diablo", "chris", "boston", "tiger",
"marine", "chicago", "rangers", "gandalf", "winter", "barney", "edward", "raiders", "badboy",
"spanky", "bigdaddy", "johnson", "chester", "london", "midnight", "blue", "fishing", "0",
"hannah", "slayer", "11111111", "rachel", "redsox", "thx1138", "asdf", "marlboro", "panther",
"zxcvbnm", "arsenal", "oliver", "qazwsx", "mother", "victoria", "7777777", "jasper", "angel",
"david", "winner", "crystal", "golden", "butthead", "viking", "jack", "iwantu", "shannon",
"murphy", "angels", "prince", "cameron", "girls", "madison", "wilson", "carlos", "willie",
"startrek", "captain", "maddog", "jasmine", "butter", "booger", "angela", "golf", "lauren",
"rocket", "tiffany", "theman", "dennis", "liverpoo", "flower", "forever", "green", "jackie",
"muffin", "turtle", "sophie", "danielle", "redskins", "toyota", "jason", "sierra", "winston",
"debbie", "giants", "packers", "newyork", "jeremy", "casper", "bubba", "112233", "sandra", "lovers",
"mountain", "united", "cooper", "driver", "tucker", "helpme", "pookie", "lucky", "maxwell",
"8675309", "bear", "gators", "5150", "222222", "jaguar", "monica", "fred", "happy",
"hotdog", "gemini", "lover","xxxxxxxx", "777777", "canada", "nathan", "victor", "florida",
"88888888", "nicholas", "rosebud", "metallic", "doctor", "trouble", "success", "stupid",
"tomcat", "warrior", "peaches", "apples", "fish", "qwertyui", "magic", "buddy", "dolphins",
"rainbow", "gunner", "987654", "freddy", "alexis", "braves", "2112", "1212", "cocacola", "xavier",
"dolphin", "testing", "bond007", "member", "calvin", "voodoo", "7777", "samson", "alex", "apollo",
"fire", "tester", "walter", "beavis", "voyager", "bonnie", "rush2112", "beer", "apple", "scorpio",
"jonathan", "skippy", "sydney", "scott", "red123", "power", "gordon", "travis", "beaver", "star",
"jackass", "flyers", "232323", "zzzzzz", "steve", "rebecca", "scorpion", "doggie", "legend",
"ou812", "yankee", "blazer", "bill", "runner", "birdie", "555555", "parker", "topgun",
"asdfasdf", "heaven", "viper", "animal", "2222", "bigboy", "4444", "arthur", "baby", "private",
"godzilla", "donald", "williams", "lifehack", "phantom", "dave", "rock", "august", "sammy", "cool",
"brian", "platinum", "jake", "bronco", "paul", "mark", "frank", "heka6w2", "copper", "billy",
"garfield", "willow", "little", "carter", "albert", "kitten", "super", "jordan23", "eagle1",
"shelby", "america", "11111", "jessie", "house", "free", "123321", "chevy", "white", "broncos",
"horney", "surfer", "nissan", "999999", "saturn", "airborne", "elephant", "marvin", "action",
"adidas", "qwert", "kevin", "1313", "explorer", "walker", "police", "christin", "december",
"benjamin", "wolf", "sweet", "therock", "king", "online", "brooklyn", "teresa", "cricket", "sharon",
"dexter", "racing", "gregory", "teens", "redwings", "dreams", "michigan", "hentai", "magnum",
"87654321", "nothing", "donkey", "trinity", "digital", "333333", "stella", "cartman", "guinness",
"123abc", "speedy", "buffalo"]


#password verification function
def passwordverification(password):
    """This function is to verify the password length and that it is not a common password"""
    if len(password) < 12:
        print("not long enough")
    elif re.search('[0-9]', password) is None:
        print("need a number")
    elif re.search('[A-Z]', password) is None:
        print("need upper number")
    elif re.search('[a-z]', password) is None:
        print("need a lower number")
    if password in CommonPasswords:
        print("It is recommended you change your password")

#username and password verification
def userverification(username, password):
    """This function is to verify a username and password in the BD"""
    cont = False
    statement = f"SELECT username from 'users' WHERE username='{username}' AND password=\
    '{password}'"
    cur.execute(statement)
    while cont is False:
        if not cur.fetchone():
            cont = False
        else:
            cont = True
    return cont

#username and password registration
def userregistration(username, password):
    """This function is to register a username and password in the DB"""
    statement = f"INSERT INTO users VALUES ('{username}', '{password}')"
    cur.execute(statement)

#password update
def password_update(username, new_password):
    """This function is to update a password in the DB"""
    statement = f"UPDATE users SET password = '{new_password}' WHERE username='{username}'"
    cur.execute(statement)



#routes to pull to the different pages

#route to home page
@app.route('/')
def home():
    """This function is to pull in the home html code"""
    return render_template('home.html')

#route to current date time page, give link to world clock
@app.route('/datetime')
def date():
    """This function is to pull in the datetime html code"""
    datenow = CURRENTDATE.today()
    return render_template('datetime.html', datetime=datenow)


#route to a dad joke, give link to daily dad jokes
@app.route('/jokes')
def jokes():
    """This function is to pull in the jokes html code"""
    return render_template('jokes.html')

#route to list of books and book pages
@app.route('/books')
def books():
    """This function is to pull the books html code"""
    return render_template('books.html')

#login page route to page with the table
@app.route('/table', methods = ["GET", "POST"])
def table():
    """This function is to go to the table after logging in"""
    if request.method == "POST":
        return redirect('/update')
    return render_template('table.html')


#route to the user registration form
@app.route('/login', methods = ["GET", "POST"])
def login():
    """This function is to pull the login html code"""
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if userverification(username, password) is True:
            return redirect('/table')
        if userverification(username, password) is False:
            return redirect('/register')
    return render_template('login.html')

#route to the user login
@app.route('/register', methods = ["GET", "POST"])
def register():
    """This function is to pull the register html code"""
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        passwordverification(password)
        userregistration(username, password)
        return redirect('/table')
    return render_template('register.html')

#route to password update
@app.route('/update', methods = ["GET", "POST"])
def update():
    """This function is to pull the update html code"""
    if request.method == "POST":
        username = request.form['username']
        new_password = request.form['NewPassword']
        passwordverification(new_password)
        password_update(username, new_password)
        return redirect('/table')
    return render_template('update.html')




if __name__ == '__main__':
    app.debug = True
    app.run()

pi_ip = '192.168.1.176' #Pi's IP address
port = '8081' #motion port

'''import RPi.GPIO as gpio
import time
    
rc = 11 #right clockwise
ra = 19 #right anticlockwise
lc = 15 #left clockwise
la = 13 #left anti-clockwise
trig = 16
echo = 18
    
def init():
    global rc,ra,lc,la,trig,echo
    gpio.setmode(gpio.BOARD)
    gpio.setup(rc, gpio.OUT)
    gpio.setup(ra, gpio.OUT)
    gpio.setup(lc, gpio.OUT)
    gpio.setup(la, gpio.OUT)  #motors
    
    gpio.setup(trig, gpio.OUT)
    gpio.setup(echo, gpio.IN) #ultrasonic sensor

init()

def distance():
    global trig, echo
    gpio.output(trig, True)
    time.sleep(0.00001)
    gpio.output(trig, False)
    
    pulse_start = time.time()
    pulse_end = time.time()

    while gpio.input(echo)==0:
        pulse_start = time.time()
    
    while gpio.input(echo)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150 #sonic speed/2- there and back

    distance = round(distance, 2)
    return distance

def stop_sense():
    stop_distance = 8 #will stop if object detected within stop_distance cm
    x = distance()
    print(x)
    if x<=stop_distance or x>1000:
        print('false')
        return False
    else:
        print('true')
        return True

def clean():
    global rc,ra,la,lc
    gpio.output([rc,ra,la,lc],False)
    
def forward(sec):
    global rc,ra,la,lc
    if not stop_sense(): return False
    else:
        gpio.output([rc,lc], True)
        gpio.output([ra,la], False)
        time.sleep(sec)
        clean()
    
def backward(sec):
    global rc,ra,la,lc
    if not stop_sense(): return False
    else:
        gpio.output([ra,la], True)
        gpio.output([rc,lc], False)
        time.sleep(sec)
        clean()

def right(sec):
    global rc,ra,la,lc
    if not stop_sense(): return False
    else:
        gpio.output([ra,lc], True)
        gpio.output([rc,la], False)
        time.sleep(sec)
        clean()

def left(sec):
    global rc,ra,la,lc
    if not stop_sense(): return False
    else:
        gpio.output([la,rc], True)
        gpio.output([lc,ra], False)
        time.sleep(sec)
        clean()

init()
'''
from flask import Flask, url_for, flash, redirect, render_template, request
import socket

my_ip = socket.gethostbyname(socket.gethostname())
app = Flask(__name__)
app.secret_key = 'afkjajdkfaldsfynchuerieruf'

def check():
    global logged_in, ips
    if logged_in and (request.remote_addr in ips) and not locked_out:
        return True
    return False
    
attempts = 0 #password attempts
logged_in = False
locked_out = False
ips= []

@app.route("/")
def index():
    global pi_ip,port
    x='http://'+pi_ip+':'+port
    print(x)
    if not check():
        return redirect(url_for('login'))
    else:
        return render_template('home.html', ip=x)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global logged_in, attempts, ips
    if attempts >=5:
        locked_out = True
        return '<h1>Too many failed password attempts: locked out. Please restart the script to end lockout.</h1>'
        
    elif request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            flash('Invalid Credentials. Please try again.')
            print('Incorrect password')
            attempts +=1
        else:
            logged_in = True
            ips.append(request.remote_addr)
            print('Sucessful login')
            return redirect(url_for('index'))
        
    return render_template('login.html')

@app.route("/logout")
def logout():
    if check():
        global logged_in, attempts, ips
        attempts = 0
        logged_in = False
        ips.remove(request.remote_addr)
        return '<h1>Sucessfully logged out</h1>'
    else:
        return redirect(url_for('index'))

@app.route("/forward/", methods=['POST'])
def f():
    print('forward')
    forward(3)
    return redirect(url_for('index'))

@app.route("/backward/", methods=['POST'])
def b():
    backward(3)
    print('backward')
    return redirect(url_for('index'))

@app.route("/left/", methods=['POST'])
def l():
    left(3)
    print('left')
    return redirect(url_for('index'))

@app.route("/right/", methods=['POST'])
def r():
    right(3)
    print('right')
    return redirect(url_for('index'))





if __name__ == '__main__':
    app.run(host=my_ip, port=5000)

gpio.cleanup()

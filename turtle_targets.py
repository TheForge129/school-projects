import turtle
import random
import json
import os
from datetime import datetime, timezone
import zlib

#wip code block to generate and write json settings file

try:
	settingsfile=open(os.path.join('c:\\users',os.getlogin(),'appdata\\local\\turtletargets\\settings.json'),"r+") #tries to open settings file
except:
	try:
		os.mkdir(os.path.join('c:\\users',os.getlogin(),'appdata\\local\\turtletargets')) #generates folder in c:\users\(username)\appdata
    except:
        print("appdata/local/turtletargets already exists apparently, yet the settings file does not. creating file.")
    settingsfile=open(os.path.join('c:\\users',os.getlogin(),'appdata\\local\\turtletargets\\settings.json'),"xr+") #creates settings file
    settings={
                "time": 30
            }
    settingsfile.write(json.dumps(settings, indent=4))

try:
    settings=json.loads(settingsfile.read()) #loads settings as dict
except:
    settingsfile.truncate(0) #deleting data in settings file if invalid
    settingsfile.seek(0) #reset cursor pos
    print("Settings JSON is invalid; deleting and resetting...")
    settings={
                "time": 30
            }
    settingsfile.write(json.dumps(settings))

try:
    scorefile=open(os.path.join('c:\\users',os.getlogin(),'appdata\\local\\turtletargets\\highscores'),"r+b") #tries to open score file
    decompressedscore=zlib.decompress(scorefile.read()) #decompressing
except:
    try:
        os.mkdir(os.path.join('c:\\users',os.getlogin(),'appdata\\local\\turtletargets')) #generates folder in c:\users\(username)\appdata
    except:
        print("appdata/local/turtletargets already exists apparently, yet the highscores file does not. You have clearly messed with it in some way. How dare you.") #detects and calls out the user for tampering with the files. callout is mostly included as a joke, as there are no actual anti-tamper measures. thinking about implementing some sort of encryption/decryption algorithm to prevent highscore fudging, but that can wait. (addendum 11:41 PM 10/29/2023: the score file is now compressed which should obfuscate things enough that people just don't feel like cheating.)
    scorefile=open(os.path.join('c:\\users',os.getlogin(),'appdata\\local\\turtletargets\\highscores'),"x") #creates highscore file
    scorefile.close #closes the highscore file
    scorefile=open(os.path.join('c:\\users',os.getlogin(),'appdata\\local\\turtletargets\\highscores'),"r+b") #opens hs file to modify

try:
    scorehistory=json.loads(decompressedscore) #loads scores as dict
except: 
    scorefile.truncate(0) #deleting data in scorefile if invalid
    scorefile.seek(0) #reset cursor pos
    print("Scorefile is invalid; deleting...") #status message
    scorehistory={} #creating dummy dictionary

activetarget = turtle.Turtle("turtle") #everything from here to line 91 is just initializing stuff
oldtargets = turtle.Turtle("turtle")
scoredisplay = turtle.Turtle("turtle")
timerdisplay = turtle.Turtle("turtle")
borders = turtle.Turtle("turtle")
highscoredisplay = turtle.Turtle("turtle")

activetarget._delay(0)
activetarget.resizemode("auto")
oldtargets._delay(0)
oldtargets.resizemode("auto")
scoredisplay._delay(0)
timerdisplay._delay(0)
borders._delay(0)

scoredisplay.ht()
highscoredisplay.ht()
timerdisplay.ht()
oldtargets.ht()
borders.ht()

activetarget.penup()
oldtargets.penup()
highscoredisplay.penup()

scoredisplay.setpos(350,250)
timerdisplay.setpos(-350,250)
scoredisplay.clear()
timerdisplay.clear()

activetarget.color("red")
oldtargets.color("#5f5f5f")
scoredisplay.color("white")
timerdisplay.color("white")

size=0
updatingTimer=False
timerInvalid=True

#assumes the timer is invalid
while (timerInvalid==True):
    try:
        timer=settings["time"]+1 #tries to set the timer
        if(timer<1 or int(timer)!=timer): #if it is not a positive integer
            raise Exception("Timer is not a positive integer") #it throws an exception
        break
    except:
        settingsfile.truncate(0) #deleting data in settings file
        settingsfile.seek(0) #reset cursor pos
        print("Timer setting is invalid; deleting and resetting...")
        settings={
                "time": 30
                }
        settingsfile.write(json.dumps(settings)) #resetting settings file to default
        timerInvalid=False #timer cannot be invalid anymore
score=0

try:
    turtle.bgpic(os.path.join('c:\\users',os.getlogin(),'appdata\\local\\turtletargets\\background.gif')) #checking for a background image
    turtle.bgcolor("#000000")
except:
    print("Could not find background file; using default.\nTo create a background, add an image file called background.gif to C:/users/(username)/appdata/local/turtletargets.\nDarker backgrounds are recommended.")
    turtle.bgcolor("#201717")

def writeScoreToJson():
    global scorehistory
    global scorefile
    global score
    currenttime=datetime.now(timezone.utc) #grabbing date/time in utc
    scorehistory["Achieved on " + str(currenttime.strftime("%d/%m/%Y %H:%M:%S UTC"))]=score #setting score as dictionary entry with timestamp as key
    scorefile.truncate(0) #deleting data in scorefile
    scorefile.seek(0) #resetting cursor pos
    rawscore=json.dumps(scorehistory, indent=4)
    compressedscore=zlib.compress(rawscore.encode())
    scorefile.write(compressedscore) #writing scores to file

def updateTimer():
    global highscoredisplay
    global timerdisplay
    global timer
    global activetarget
    global scoredisplay
    timerdisplay.clear() #clears old time
    timer+=-1 #increments timer
    timerdisplay.write("Timer: " + str(timer), align="center",font=("Arial", 24, "bold")) #writing new time
    if(timer>=1): #checks if the timer hits zero
        turtle.ontimer(updateTimer,t=1000)
    else: #ending game if timer=0
        activetarget.ht() #no more active target
        #try:
        writeScoreToJson() #self-explanatory
        #except:
        #    print("JSON writing failed! Please contact the author with any debug information.") #self-explanatory
        activetarget.onclick(None) # all of this (to line 159) is just displaying the writing
        scoredisplay.color("#FFFFFF")
        timerdisplay.color("#FFFFFF")
        scoredisplay.setpos(0,50)
        scoredisplay.clear()
        scoredisplay.write("Final score: " + str(score), align="center", font=("Arial", 40, "bold"))
        timerdisplay.setpos(0,150)
        timerdisplay.clear()
        timerdisplay.write("Time's Up!", align="center", font=("Arial", 40, "bold"))
        highscoredisplay.setpos(0,-50)
        highscoredisplay.color("#FFFFFF")
        highscoredisplay.write("High scores:", align="center", font=("Arial", 30, "bold"))
        displayHighScores()

def displayHighScores():
    global scorehistory
    sortedhistorydict={k: v for k, v in sorted(scorehistory.items(), key=lambda item: item[1])} #sorting dictionary; not entirely sure how it works but it does.
    highscoredisplay.setpos(0,-90)
    count=0
    while count<5:
        try: #loops to display the top 5 highest scores
            highscoredisplay.write(sortedhistorydict[max(sortedhistorydict, key=sortedhistorydict.get)],align="center",font=("Arial", 20)) #searches for the highest score and prints it
            highscoredisplay.setpos(0,highscoredisplay.ycor()-25)
            highscoredisplay.write(max(sortedhistorydict, key=sortedhistorydict.get),align="center",font=("Arial", 15)) #prints the date/time of the score just below
            del sortedhistorydict[max(sortedhistorydict, key=sortedhistorydict.get)] #removes the highest score that it just printed from the dict
            count+=1
            highscoredisplay.setpos(0,highscoredisplay.ycor()-35)
        except:
            break #stops if it can't find at least 5 scores

def updateScore():
    global scoredisplay
    global score
    scoredisplay.clear()
    scoredisplay.write("Score: " + str(score), align="center",font=("Arial", 24, "bold"))

def genNewTargets(x,y):
    global score
    global updatingTimer
    score+=1 #incrementing score
    setOldTargetPos() #calling functions
    genTarget()
    updateScore()
    if(updatingTimer==False): #initial starting of timer
        updateTimer()
        updatingTimer=True

def setOldTargetPos():
    global activetarget
    global oldtargets
    global size
    oldtargets.st()
    oldtargets.setheading(activetarget.heading())
    oldtargets.setpos(activetarget.xcor(),activetarget.ycor())
    oldtargets.turtlesize(size,size)
    oldtargets.stamp()

def genTarget():
    global activetarget
    global size
    size=float(random.randint(5,20))/10
    activetarget.turtlesize(size,size) #randomize size
    activetarget.setheading(random.randint(1, 360)) #randomize angle
    activetarget.setpos(random.randint(-280,280),random.randint(-180,180)) #randomize position

borders.color("#b0b0b0")
borders.setpos(-300,200)
borders.clear()
borders.setheading(0)
borders.forward(600)
borders.right(90)
borders.forward(400)
borders.right(90)
borders.forward(600)
borders.right(90)
borders.forward(400)

activetarget.onclick(genNewTargets)

updateScore() 

genTarget()

turtle.mainloop()

from psychopy import visual, event, core, misc
from psychopy.hardware import keyboard

import numpy
import math

#Declare global variables
RBAX = []
RBAY = []
RBBX = []
RBBY = []
freqRB = []
orientRB = []
IIAX = []
IIAY = []
IIBX = []
IIBY = []
freqII = []
orientII = []
thisCat = []
feedback = None
window = None
gabor = None
fixation = None
answer_prompt = None
correct = None
wrong = None
log_file = None
kb = None
finished_trial = 0


def RBValues():
    #Make 200 x and y coordinates for radomized Gabor patches.
    #These values come from a 1 to 100 two dimensional sampling space.
    #These will be used later in a Rule Based categorization task.
    #The categories (A and B) are defined by a vertical cut across the frequency values (x axis)

    global freqRB
    global orientRB
    global RBAX
    global RBAY
    global RBBX
    global RBBY

    #Define x (freq) and y (orientation) coordinates from a normalized sampling space for Category A
    #Sample 100 frequency values from normalized space arround a mean=30 and sd = 2.5
    RBAX = numpy.random.normal(loc=30,scale=2.5,size=100)
    #Sample 100 orientation values from normalized space arround a mean=50 and sd = 20
    RBAY = numpy.random.normal(loc=50,scale=20,size=100)

    #Define x (freq) and y (orientation) coordinates from a normalized sampling space for Category B
    #Sample 100 frequency values from normalized space arround a mean=70 and sd = 2.5
    RBBX = numpy.random.normal(loc=70,scale=2.5,size=100)
    #Sample 100 orientation values from normalized space arround a mean=50 and sd = 20
    RBBY = numpy.random.normal(loc=50,scale=20,size=100)

    #Add X and Y from each category to array with all frequency and orientation values
    freqRB = numpy.concatenate((RBAX,RBBX), axis = None)
    orientRB = numpy.concatenate((RBAY,RBBY), axis = None)

    #Randomize values for frequency and orientation
    numpy.random.shuffle(freqRB)
    numpy.random.shuffle(orientRB)

def IIValues():
    #This function rotates in 45° the x and y coordinates from the RB task to generate a diagonal cut of the sampling space.
    #These will be used later in an Information Integration categorization task.

    global RBAX
    global RBAY
    global RBBX
    global RBBY
    global IIAX
    global IIAY
    global IIBX
    global IIBY
    global freqII
    global orientII

    #Use x'=xcos(theta)-ysin(theta), and y'=ycos(theta)+xsin(theta) for the rotation
    #set value for theta
    theta = -math.pi/4

    #Rotate category A RB values for II Task
    IIAX = (RBAX*math.cos(theta))-(RBAY*math.sin(theta))
    IIAY = (RBAY*math.cos(theta))+(RBAX*math.sin(theta))

    #Rotate category B RB values for II Task
    IIBX = (RBBX*math.cos(theta))-(RBBY*math.sin(theta))
    IIBY = (RBBY*math.cos(theta))+(RBBX*math.sin(theta))


    #Rescale dimensions so all values go form 1 to 100
    #Set min and max values
    minsf = 1
    maxsf = 100
    minang = 1
    maxang = 100
    #Rescale
    IIBX = numpy.interp(IIBX, (numpy.min(IIBX), numpy.max(IIBX)), (minsf, maxsf))
    IIAX = numpy.interp(IIAX, (numpy.min(IIAX), numpy.max(IIAX)), (minsf, maxsf))
    IIAY = numpy.interp(IIAY, (numpy.min(IIAY), numpy.max(IIAY)), (minang, maxang))
    IIBY = numpy.interp(IIBY, (numpy.min(IIBY), numpy.max(IIBY)), (minang, maxang))

    #Add X and Y from each category to array with all frequency and orientation values
    freqII = numpy.concatenate((IIAX,IIBX), axis = None)
    orientII = numpy.concatenate((IIAY,IIBY), axis = None)

    #Randomize values for frequency and orientation
    numpy.random.shuffle(freqII)
    numpy.random.shuffle(orientII)

def MakeGabor(thisFreq,thisOrient):
    #Make Gabor patches that will be used later.
    #X and Y values previously generated will be fed to sf and ori parameters

    global window
    global gabor

    #units have to be 'height' so frequency is lines per stimuli.
    gabor = visual.GratingStim(window, tex='sin', mask='circle',
        size=(0.33,0.33), pos=(0,0), sf=thisFreq, ori=thisOrient, units = 'height')


def RB_Instructions():
    global window

    #Instruccions before the RB task begins
    insRB = visual.TextStim(window, height=0.7, wrapWidth=25, color='black', pos=(0, 0))
    insRB.text = 'You will be observing a series of striped circles in the center of the screen. \n \
You will have to categorize each circle by pressing keys (left or right) in your keyboard. \n \
You need to learn to categorize them correctly.\n \
At the beginning, you will not know, but you will be provided visual feedback (the words CORRECT or WRONG).\n \
This feedback will guide you in the learning process.\n \n \n \n \
Press any key to start.'

    #presents instructions and wait for a response in keyboard
    while not event.getKeys():
        insRB.draw()
        window.flip()


def II_Instructions():
    global window

    #Instruccions before the II task begins
    insII = visual.TextStim(window, height=0.7, wrapWidth=25, color='black', pos=(0, 0))
    insII.text = 'The first part of the experiment is over.\n \
You can take a break before continuing if you want. \n \n \n \
Again you will be observing a series of striped circles in the center of the screen. \n \
You will have to categorize each circle by pressing keys (left or right) in your keyboard. \n \
You need to learn to categorize them correctly.\n \
You will be provided visual feedback (the words CORRECT or WRONG).\n \
This feedback will guide you in the learning process.\n \n \n \n \
Press any key to continue.'

    #presents instructions and wait for a response in keyboard
    while not event.getKeys():
        insII.draw()
        window.flip()


def Initialize():
    global window
    global fixation
    global answer_prompt
    global correct
    global wrong
    global kb
    global log_file


    #Initialize window to be used. Opens a white full screen
    window = visual.Window(monitor="testMonitor", fullscr = True, units = 'deg', color='white')

    #Make fixation cross
    fixation = visual.ShapeStim(window, vertices=((0, -0.5), (0, 0.5), (0,0), (-0.5,0), (0.5, 0)),
        lineWidth=5,closeShape=False,lineColor="black")

    #Make text to request answer in each trial
    answer_prompt = visual.TextStim(window, height=1, wrapWidth=10, color='black', pos=(0,-6))
    answer_prompt.text = "Select 'left' or 'right'"

    #Make feedback messages
    correct = visual.TextStim(window, text='Correct!', height=1.5, wrapWidth=10, color='black', pos=(0,0))
    wrong = visual.TextStim(window, text='Wrong!', height=1.5, wrapWidth=10, color='black', pos=(0,0))

    #Initialize keyboard
    kb = keyboard.Keyboard()

    #Initialize sampling functions
    RBValues()
    IIValues()

    #Open file log
    log_file = open('logfile.csv', 'a')


def RunRBTask():
    #Run RB task presenting Gabor patches with frequency and orientation from RB values function
    #Every trial starts with a fixation cross, then presents a Gabor patch and feedback after response

    global window
    global fixation
    global gabor
    global answer_prompt
    global kb
    global correct
    global wrong
    global finished_trial
    global freqRB
    global orientRB
    global RBAX
    global RBAY
    global RBBX
    global RBBY
    global thisCat
    global feedback
    global log_file

    #clear keyboard buffer before start of task
    kb.clearEvents()


    #Set number of trials to run
    nTrials = 200

    #Pick a frequency and orientation value for each trial
    for i in range(nTrials):
        thisFreq = freqRB[i]
        thisOrient = orientRB[i]
        #Feed frequency and orientation values to Make Gabor function
        MakeGabor(thisFreq,thisOrient)

        #Save category of stimulus (A=1, B=2)
        if thisFreq in RBAX and thisOrient in RBAY:
            thisCat = 1
        elif thisFreq in RBBX and thisOrient in RBBY:
            thisCat = 2

        #Set randomizer for partial feedback
        feedback = numpy.random.random()

        #Present fixation cross for 1 sec
        fixation.draw()
        window.flip()
        core.wait(1)

        #Present Gabor with answer prompt and wait for a left, right or escape response.
        while not event.getKeys(['left', 'right', 'escape']):
            gabor.draw()
            answer_prompt.draw()
            window.flip()
            core.wait(1)

            #Check keyboard
            keys = kb.getKeys(['left','right', 'escape'])

            #Check pressed key
            for i in keys:
                response_entry = "response," #Save response
                #if left key is pressed...
                if'left' in keys:
                    response_entry += "L," #Save pressed key
                    #... and stimulus belongs to category A(1)...
                    if thisCat == 1:
                        #... save correct response
                        response_entry += "1,"
                        #present 'correct!' on 80% of correct trials
                        if feedback > 0.2:
                            response_entry += "1" #Save feedback presented
                            correct.draw()
                            window.flip()
                            core.wait(2)
                        #present 'wrong!' on 20% of correct trials
                        else:
                            response_entry += "0" #Save feedback presented
                            wrong.draw()
                            window.flip()
                            core.wait(2)

                    #... and stimulus belongs to category B(2)...
                    elif thisCat == 2:
                        #... save incorrect response
                        response_entry += "0,"
                        #present 'wrong!' on 80% of incorrect trials
                        if feedback > 0.2:
                            response_entry += "1" #Save feedback presented
                            wrong.draw()
                            window.flip()
                            core.wait(2)
                        #present 'correct!' on 20% of incorrect trials
                        else:
                            response_entry += "0" #Save feedback presented
                            correct.draw()
                            window.flip()
                            core.wait(2)

                #if right key is pressed...
                elif 'right' in keys:
                    response_entry += "R," #Save pressed key
                    #... and stimulus belongs to category A(1)...
                    if thisCat == 1:
                        #... save incorrect response
                        response_entry += "0,"
                        #present 'wrong!' on 80% of incorrect trials
                        if feedback > 0.2:
                            response_entry += "1" #Save feedback presented
                            wrong.draw()
                            window.flip()
                            core.wait(2)
                        #present 'correct!' on 20% of incorrect trials
                        else:
                            response_entry += "0" #Save feedback presented
                            correct.draw()
                            window.flip()
                            core.wait(2)

                    #... and stimulus belongs to category B(2)...
                    elif thisCat == 2:
                        #... save correct response
                        response_entry += "1,"
                        #present 'correct!' on 80% of correct trials
                        if feedback > 0.2:
                            response_entry += "1" #Save feedback presented
                            correct.draw()
                            window.flip()
                            core.wait(2)
                        #present 'wrong!' on 20% of correct trials
                        else:
                            response_entry += "0" #Save feedback presented
                            wrong.draw()
                            window.flip()
                            core.wait(2)
                #Close program whenever 'esc' key is pressed
                elif 'escape' in keys:
                    window.close() 
                    core.quit()

                #1 sec ITI
                window.flip()
                core.wait(1)

                #Count finished trial
                finished_trial += 1

                #Save trials, stimuli parameters, task, category, response and feedback to logfile
                log_file.write(str(finished_trial) + ',' + str(thisFreq) + ',' + str(thisOrient) + ',' + 'RB,1,'+ str(thisCat) + ',' + response_entry + ',' + '\n')


def RunIITask():
    #Run II task presenting Gabor patches with frequency and orientation from II values function
    #Every trial starts with a fixation cross, then presents a Gabor patch and feedback after response

    global window
    global fixation
    global gabor
    global answer_prompt
    global kb
    global correct
    global wrong
    global finished_trial
    global IIAY
    global IIAX
    global IIBX
    global IIBY
    global freqII
    global orientII
    global thisCat
    global feedback
    global log_file

    #clear keyboard buffer before start of task
    kb.clearEvents()

    #Set number of trials to run
    nTrials = 200

    #Pick a frequency and orientation value for each trial
    for i in range(nTrials):
        thisFreq = freqII[i]
        thisOrient = orientII[i]
        #Feed frequency and orientation values to Make Gabor function
        MakeGabor(thisFreq,thisOrient)

        #Save category of stimulus (A=1, B=2)
        if thisFreq in IIAX and thisOrient in IIAY:
            thisCat = 1
        elif thisFreq in IIBX and thisOrient in IIBY:
            thisCat = 2

        #Set randomizer for partial reinforcement
        feedback = numpy.random.random()

        #Present fixation cross for 1 sec
        fixation.draw()
        window.flip()
        core.wait(1)

        #Present Gabor with answer prompt and wait for a left, right or escape response.
        while not event.getKeys(['left', 'right', 'escape']):
            gabor.draw()
            answer_prompt.draw()
            window.flip()
            core.wait(1)

            #Check keyboard
            keys = kb.getKeys(['left','right','escape'])

            #Check pressed key
            for i in keys:
                response_entry = "response," #Save response
                #if left key is pressed...
                if'left' in keys:
                    response_entry += "L," #Save pressed key
                    #... and stimulus belongs to category A(1)...
                    if thisCat == 1:
                        #... save correct response
                        response_entry += "1,"
                        #present 'correct!' on 80% of correct trials
                        if feedback > 0.2:
                            response_entry += "1" #Save feedback presented
                            correct.draw()
                            window.flip()
                            core.wait(2)
                        #present 'wrong!' on 20% of correct trials
                        else:
                            response_entry += "0" #Save feedback presented
                            wrong.draw()
                            window.flip()
                            core.wait(2)

                    #... and stimulus belongs to category B(2)...
                    elif thisCat == 2:
                        #... save incorrect response
                        response_entry += "0,"
                        #present 'wrong!' on 80% of incorrect trials
                        if feedback > 0.2:
                            response_entry += "1" #Save feedback presented
                            wrong.draw()
                            window.flip()
                            core.wait(2)
                        #present 'correct!' on 20% of incorrect trials
                        else:
                            response_entry += "0" #Save feedback presented
                            correct.draw()
                            window.flip()
                            core.wait(2)
                #if right key is pressed...
                elif 'right' in keys:
                    response_entry += "R," #Save pressed key
                    #... and stimulus belongs to category A(1)...
                    if thisCat == 1:
                        #... save incorrect response
                        response_entry += "0,"
                        #present 'wrong!' on 80% of incorrect trials
                        if feedback > 0.2:
                            response_entry += "1" #Save feedback presented
                            wrong.draw()
                            window.flip()
                            core.wait(2)
                        #present 'correct!' on 20% of incorrect trials
                        else:
                            response_entry += "0" #Save feedback presented
                            correct.draw()
                            window.flip()
                            core.wait(2)
                    #... and stimulus belongs to category B(2)...
                    elif thisCat == 2:
                        #... save correct response
                        response_entry += "1,"
                        #present 'correct!' on 80% of correct trials
                        if feedback > 0.2:
                            response_entry += "1" #Save feedback presented
                            correct.draw()
                            window.flip()
                            core.wait(2)
                        #present 'wrong!' on 20% of correct trials
                        else:
                            response_entry += "0" #Save feedback presented
                            wrong.draw()
                            window.flip()
                            core.wait(2)

                #Close program whenever 'esc' key is pressed
                elif 'escape' in keys:
                    window.close() 
                    core.quit()

                #1 sec ITI
                window.flip()
                core.wait(1)

                #Count finished trial
                finished_trial += 1

                #Save trials, stimuli parameters, task, category, response and feedback to logfile
                log_file.write(str(finished_trial) + ',' + str(thisFreq) + ',' + str(thisOrient) + ',' + 'II,2,' + str(thisCat) + ',' + response_entry + ',' + '\n')


def TerminateTask():
    #Once both tasks are finished, close everything.

    global window

    log_file.close()
    window.close()
    core.quit()


Initialize()
RB_Instructions()
RunRBTask()
II_Instructions()
RunIITask()
TerminateTask()
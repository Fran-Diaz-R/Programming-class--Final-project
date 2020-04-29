from psychopy import visual, core  # import some libraries from PsychoPy
 
import numpy
import matplotlib.pyplot as plt

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

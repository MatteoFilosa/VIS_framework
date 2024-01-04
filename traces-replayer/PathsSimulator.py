import json
import random
import time
from random import choice
from re import S
from xml.dom.minidom import Element

import uuid
import numpy as np
import scipy.interpolate as si
import selenium
from matplotlib.style import use
from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        ElementNotInteractableException)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.events import (AbstractEventListener,
                                               EventFiringWebDriver)
from selenium.webdriver.support.ui import Select, WebDriverWait

#According to https://drive.google.com/drive/u/0/folders/1ARGI_CIR3V3FvrhttgFNfXWiIpaFqNeV
latencyLimits = {"click":0, "change":0, "contextmenu":0,"mousedown":0, "mouseup":1, "mouseover":0, "mouseenter":0, "mousemove":0 , "mouseleave":1 , "mouseout":1, "wheel":1, "dbclick":1}
Levels = [(0,200.0),(200.0,2000.0),(2000.0,5000.0),(5000.0,15000.0),15000.0]

def checkLevel(event,value):

    if(value < 0):
        value = 0.0
    
    numRanges = len(Levels)-1
    indexEvent = latencyLimits[event]
    rangeLimit = Levels[indexEvent]

    #print("Level index " + str(indexEvent))
    #print("numRanges " + str(numRanges))
    if(indexEvent != numRanges):
        
        calcolationUp = value - rangeLimit[1]
        calcolationDown = value - rangeLimit[0]

        #print(calcolationUp)
        #print(calcolationDown)
        if(calcolationUp <= 0 and calcolationDown >= 0):
            #print("Returning V")
            return 0

        elif(calcolationDown < 0):

            newIndex = indexEvent
            while(newIndex >=0):

                #print("Inside cycle, new index is " + str(newIndex))
                
                rangeLimit = Levels[newIndex]

                if(newIndex != numRanges):
                    
                    calcolationUp = value - rangeLimit[1]
                    calcolationDown = value - rangeLimit[0]

                    #print("CalcUp " + str(calcolationUp))
                    #print("CalcDown " + str(calcolationDown))
                    if(calcolationUp <= 0 and calcolationDown >= 0):
                        #print("Advatage of level " + str(newIndex - indexEvent))
                        return (newIndex - indexEvent)
                
                newIndex-=1

        elif(calcolationUp > 0):

            newIndex = indexEvent
            while(newIndex <= numRanges):

                #print("Inside cycle, new index is " + str(newIndex))
                
                rangeLimit = Levels[newIndex]

                if(newIndex != numRanges):
                    
                    calcolationUp = value - rangeLimit[1]
                    calcolationDown = value - rangeLimit[0]

                    #print("CalcUp " + str(calcolationUp))
                    #print("CalcDown " + str(calcolationDown))
                    if(calcolationUp <= 0 and calcolationDown >= 0):
                        #print("Violation of level " + str(newIndex - indexEvent))
                        return (newIndex - indexEvent)

                else:

                    #print("Violation of level " + str(numRanges - indexEvent))
                    return(numRanges - indexEvent)
                
                newIndex+=1

    else:

        calcolation =  value - rangeLimit

        if(calcolation > 0):
            return 0

        else:

            newIndex = indexEvent-1
            while(newIndex >=0):

                #print("Inside cycle, new index is " + str(newIndex))
                
                rangeLimit = Levels[newIndex]

                if(newIndex != numRanges):
                    
                    calcolationUp = value - rangeLimit[1]
                    calcolationDown = value - rangeLimit[0]

                    #print("CalcUp " + str(calcolationUp))
                    #print("CalcDown " + str(calcolationDown))
                    if(calcolationUp <= 0 and calcolationDown >= 0):
                        #print("Advantage of level " + str(newIndex - indexEvent))
                        return (newIndex - indexEvent)
                
                newIndex-=1

def GetPixelsBack(width):

    return -width/2

def GetPixelsToMove(width,actionType):

    divisor = None
    if(actionType == "L"):

        divisor = 1/3
    
    elif(actionType == "M"):

        divisor = 1/2

    else:

        divisor = 2/3

    pixels = int(width*divisor)
    return pixels

def PanZoom(zoomInfo,driver):
    
    actionType = zoomInfo[0]

    divisor = None
    if(actionType == "L"):

        divisor = 1/3
    
    elif(actionType == "M"):

        divisor = 1/2

    else:

        divisor = 2/3

    #Retrieve all the information for performing the panning
    height = zoomInfo[1][0]
    width = zoomInfo[1][1]

    xStart = zoomInfo[2][0]
    yStart = zoomInfo[2][1]

    xMove = zoomInfo[3][0]
    yMove = zoomInfo[3][1]

    print("StartingX: " + str(xStart) + " " + "StartingY: " + str(yStart))

    #Here we calculate the space that we have horizontally
    #and vertically in order to perform the panning
    if(xMove == "right"):

        spaceHorizontal = width - xStart
    
    else:

        spaceHorizontal = -xStart

    if(yMove == "down"):

        spaceVertical = height - yStart

    else:

        spaceVertical = -yStart

    print(element.rect)

    actions = ActionChains(driver,duration=1)
    actions.move_to_element_with_offset(element,xStart,yStart).perform()

    actions.click_and_hold()

    listMoveLatency = []

    start = time.time()
    actions.perform()
    end = time.time()

    listMoveLatency.append((end-start)*1000)
    
    moveX = int(spaceHorizontal*divisor)
    moveY = int(spaceVertical*divisor)

    xStart = 0
    yStart = 0
    while(xStart != moveX or yStart != moveY):
        
        if(xStart == moveX):

            if(yStart < moveY):
                yStart+=1
                actions.move_by_offset(0,1)
            else:
                yStart-=1
                actions.move_by_offset(0,-1)

        elif(xStart < moveX):

            if(yStart < moveY):
                yStart+=1
                xStart+=1
                actions.move_by_offset(1,1)
            elif(yStart > moveY):
                yStart-=1
                xStart+=1
                actions.move_by_offset(1,-1)
            else:
                xStart+=1
                actions.move_by_offset(1,0)

        else:

            if(yStart < moveY):
                yStart+=1
                xStart-=1
                actions.move_by_offset(-1,1)
            elif(yStart > moveY):
                yStart-=1
                xStart-=1
                actions.move_by_offset(-1,-1)
            else:
                xStart-=1
                actions.move_by_offset(-1,0)

        start = time.time()
        actions.perform()
        end = time.time()
        listMoveLatency.append((end-start)*1000)

    actions.release()

    start = time.time()
    actions.perform()
    end = time.time()

    listMoveLatency.append((end-start)*1000)

    return listMoveLatency
    
def Zoom(infoInput,driver):
    
    #Check if zoom in or zoom out
    typeZoom = infoInput[0]

    infoInput = infoInput[1]
    actionType = infoInput[0]

    xPoint=infoInput[1][0]
    yPoint=infoInput[1][1]

    print(xPoint,yPoint)

    scrollSize = None

    if(typeZoom == "in"):

        if(actionType == "L"):

            scrollSize = -200

        elif(actionType == "M"):

            scrollSize = -300
        
        else:

            scrollSize = -400
    
    else:

        if(actionType == "L"):
    
            scrollSize = 200

        elif(actionType == "M"):

            scrollSize = 300
        
        else:

            scrollSize = 400

    actions = ActionChains(driver,duration = 0)

    actions.move_to_element(element).perform()

    listWheelLatency = []

    countScroll = 0

    if(scrollSize > 0):

        while(countScroll < scrollSize):
            actions.scroll(xPoint,yPoint,0,10)

            start = time.time()
            actions.perform()
            end = time.time()

            listWheelLatency.append((end-start)*1000)

            countScroll+=10

    else:

        while(countScroll > scrollSize):
            actions.scroll(xPoint,yPoint,0,-10)

            start = time.time()
            actions.perform()
            end = time.time()

            listWheelLatency.append((end-start)*1000)

            countScroll-=10

    return listWheelLatency

def Input(infoInput,driver):
    
    actionType = infoInput[1]

    if(infoInput[0] == "range"):

        tupleInfo = infoInput[2]

        pixelsOffsetBack = GetPixelsBack(tupleInfo[2])

        pixelsOffset = GetPixelsToMove(tupleInfo[2],actionType)

        actions = ActionChains(driver,duration=1)

        actions.move_to_element(element).click_and_hold().release().perform()

        pixelStart = 0
        while(pixelStart>int(pixelsOffsetBack)):
            pixelStart +=-1
            actions.click_and_hold().move_by_offset(-1,0).perform()

        
        actions.click_and_hold()

        pixelStart=0

        listMoveLatency = []

        start = time.time()
        actions.perform()
        end = time.time()

        listMoveLatency.append((end-start)*1000)

        while(pixelStart<int(pixelsOffset)):
            pixelStart+=1
            actions.click_and_hold().move_by_offset(1,0)

            start = time.time()
            actions.perform()
            end = time.time()

            listMoveLatency.append((end-start)*1000)

        actions.release()

        start = time.time()
        actions.perform()
        end = time.time()

        return listMoveLatency

    elif(infoInput[0] == "number"):

        element.clear()

        start = time.time()
        element.send_keys(str(infoInput[1]))
        element.send_keys(Keys.ENTER)
        end = time.time()

    elif(infoInput[0] == "checkbox" or infoInput[0] == "radio"):

        actions = ActionChains(driver,duration = 0)

        actions.move_to_element(element).perform()

        actions.click()
        
        start = time.time()
        actions.perform()
        end = time.time()
    
    return end-start

def Mouseout(driver):

    actions = ActionChains(driver,duration=0)

    actions.move_to_element(element).perform()


    mouseOutElement = driver.find_element(By.CSS_SELECTOR,"body")
    #Move to the 1,1 point of the HTML/BODY
    actions.move_to_element(mouseOutElement)
    
    start = time.time()
    actions.perform()
    end = time.time()

    return (end-start) - timeOut

def Mousemove(infoInput,driver):

    listLatency = []

    if(infoInput!=None):

        offSetWidth = infoInput[0]
        offSetHeight = infoInput[1]

        actions = ActionChains(driver,duration=1)

        actions.move_to_element(element).perform()

        xStart = 0
        yStart = 0
        while(xStart != offSetWidth or yStart != offSetHeight):
            
            if(xStart == offSetWidth):

                if(yStart < offSetHeight):
                    yStart+=1
                    actions.move_by_offset(0,1)
                else:
                    yStart-=1
                    actions.move_by_offset(0,-1)

            elif(xStart < offSetWidth):

                if(yStart < offSetHeight):
                    yStart+=1
                    xStart+=1
                    actions.move_by_offset(1,1)
                elif(yStart > offSetHeight):
                    yStart-=1
                    xStart+=1
                    actions.move_by_offset(1,-1)
                else:
                    xStart+=1
                    actions.move_by_offset(1,0)

            else:

                if(yStart < offSetHeight):
                    yStart+=1
                    xStart-=1
                    actions.move_by_offset(-1,1)
                elif(yStart > offSetHeight):
                    yStart-=1
                    xStart-=1
                    actions.move_by_offset(-1,-1)
                else:
                    xStart-=1
                    actions.move_by_offset(-1,0)

            start = time.time()
            actions.perform()
            end = time.time()
            listLatency.append((end-start)*1000)

    return listLatency


def Mouseover(driver):

    actions = ActionChains(driver)

    #It's like a jump
    actions.move_to_element(element)

    start = time.time()
    actions.perform()
    end = time.time()     

    return (end-start) - 0.250

def Click(clickInfo,driver):

    if(clickInfo == None):

        actions = ActionChains(driver,duration = 0)
        
        actions.move_to_element(element).perform()

        actions.click()

        #Then we perform the click on that element

        try:

            start = time.time()
            element.click()
            end = time.time()
        
        except ElementClickInterceptedException:

            print("Exception")

            start = time.time()
            actions.perform()
            end = time.time()

        except:

            start=0
            end=0
        

    else:

        actions = ActionChains(driver, duration = 0)

        #At first we go on the element
        actions.move_to_element_with_offset(element,clickInfo[0],clickInfo[1]).perform()
        
        actions.click()
        
        #Then we perform the click on that element
        start = time.time()
        actions.perform()
        end = time.time()

    #Return the latency time
    return (end-start)

def doubleClick(clickInfo,driver):

    if(clickInfo == None):

        actions = ActionChains(driver,duration = 0)
        
        actions.move_to_element(element).perform()

        actions.doubleClick()

        #Then we perform the click on that element

        try:

            start = time.time()
            element.doubleClick()
            end = time.time()
        
        except ElementClickInterceptedException:

            print("Exception")

            start = time.time()
            actions.perform()
            end = time.time()

        except:

            start=0
            end=0
        

    else:

        actions = ActionChains(driver, duration = 0)

        #At first we go on the element
        actions.move_to_element_with_offset(element,clickInfo[0],clickInfo[1]).perform()
        
        actions.click()
        
        #Then we perform the click on that element
        start = time.time()
        actions.perform()
        end = time.time()

    #Return the latency time
    return (end-start)

def ContextClick(clickInfo,driver):
    
    actions = ActionChains(driver, duration = 0)

    if(clickInfo == None):
        
        actions.move_to_element(element).perform()

    else:

        #At first we go on the element
        actions.move_to_element_with_offset(element,clickInfo[0],clickInfo[1]).perform()
        
    
    actions.context_click()

    try:

            #Then we perform the click on that element
            start = time.time()
            actions.perform()
            end = time.time()

    except:

            start=0
            end=0

    #Return the latency time
    return (end-start)

def Brush(infoBrush,driver):
    
    Start = infoBrush[0]
    End = infoBrush[1]

    print("Start: ", Start)
    print("End: ", End)

    xStart = Start[0]
    yStart = Start[1]

    print("xStart: ", xStart)
    print("yStart: ", yStart)

    xEnd = End[0]
    yEnd = End[1]

    print("xEnd: ", xEnd)
    print("yEnd: ", yEnd)

    listMoveLatency = []

    actions = ActionChains(driver,duration=1)

    actions.move_to_element_with_offset(element,xStart,yStart).perform()
    
    actions.click_and_hold()
    
    start = time.time()
    actions.perform() 
    end = time.time()

    listMoveLatency.append((end-start)*1000)

    if(xStart != xEnd and yStart != yEnd):

        while(xStart<xEnd and yStart<yEnd):
            xStart+=1
            yStart+=1
            actions.move_by_offset(1,1)

            start = time.time()
            actions.perform()
            end = time.time()
            
            listMoveLatency.append((end-start)*1000)

    #This is the case in which we move only in the "x" direction
    elif(xStart != xEnd and yStart == yEnd):

        while(xStart<xEnd):
            xStart+=1
            actions.move_by_offset(1,0)

            start = time.time()
            actions.perform()
            end = time.time()
            
            listMoveLatency.append((end-start)*1000)

    #Case in which we move only in the "y" direction
    else:
        while(yStart<yEnd):
            yStart+=1
            actions.move_by_offset(0,1)

            start = time.time()
            actions.perform()
            end = time.time()
            
            listMoveLatency.append((end-start)*1000)

    actions.release()
    
    start = time.time()
    actions.perform()
    end = time.time()

    listMoveLatency.append((end-start)*1000)
    #In order to refresh the brush
    #actions.move_to_element_with_offset(element,0,0).click().release().perform()

    return listMoveLatency

def PanBrush(infoPan,driver):

    newBrushAfterPan = infoPan[1]
    infoPan = infoPan[0]
    

    width = infoPan[4]
    height = infoPan[5]

    xMiddleBrush = infoPan[2]
    yMiddleBrush = infoPan[3]

    print("infoPan",infoPan)
    print("newBrushAfterPan",newBrushAfterPan)
    print("xMiddleBrush",xMiddleBrush)
    print("yMiddleBrush",yMiddleBrush)
    print("width",width)
    print("height",height)


    actions = ActionChains(driver,duration=1)

    listLatency = []

    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,pathElement)))

    #actions.move_to_element_with_offset(element,0,0).perform()
    actions.move_to_element_with_offset(element,xMiddleBrush,yMiddleBrush).perform()
    
    actions.click_and_hold()

    start = time.time()
    actions.perform()
    end = time.time()
    listLatency.append((end-start)*1000)

    moveX = infoPan[0]
    moveY = infoPan[1]

    xStart = 0
    yStart = 0
    while(xStart != moveX or yStart != moveY):
        
        if(xStart == moveX):

            if(yStart < moveY):
                yStart+=1
                actions.move_by_offset(0,1)
            else:
                yStart-=1
                actions.move_by_offset(0,-1)

        elif(xStart < moveX):

            if(yStart < moveY):
                yStart+=1
                xStart+=1
                actions.move_by_offset(1,1)
            elif(yStart > moveY):
                yStart-=1
                xStart+=1
                actions.move_by_offset(1,-1)
            else:
                xStart+=1
                actions.move_by_offset(1,0)

        else:

            if(yStart < moveY):
                yStart+=1
                xStart-=1
                actions.move_by_offset(-1,1)
            elif(yStart > moveY):
                yStart-=1
                xStart-=1
                actions.move_by_offset(-1,-1)
            else:
                xStart-=1
                actions.move_by_offset(-1,0)

        start = time.time()
        actions.perform()
        end = time.time()
        listLatency.append((end-start)*1000)


    actions.release()

    start = time.time()
    actions.perform()
    end = time.time()

    listLatency.append((end-start)*1000)

    #print("Panning... " + str(moveX) + " " + str(moveY))

    #This part of the code is useful to cancel the brushed zone and prepare a new brush
    listExcludeX = []
    listExcludeY = []

    for i in range(int(newBrushAfterPan[0][0]),int(newBrushAfterPan[1][0])):
        listExcludeX.append(i)

    for j in range(int(newBrushAfterPan[0][1]),int(newBrushAfterPan[1][1])):
        listExcludeY.append(j)

    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,pathElement)))

    if(element.rect["x"] < 0):

        if(element.rect["y"] < 0):

            xWhereClick = choice(list(set([x for x in range(-element.rect["x"],int(width))]) - set(listExcludeX)))
            yWhereClick = choice(list(set([x for x in range(-element.rect["y"],int(height))]) - set(listExcludeY)))

        else:

            xWhereClick = choice(list(set([x for x in range(-element.rect["x"],int(width))]) - set(listExcludeX)))
            yWhereClick = choice(list(set([x for x in range(1,int(height))]) - set(listExcludeY)))

    else:

        if(element.rect["y"] < 0):

            xWhereClick = choice(list(set([x for x in range(1,int(width))]) - set(listExcludeX)))
            yWhereClick = choice(list(set([x for x in range(-element.rect["y"],int(height))]) - set(listExcludeY)))

        else:

            xWhereClick = choice(list(set([x for x in range(1,int(width))]) - set(listExcludeX)))
            yWhereClick = choice(list(set([x for x in range(1,int(height))]) - set(listExcludeY)))

    print(xWhereClick, yWhereClick)
    print("X and Y to click: " + str(xWhereClick) + " " + str(yWhereClick))

    #actions.move_to_element_with_offset(element,xWhereClick,yWhereClick).click().perform()

    return listLatency

def ResetBrush(infoReset,driver):
    
    actions = ActionChains(driver,duration = 10)

    #Dimension of the brushable area
    widthBrush = infoReset[1][0] - infoReset[0][0]
    heightBrush = infoReset[1][1] - infoReset[0][1]

    actions.move_to_element_with_offset(element,widthBrush,heightBrush/2).click_and_hold().move_by_offset(-widthBrush/2,0).perform()

    actions.move_to_element_with_offset(element,widthBrush*2/3,heightBrush/2).click().perform

def EventHandle(eventName,state,driver,pathNumber,pathElement):

    print("----------ANALYZING " + pathElement + "------------")
    print("----------EVENT : " + str(eventName) + "------------")

    latency = None

    if(eventName == "click"):
    
        latency = Click(state["info"],driver)

    #elif(eventName == "dblclick"):
        #latency = doubleClick(state["info"], driver)

    elif(eventName == "change"):

        if(state["info"] == None):

            latency = Click(state["info"],driver)

        else:
                
            latency = Input(state["info"],driver)

    elif(eventName == "contextmenu"):

        latency = ContextClick(state["info"],driver)

    elif(eventName == "mouseover" or eventName == "mouseenter"):

        latency = Mouseover(driver)
    
    elif(eventName == "brush"):

        print("Brush start")

        latency = Brush(state["info"][0],driver)

        #print("STATE: " + xpath + " EVENT: " + "mousedown" + " LATENCY: " + str(latency[1]) + " ms")
        actionSequence.append(["brush mousedown",latency[0]])

        resultLatency = checkLevel("mousedown",latency[0])
        if(resultLatency > 0):
            problemsFound[pathNumber].append(([pathElement,"brush mousedown",state["info"][0],latency[0] , resultLatency]))

        finalSummary[pathNumber].append([pathElement,"brush mousedown",state["info"][0],latency[0] , resultLatency])


        for latencyTime in latency[1:-1]:
            #Convert in milliseconds
            #print("STATE: " + xpath + " EVENT: " + "mousemove" + " LATENCY: " + str(latencyTime) + " ms")
            actionSequence.append(["brush mousemove",latencyTime])

            resultLatency = checkLevel("mousemove",latencyTime)
            if(resultLatency > 0):
                problemsFound[pathNumber].append([pathElement,"brush mousemove",state["info"][0],latencyTime , resultLatency])

            finalSummary[pathNumber].append([pathElement,"brush mousemove",state["info"][0],latencyTime , resultLatency])

        #print("STATE: " + xpath + " EVENT: " + "mouseup" + " LATENCY: " + str(latency[-1]) + " ms")
        actionSequence.append(["brush mouseup",latency[-1]])

        resultLatency = checkLevel("mouseup",latency[-1])
        if(resultLatency > 0):
            problemsFound[pathNumber].append([pathElement,"brush mouseup",state["info"][0],latency[-1] , resultLatency])

        finalSummary[pathNumber].append([pathElement,"brush mouseup",state["info"][0],latency[-1] , resultLatency])

        print("Pan start")

        latency = PanBrush(state["info"][1],driver)
        print(state["info"][1])
        #print("STATE: " + xpath + " EVENT: " + "mousedown" + " LATENCY: " + str(latency[1]) + " ms")
        actionSequence.append(["panbrush mousedown",latency[0]])

        resultLatency = checkLevel("mousedown",latency[0])
        if(resultLatency > 0):
            problemsFound[pathNumber].append(([pathElement,"panbrush mousedown",state["info"][1],latency[0] , resultLatency]))

        finalSummary[pathNumber].append([pathElement,"panbrush mousedown",state["info"][1],latency[0] , resultLatency])


        for latencyTime in latency[1:-1]:
            #Convert in milliseconds
            #print("STATE: " + xpath + " EVENT: " + "mousemove" + " LATENCY: " + str(latencyTime) + " ms")
            actionSequence.append(["panbrush mousemove",latencyTime])

            resultLatency = checkLevel("mousemove",latencyTime)
            if(resultLatency > 0):
                problemsFound[pathNumber].append([pathElement,"panbrush mousemove",state["info"][1],latencyTime , resultLatency])

            finalSummary[pathNumber].append([pathElement,"panbrush mousemove",state["info"][1],latencyTime , resultLatency])

        #print("STATE: " + xpath + " EVENT: " + "mouseup" + " LATENCY: " + str(latency[-1]) + " ms")
        actionSequence.append(["panbrush mouseup",latency[-1]])

        resultLatency = checkLevel("mouseup",latency[-1])
        if(resultLatency > 0):
            problemsFound[pathNumber].append([pathElement,"panbrush mouseup",state["info"][1],latency[-1] , resultLatency])

        finalSummary[pathNumber].append([pathElement,"panbrush mouseup",state["info"][1],latency[-1] , resultLatency])

    elif(eventName == "panzoom"):

        latency = PanZoom(state["info"],driver)

        #print("STATE: " + xpath + " EVENT: " + "mousedown" + " LATENCY: " + str(latency[1]) + " ms")
        actionSequence.append(["panzoom mousedown",latency[0]])

        resultLatency = checkLevel("mousedown",latency[0])
        if(resultLatency > 0):
            problemsFound[pathNumber].append([pathElement,"panzoom mousedown",state["info"][1],latency[0] , resultLatency])

        finalSummary[pathNumber].append([pathElement,"panzoom mousedown",state["info"][1],latency[0] , resultLatency])


        for latencyTime in latency[1:-1]:
            #Convert in milliseconds
            #print("STATE: " + xpath + " EVENT: " + "mousemove" + " LATENCY: " + str(latencyTime) + " ms")
            actionSequence.append(["panzoom mousemove",latencyTime])

            resultLatency = checkLevel("mousemove",latencyTime)
            if(resultLatency > 0):
                problemsFound[pathNumber].append([pathElement,"panzoom mousemove",state["info"][1],latencyTime , resultLatency])

            finalSummary[pathNumber].append([pathElement,"panzoom mousemove",state["info"][1],latencyTime , resultLatency])

        #print("STATE: " + xpath + " EVENT: " + "mouseup" + " LATENCY: " + str(latency[-1]) + " ms")
        actionSequence.append(["panzoom mouseup",latency[-1]])

        resultLatency = checkLevel("mouseup",latency[-1])
        if(resultLatency > 0):
            problemsFound[pathNumber].append([pathElement,"panzoom mouseup",state["info"][1],latency[-1] , resultLatency])

        finalSummary[pathNumber].append([pathElement,"panzoom mouseup",state["info"][1],latency[-1] , resultLatency])

    elif(eventName == "wheel"):

        latency = Zoom(state["info"],driver)

        for latencyTime in latency:
    
            #print("STATE: " + xpath + " EVENT: " + "mousemove" + " LATENCY: " + str(latencyTime) + " ms")
            actionSequence.append([eventName,latencyTime])

            resultLatency = checkLevel(eventName,latencyTime)
            if(resultLatency > 0):
                problemsFound[pathNumber].append([pathElement,eventName,state["info"],latencyTime , resultLatency])

            finalSummary[pathNumber].append([pathElement,eventName,state["info"],latencyTime , resultLatency])

    elif(eventName == "mouseout" or eventName == "mouseleave"):

        latency = Mouseout(driver)

    elif(eventName == "input"):

        latency = Input(state["info"],driver)

        if(type(latency) is list):
    
            #print("STATE: " + xpath + " EVENT: " + "mousedown" + " LATENCY: " + str(latency[1]) + " ms")
            actionSequence.append(["slider mousedown",latency[0]])

            resultLatency = checkLevel("mousedown",latency[0])
            if(resultLatency > 0):
                problemsFound[pathNumber].append([pathElement,"slider mousedown",state["info"],latency[0] , resultLatency])
            finalSummary[pathNumber].append([pathElement,"slider mousedown",state["info"],latency[0] , resultLatency])


            for latencyTime in latency[1:-1]:
                #Convert in milliseconds
                #print("STATE: " + xpath + " EVENT: " + "mousemove" + " LATENCY: " + str(latencyTime) + " ms")
                actionSequence.append(["slider mousemove",latencyTime])

                resultLatency = checkLevel("mousemove",latencyTime)
                if(resultLatency > 0):
                    problemsFound[pathNumber].append([pathElement,"slider mousemove",state["info"],latencyTime , resultLatency])

                finalSummary[pathNumber].append([pathElement,"slider mousemove",state["info"],latencyTime , resultLatency])

            #print("STATE: " + xpath + " EVENT: " + "mouseup" + " LATENCY: " + str(latency[-1]) + " ms")
            actionSequence.append(["slider mouseup",latency[-1]])

            resultLatency = checkLevel("mouseup",latency[-1])
            if(resultLatency > 0):
                problemsFound[pathNumber].append([pathElement,"slider mouseup",state["info"],latency[-1] , resultLatency])

            finalSummary[pathNumber].append([pathElement,"slider mouseup",state["info"],latency[-1] , resultLatency])

    elif(eventName == "mousemove"):

        latency = Mousemove(state["info"],driver)

        for responseTime in latency:
    
            #print("STATE: " + xpath + " EVENT: " + eventName + " LATENCY: " + str(responseTime) + " ms")
            actionSequence.append([eventName,responseTime])

            resultLatency = checkLevel(eventName,responseTime)
            if(resultLatency > 0):
                problemsFound[pathNumber].append([pathElement,eventName,state["info"],responseTime, resultLatency])
            finalSummary[pathNumber].append([pathElement,eventName,state["info"],responseTime, resultLatency])


    elif(eventName == "reset_brush"):
    
        ResetBrush(state["info"],driver)

    if(latency != None):

        if(type(latency) is not list):

            #Convert in milliseconds
            latency = latency * 1000
            
            #print("STATE: " + xpath + " EVENT: " + eventName + " LATENCY: " + str(latency) + " ms")
            actionSequence.append([eventName,latency])

            resultLatency = checkLevel(eventName,latency)
            if(resultLatency > 0):
                problemsFound[pathNumber].append([pathElement,eventName,state["info"],latency, resultLatency])
            finalSummary[pathNumber].append([pathElement,eventName,state["info"],latency, resultLatency])
            
    else:

        #print("STATE: " + xpath + " EVENT: " + eventName + " LATENCY: None")
        actionSequence.append([eventName,latency])


actionSequence = []
finalSummary = {}
exploredNodes = {}
problemsFound =  {}
element = None
pathElement = ""

if __name__ == "__main__":

    startTime = time.asctime()

    configuration = open("conf.json")
    confJSON=json.load(configuration)

    nameVis = confJSON["name"]
    urlVis = confJSON["url"]
    siblingPercentage = confJSON["siblings_percentage"]

    userTrace = confJSON["user"]

    if(userTrace == 0):

        #open the statechart json file
        explorationSequence = open('exploration_falcon_7M_1.json') #change the number of the exploration you would like to test! open('explorations/exploration_' + nameVis +'_1.json')

        #returns the JSON object as a dictionary
        explorationSequence = json.load(explorationSequence)

        #driver = webdriver.Chrome()
        options = webdriver.ChromeOptions()
        options.add_argument('ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        driver = webdriver.Chrome(executable_path='C:\webdrivers\chromedriver.exe')
        driver = webdriver.Chrome(chrome_options=options)

        
        pathNumber = 0
        for path in explorationSequence:
            #print(explorationSequence)
            try:

                driver.get(urlVis)
                driver.maximize_window()

            except:

                print("URL NOT REACHABLE")
                driver.close()
                exit

            else:

                originalWindow = driver.current_window_handle

                print("PATH: " + str(pathNumber))
                
                finalSummary[pathNumber] = []
                problemsFound[pathNumber] = []
                exploredNodes[pathNumber] = []

                if(path == None):
                    print("None found")

                else:

                    time.sleep(2)

                    

                    for transition in path:
                        
                        fake = 0
                        warning = -1
                        #print("Starting from state 0:")
                        #toWrite = "Starting from state 0:"
                        #exploredNodes[pathNumber].append(toWrite)
                        if transition["event"] == "brush":
                            try:
                                print(transition["info"][0][1])
                            except:
                                print("Fake brush, skipping...")
                                fake = 1
                        


                        if transition["css"] == "#departure canvas.marks" and transition["event"] == "brush" and fake != 1:
                            print("mousedown on departure, transition: 0--->6")
                            toWrite = "mousedown on departure, transition: 0--->6"
                            exploredNodes[pathNumber].append(toWrite)
                            print("mousemove on departure, transition: 6--->6")
                            toWrite = "mousemove on departure, transition: 6--->6"
                            exploredNodes[pathNumber].append(toWrite)
                            
                            if transition["startingPath"] == "detected_wheel":
                                print("wheel on departure while brushing, transition: 6--->6")
                                toWrite = "wheel on departure while brushing, transition: 6--->6"
                                exploredNodes[pathNumber].append(toWrite)
                            
                            if transition["startingPath"] == "detected_mouseout":
                                print("mouseout on departure while brushing, transition: 6--->6")
                                toWrite = "mouseout on departure while brushing, transition: 6--->6"
                                exploredNodes[pathNumber].append(toWrite)
                            
                            print("mouseup on departure, transition: 6--->0")
                            toWrite = "mouseup on departure, transition: 6--->0"
                            exploredNodes[pathNumber].append(toWrite)

                        if transition["css"] == "#arrival canvas.marks" and transition["event"] == "brush" and fake != 1:
                            print("mousedown on arrival, transition: 0--->5")
                            toWrite = "mousedown on arrival, transition: 0--->5"
                            exploredNodes[pathNumber].append(toWrite)
                            print("mousemove on arrival, transition: 5--->5")
                            toWrite = "mousemove on arrival, transition: 5--->5"
                            exploredNodes[pathNumber].append(toWrite)
                            
                            if transition["startingPath"] == "detected_wheel":
                                print("wheel on arrival while brushing, transition: 5--->5")
                                toWrite = "wheel on arrival while brushing, transition: 5--->5"
                                exploredNodes[pathNumber].append(toWrite)
                            
                            if transition["startingPath"] == "detected_mouseout":
                                print("mouseout on arrival while brushing, transition: 5--->5")
                                toWrite = "mouseout on arrival while brushing, transition: 5--->5"
                                exploredNodes[pathNumber].append(toWrite)
                            
                            print("mouseup on arrival, transition: 5--->0")
                            toWrite = "mouseup on arrival, transition: 5--->0"
                            exploredNodes[pathNumber].append(toWrite)
                            
                        if transition["css"] == "#airtime canvas.marks" and transition["event"] == "brush" and fake != 1:
                            print("mousedown on airtime, transition: 0--->7")
                            toWrite = "mousedown on airtime, transition: 0--->7"
                            exploredNodes[pathNumber].append(toWrite)
                            print("mousemove on airtime, transition: 7--->7")
                            toWrite = "mousemove on airtime, transition: 7--->7"
                            exploredNodes[pathNumber].append(toWrite)
                            
                            if transition["startingPath"] == "detected_wheel":
                                print("wheel on airtime while brushing, transition: 7--->7")
                                toWrite = "wheel on airtime while brushing, transition: 7--->7"
                                exploredNodes[pathNumber].append(toWrite)
                            
                            if transition["startingPath"] == "detected_mouseout":
                                print("mouseout on airtime while brushing, transition: 7--->7")
                                toWrite = "mouseout on airtime while brushing, transition: 7--->7"
                                exploredNodes[pathNumber].append(toWrite)
                            
                            print("mouseup on airtime, transition: 7--->0")
                            toWrite = "mouseup on airtime, transition: 7--->0"
                            exploredNodes[pathNumber].append(toWrite)
                        
                        if transition["css"] == "#delay canvas.marks" and transition["event"] == "brush" and fake != 1:
                            print("mousedown on delay, transition: 0--->8")
                            toWrite = "mousedown on delay, transition: 0--->8"
                            exploredNodes[pathNumber].append(toWrite)
                            print("mousemove on delay, transition: 8--->8")
                            toWrite = "mousemove on delay, transition: 8--->8"
                            exploredNodes[pathNumber].append(toWrite)
                            
                            if transition["startingPath"] == "detected_wheel":
                                print("wheel on delay while brushing, transition: 8--->8")
                                toWrite = "wheel on delay while brushing, transition: 8--->8"
                                exploredNodes[pathNumber].append(toWrite)
                            
                            if transition["startingPath"] == "detected_mouseout":
                                print("mouseout on delay while brushing, transition: 8--->8")
                                toWrite = "mouseout on delay while brushing, transition: 8--->8"
                                exploredNodes[pathNumber].append(toWrite)
                                
                            print("mouseup on delay, transition: 8--->0")
                            toWrite = "mouseup on delay, transition: 8--->0"
                            exploredNodes[pathNumber].append(toWrite)

                        if transition["css"] == "#distance canvas.marks" and transition["event"] == "brush" and fake != 1:
                            print("mousedown on distance, transition: 0--->4")
                            toWrite = "mousedown on distance, transition: 0--->4"
                            exploredNodes[pathNumber].append(toWrite)
                            print("mousemove on distance, transition: 4--->4")
                            toWrite = "mousemove on distance, transition: 4--->4"
                            exploredNodes[pathNumber].append(toWrite)
                            
                            if transition["startingPath"] == "detected_wheel":
                                print("wheel on distance while brushing, transition: 4--->4")
                                toWrite = "wheel on distance while brushing, transition: 4--->4"
                                exploredNodes[pathNumber].append(toWrite)
                            
                            if transition["startingPath"] == "detected_mouseout":
                                print("mouseout on distance while brushing, transition: 4--->4")
                                toWrite = "mouseout on distance while brushing, transition: 4--->4"
                                exploredNodes[pathNumber].append(toWrite)
                                
                            print("mouseup on distance, transition: 4--->0")
                            toWrite = "mouseup on distance, transition: 4--->0"
                            exploredNodes[pathNumber].append(toWrite)

                        if transition["event"] != "brush":
                            print(transition["event"] + " on " + transition["css"] + " , transition: 0--->0")
                            toWrite = transition["event"] + " on " + transition["css"] + " , transition: 0--->0"
                            exploredNodes[pathNumber].append(toWrite)
                        
                        if transition["css"] == "#count canvas.marks" and transition["event"] == "mousedown":
                            print("mousedown on count, transition: 0--->1")
                            toWrite = "mousedown on count, transition: 0--->1"
                            warning = 1
                         
                        if transition["css"] == "#count canvas.marks" and transition["event"] == "click" and warning == 1:
                            print("click on count, transition: 1--->1")
                            toWrite = "click on count, transition: 1--->1"
                            
                        if transition["css"] == "#count canvas.marks" and transition["event"] == "mousemove" and warning == 1:
                            print("mousemove on count, transition: 1--->1")
                            toWrite = "mousemove on count, transition: 1--->1"
                        
                        if transition["css"] == "#count canvas.marks" and transition["event"] == "mouseout" and warning == 1:
                            print("mouseout on count, transition: 1--->1")
                            toWrite = "mouseout on count, transition: 1--->1"
                            
                        if transition["css"] == "#count canvas.marks" and transition["event"] == "facsimile_back" and warning == 1:
                            print("facsimile_back on count, transition: 1--->0")
                            toWrite = "facsimile_back on count, transition: 1--->0"
                            warning = 0          


                        if(len(driver.window_handles) != 1):
                            driver.switch_to.window(originalWindow)

                        time.sleep(1)

                        mouseOutElement = driver.find_element(By.CSS_SELECTOR,"body")
                        actions = ActionChains(driver,duration = 0)

                        actions.move_to_element(mouseOutElement)
                        
                        start = time.time()
                        actions.perform()
                        end = time.time()

                        timeOut = end-start

                        xpath = transition["xpath"]
                        event = transition["event"]
                        siblings = 0 #change to string if you want to access falcon 7M
                        starting = transition["startingPath"]
                    

                        for i in range(siblings + 1):

                            if(siblings != 0):

                                pathElement = xpath + "[" + str(starting + i) + "]"
                            
                            else:

                                pathElement = xpath

                            try:

                                element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,pathElement)))

                            except Exception as e:

                                    print(e)
                                    print("Element not found: " + pathElement)

                            else:

                                try:

                                    if(element.rect["width"] == 0 and element.rect["height"] == 0):

                                        print("Element not interactable")

                                    else:

                                        visible = driver.execute_script("var rect = arguments[0].getBoundingClientRect(); "+
                                            "return (rect.top >= 0 && rect.left >= 0 && rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && " +
                                            "rect.right <= (window.innerWidth || document.documentElement.clientWidth))",element)

                                        if not visible:
                            
                                            driver.execute_script("arguments[0].scrollIntoView(true);", element)

                                        eventName = event

                                        EventHandle(eventName,transition,driver,pathNumber,pathElement)

                                except Exception as e:
                                    
                                    print("Exception Found: ",end="")
                                    print(e)
                                    
                            print("-------------------------------------------------------")

                pathNumber+=1
            
        driver.close()

        tmp = str(uuid.uuid4())
        with open('count/summary_' + nameVis + '_' + tmp + '.json', 'w') as fp: #saves the exploration that will be used by the times.py script
            json.dump(finalSummary, fp,  indent=4)

        with open('time_and_violations/summary_' + nameVis + '_' + tmp + '.json', 'w') as file: #saves the exploration that will be used by the count.py script
            print(exploredNodes)
            json.dump(exploredNodes, file,  indent=4)
        
        #print(actionSequence)
        print("Problems found :",end="")
        print(problemsFound)

        with open('time_and_violations/summaryProblems_' + nameVis + '_' + tmp + '.json', 'w') as fp: #saves an additional output file, containing the violations in latency thresholds. The violations are already computed by the times.py script.
            json.dump(problemsFound, fp,  indent=4)


    else:

        pathNumber = 0

        finalSummary[pathNumber] = []
        problemsFound[pathNumber] = []

        #open the statechart json file
        explorationSequence = open('user_trace.json')

        #returns the JSON object as a dictionary
        explorationSequence = json.load(explorationSequence)

        driver = webdriver.Chrome()

        try:

            driver.get(urlVis)
            driver.maximize_window()

        except:

            print("URL NOT REACHABLE")
            driver.close()
            exit

        else:

            originalWindow = driver.current_window_handle

            for transition in explorationSequence:

                if(len(driver.window_handles) != 1):
                    driver.switch_to.window(originalWindow)

                time.sleep(0.5)

                mouseOutElement = driver.find_element(By.CSS_SELECTOR,"body")
                actions = ActionChains(driver,duration = 0)

                actions.move_to_element(mouseOutElement)
                
                start = time.time()
                actions.perform()
                end = time.time()

                timeOut = end-start


                xpath = transition["xpath"]
                event = transition["event"]

                pathElement = xpath

                try:

                    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,pathElement)))

                except Exception as e:

                        print(e)
                        print("Element not found: " + pathElement)

                else:

                    #try:

                    if(element.rect["width"] == 0 and element.rect["height"] == 0):

                        print("Element not interactable")

                    else:

                        visible = driver.execute_script("var rect = arguments[0].getBoundingClientRect(); "+
                            "return (rect.top >= 0 && rect.left >= 0 && rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && " +
                            "rect.right <= (window.innerWidth || document.documentElement.clientWidth))",element)

                        if not visible:
            
                            driver.execute_script("arguments[0].scrollIntoView(true);", element)

                        eventName = event

                        EventHandle(eventName,transition,driver,pathNumber,pathElement)

                    #except Exception as e:
                        
                    #    print("Exception Found: ",end="")
                    #    print(e)
                        
                print("-------------------------------------------------------")


            driver.close()

            with open('userTraceSummary_' + nameVis + '.json', 'w') as fp:
                json.dump(finalSummary, fp,  indent=4)
            
            #print(actionSequence)
            print("Problems found :",end="")
            print(problemsFound)

            with open('userTraceSummaryProblems_' + nameVis + '.json', 'w') as fp:
                json.dump(problemsFound, fp,  indent=4)


    endTime = time.asctime()

    print("Execution start " + str(startTime) + " and end in " + str(endTime))

    driver.quit()
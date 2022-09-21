# import libraries
import numpy as np
import cv2

import matplotlib.pyplot as plt

# ----------------
##  Part (a)
# ----------------
# Load in the image and convert to grayscale 
hand = cv2.imread('hand0.png').astype(np.float32)
us   = cv2.imread('US.png').astype(np.float32)

hand_gray = ((hand[:,:,2] + hand[:,:,1] + hand[:,:,0]) / 3)
us_gray   = ((us[:,:,2] + us[:,:,1] + us[:,:,0]) / 3)

#print("Hand shape: ", np.shape(hand_gray))
#print("US shape: ", np.shape(us_gray))

# ----------------
##  Part (b)
# ----------------
# Convert to a binary image using Otsu's thresholding method
# The hand and continental US should be foreground (white)
retval_hand, handBin = cv2.threshold(hand_gray, thresh=127, maxval=255, type=cv2.THRESH_BINARY_INV)
retval_us, usBin = cv2.threshold(us_gray, thresh=170, maxval=255, type=cv2.THRESH_BINARY_INV)

# ----------------
##  Part (c)
# ----------------
# Fill in the first and last rows & columns of the binary image with black
handBin[:,0] = 0
handBin[:, np.shape(handBin)[1]-1] = 0
handBin[0,:] = 0
handBin[np.shape(handBin)[0]-1, :] = 0

usBin[:,0] = 0
usBin[:, np.shape(usBin)[1]-1] = 0
usBin[0,:] = 0
usBin[np.shape(usBin)[0]-1, :] = 0

# ----------------
##  Part (d)
# ----------------
# Write out the binarized image to a file
cv2.imwrite('hand_binary.png', handBin)
cv2.imwrite('US_binary.png', usBin)

# ----------------
##  Part (e)
# ----------------
# Find a point on the edge of the object
# Assume that the edge is the first white pixel on the line halfway down the image
handRows = np.shape(handBin)[0]
handCols = np.shape(handBin)[1]

usRows = np.shape(usBin)[0]
usCols = np.shape(usBin)[1]

hand_midway_pt = int(np.round(handRows / 2))
us_midway_pt = int(np.round(usRows / 2))

def calcStartingPt(midPt, binImg):
    stillBlack = True
    col = 0
    while stillBlack:
        if binImg[midPt][col] == 255:
            pixelRow, pixelCol = [midPt, col]
            stillBlack = False
        col = col + 1
    return pixelRow, pixelCol

handRow, handCol = calcStartingPt(hand_midway_pt, handBin)
usRow, usCol = calcStartingPt(us_midway_pt, usBin)
print('Hand starting points: ', handRow, handCol)
print('US starting points: ', usRow, usCol)

# ----------------
##  Part (f)
# ----------------
# Call your own Pavlidis function to extract the contour of the object
def pavlidis(binRow, binCol, binImg):
    stillIterating = True
    arrowDir = 'up'

    origPointRow = binRow
    origPointCol = binCol
    rowLocations = []
    colLocations = []
    while stillIterating:
        # if the arrow direction is up, check the top left, middle, and top right pixels
        if arrowDir == 'up':
            # check front-left
            if binImg[binRow-1][binCol-1] == 255:
                rowLocations.append(binRow-1)
                colLocations.append(binCol-1)

                # set the new starting position to that location
                binRow = binRow-1
                binCol = binCol-1

                # change the arrow position to point to the left
                arrowDir = 'left'
            
            # check front
            elif binImg[binRow-1][binCol] == 255:
                rowLocations.append(binRow-1)
                colLocations.append(binCol)

                # set the new starting position to that location
                binRow = binRow-1
                binCol = binCol

                # change the arrow position to point to the left
                arrowDir = 'up'

            # check front-right
            elif binImg[binRow-1][binCol+1] == 255:
                rowLocations.append(binRow-1)
                colLocations.append(binCol+1)

                # set the new starting position to that location
                binRow = binRow-1
                binCol = binCol+1

                # change the arrow position to point to the left
                arrowDir = 'up'
            
            # if none are an edge pixel
            else:
                arrowDir = 'right'

        # if the arrow direction is right
        if arrowDir == 'right':
            # check front-left
            if binImg[binRow-1][binCol+1] == 255:
                rowLocations.append(binRow-1)
                colLocations.append(binCol+1)

                # set the new starting position to that location
                binRow = binRow-1
                binCol = binCol+1

                # change the arrow position to point to the left
                arrowDir = 'up'
            
            # check front
            elif binImg[binRow][binCol+1] == 255:
                rowLocations.append(binRow)
                colLocations.append(binCol+1)

                # set the new starting position to that location
                binRow = binRow
                binCol = binCol+1

                # change the arrow position to point to the left
                arrowDir = 'right'

            # check front-right
            elif binImg[binRow+1][binCol+1] == 255:
                rowLocations.append(binRow+1)
                colLocations.append(binCol+1)

                # set the new starting position to that location
                binRow = binRow+1
                binCol = binCol+1

                # change the arrow position to point to the left
                arrowDir = 'right'
            
            # if none are an edge pixel
            else:
                arrowDir = 'down'

        # if the arrow direction is down
        if arrowDir == 'down':
            # check front-left
            if binImg[binRow+1][binCol+1] == 255:
                rowLocations.append(binRow+1)
                colLocations.append(binCol+1)

                # set the new starting position to that location
                binRow = binRow+1
                binCol = binCol+1

                # change the arrow position to point to the left
                arrowDir = 'right'
            
            # check front
            elif binImg[binRow+1][binCol] == 255:
                rowLocations.append(binRow+1)
                colLocations.append(binCol)

                # set the new starting position to that location
                binRow = binRow+1
                binCol = binCol

                # change the arrow position to point to the left
                arrowDir = 'down'

            # check front-right
            elif binImg[binRow+1][binCol-1] == 255:
                rowLocations.append(binRow+1)
                colLocations.append(binCol-1)

                # set the new starting position to that location
                binRow = binRow+1
                binCol = binCol-1

                # change the arrow position to point to the left
                arrowDir = 'down'
            
            # if none are an edge pixel
            else:
                arrowDir = 'left'

        # if the arrow direction is left
        if arrowDir == 'left':
            # check front-left
            if binImg[binRow+1][binCol-1] == 255:
                rowLocations.append(binRow+1)
                colLocations.append(binCol-1)

                # set the new starting position to that location
                binRow = binRow+1
                binCol = binCol-1

                # change the arrow position to point to the left
                arrowDir = 'down'
            
            # check front
            elif binImg[binRow][binCol-1] == 255:
                rowLocations.append(binRow)
                colLocations.append(binCol-1)

                # set the new starting position to that location
                binRow = binRow
                binCol = binCol-1

                # change the arrow position to point to the left
                arrowDir = 'left'

            # check front-right
            elif binImg[binRow-1][binCol-1] == 255:
                rowLocations.append(binRow-1)
                colLocations.append(binCol-1)

                # set the new starting position to that location
                binRow = binRow-1
                binCol = binCol-1

                # change the arrow position to point to the left
                arrowDir = 'left'
            
            # if none are an edge pixel
            else:
                arrowDir = 'up'

        # check if made it back to starting pixel
        # if yes, then exit out of the while loop
        if (binRow == origPointRow) & (binCol == origPointCol):
            stillIterating = False

    return np.array([rowLocations, colLocations])

#handRowLoc, handColLoc = pavlidis(handRow, handCol, handBin)
#usRowLoc, usColLoc = pavlidis(usRow, usCol, usBin)

#handContourValues = np.array([handRowLoc, handColLoc])
#usContourValues = np.array([usRowLoc, usColLoc])

handContourValues = pavlidis(handRow, handCol, handBin)
usContourValues = pavlidis(usRow, usCol, usBin)

# create an empty matrix of all black pixels
# draw the contour
handContour = np.zeros(np.shape(handBin))
for val in range(np.shape(handContourValues)[1]):
    i = handContourValues[0][val]
    j = handContourValues[1][val]
    handContour[i][j] = 255

usContour = np.zeros(np.shape(usBin))
for val in range(np.shape(usContourValues)[1]):
    i = usContourValues[0][val]
    j = usContourValues[1][val]
    usContour[i][j] = 255

# save the contour
cv2.imwrite('hand_contour.png', handContour)
cv2.imwrite('us_contour.png', usContour)

# ----------------
##  Part (g)
# ----------------
# Call the function supplied to calculate the area of the object from the image

# this little function calculates the area of an object from its contour 
# using simple pixel counting 
# holes in the object are not considered (they count as if they are filled in) 
# it's really klugey - not great code 
def fillArea(ctr): 
    maxx = np.max(ctr[:, 0]) + 1 
    maxy = np.max(ctr[:, 1]) + 1 
    contourImage = np.zeros( (maxy, maxx) ) 
    length = ctr.shape[0] 
    for count in range(length): 
        contourImage[ctr[count, 1], ctr[count, 0]] = 255 
        cv2.line(contourImage, (ctr[count, 0], ctr[count, 1]), \
                 (ctr[(count + 1) % length, 0], ctr[(count + 1) % length, 1]), \
       (255, 0, 255), 1) 
    fillMask = cv2.copyMakeBorder(contourImage, 1, 1, 1, 1,\
   cv2.BORDER_CONSTANT, 0).astype(np.uint8) 
    areaImage = np.zeros((maxy, maxx), np.uint8) 
    startPoint = (int(maxy/2), int(maxx/2)) 
    cv2.floodFill(areaImage, fillMask, startPoint, 128) 
    area = np.sum(areaImage)/128 
    return area 

handArea = fillArea(handContourValues.transpose())
#print("Hand area from function provided: ", handArea)
usArea = fillArea(usContourValues.transpose())
#print("US area from function provided: ", usArea)

# ----------------
##  Part (h)
# ----------------
# Create a gaussian area estimation function
# Compute the estimated area from the contour points
def gausArea(ctr):
    area = 0
    rows = ctr[0,:] # y
    cols = ctr[1,:] # x
    for i in range(np.shape(ctr)[1]):
        try:
            det = cols[i] * rows[i+1] - cols[i+1] * rows[i]
        except:
            print('done')
            
        area = area + det

    return (area / 2)


gaussAreaHand = gausArea(handContourValues)
#print('Hand area from gaussian function: ', gaussAreaHand)
gaussAreaUS = gausArea(usContourValues)
#print('US area from gaussian function: ', gaussAreaUS)

# ----------------
##  Part (i)
# ----------------
# Print the filename, the number of points in the contour,
# the actual area, and the Gauss' estimate of the area
print('hand_contour.png')
print('Number of points in the contour: ', np.shape(handContourValues)[1])
print('Actual area: ', handArea)
print('Gauss area estimate: ', gaussAreaHand)

print('US_contour.png')
print('Number of points in the contour: ', np.shape(usContourValues)[1])
print('Actual area: ', usArea)
print('Gauss area estimate: ', gaussAreaUS)

# ----------------
##  Part (j)
# ----------------
# implement one pass of the Discrete Curve Evolution algorithm
def DCE(ctr):
    rows = ctr[0,:] # y
    cols = ctr[1,:] # x

    thetaVals = []
    lengthVals = []
    for i in range(np.shape(ctr)[1]):
        try:
            theta = np.arctan((rows[i] - rows[i-1]) / (cols[i] - cols[i-1])) - np.arctan((rows[i+1] - rows[i]) / (cols[i+1] - cols[i]))
            thetaVals.append(theta)
        except:
            pass
            

    for i in range(np.shape(ctr)[1]):
        try:
            length = np.sqrt((rows[i] - rows[i-1])**2 + (cols[i] - cols[i-1])**2)
            lengthVals.append(length)
        except:
            pass
    

    thetaVals = np.array(thetaVals)
    lengthVals = np.array(lengthVals)

    # calculate the relevance measure
    K = []
    for i in range(len(thetaVals)):
        try:
            ktemp = (np.abs(thetaVals[i]) * lengthVals[i] * lengthVals[i+1]) / (lengthVals[i] + lengthVals[i+1])
            K.append(ktemp)
        except:
            pass

    K = np.array(K)
    K_minLocations = np.argwhere(K == np.min(K))

    rows = np.delete(rows, K_minLocations[0])
    cols = np.delete(cols, K_minLocations[0])
    
    return rows, cols

# -----------------------------------------------------------------

# hand DCE calculation
handContourValues_DCE = handContourValues
for n in range(8):
    for m in range(int(np.round(np.shape(handContourValues_DCE)[1])/2)):
        handRows_DCE, handCols_DCE = DCE(handContourValues_DCE)
        handContourValues_DCE = np.array([handRows_DCE, handCols_DCE])

    # HAND CONTOUR parts (ii) and (iii)
    # create an image consisting of the remaining contour points, connected by lines
    # save this image to a file
    handContour_DCE = np.zeros(np.shape(handBin))
    for val in range(len(handRows_DCE)):
        i = handRows_DCE[val]
        j = handCols_DCE[val]
        handContour_DCE[i][j] = 255

    color = (255, 255, 255)
    for val in range(len(handRows_DCE)-1):
        cv2.line(handContour_DCE, (handCols_DCE[val],handRows_DCE[val]), (handCols_DCE[val+1], handRows_DCE[val+1]), color, 1)

    cv2.line(handContour_DCE, (handCols_DCE[-1], handRows_DCE[-1]), (handCols_DCE[0], handRows_DCE[0]), color, 1)
    filename = 'hand_contour_DCE_' + str(n) + '.png'
    cv2.imwrite(filename, handContour_DCE)

    # part (iv) 
    # call the gauss area estimation function to compute
    # the estimated area from the current contour points
    handGaussArea2 = gausArea(handContourValues_DCE)

    # print the filename, number of points in the current contour,
    # and the gauss estimate of the area
    print('Filename: hand_contour_DCE_',n,'.png')
    print('Number of contour points: ', np.shape(handContourValues_DCE)[1])
    print('Gauss area estimation: ', handGaussArea2)

print(np.shape(handContourValues_DCE))

# US DCE calculation
usContourValues_DCE = usContourValues
for n in range(8):
    for m in range(int(np.round(np.shape(usContourValues_DCE)[1])/2)):
        usRows_DCE, usCols_DCE = DCE(usContourValues_DCE)
        usContourValues_DCE = np.array([usRows_DCE, usCols_DCE])

    # US CONTOUR parts (ii) and (iii)
    # create an image consisting of the remaining contour points, connected by lines
    # save this image to a file
    usContour_DCE = np.zeros(np.shape(usBin))
    for val in range(len(handRows_DCE)):
        i = usRows_DCE[val]
        j = usCols_DCE[val]
        usContour_DCE[i][j] = 255

    color = (255, 255, 255)
    for val in range(len(usRows_DCE)-1):
        cv2.line(usContour_DCE, (usCols_DCE[val],usRows_DCE[val]), (usCols_DCE[val+1], usRows_DCE[val+1]), color, 1)

    cv2.line(usContour_DCE, (usCols_DCE[-1], usRows_DCE[-1]), (usCols_DCE[0], usRows_DCE[0]), color, 1)
    filename='us_contour_DCE_' + str(n) + '.png'
    cv2.imwrite(filename, usContour_DCE)

    # part (iv) 
    # call the gauss area estimation function to compute
    # the estimated area from the current contour points
    usGaussArea2 = gausArea(usContourValues_DCE)

    # print the filename, number of points in the current contour,
    # and the gauss estimate of the area
    print('Filename: US_contour_DCE_',n,'.png')
    print('Number of contour points: ', np.shape(usContourValues_DCE)[1])
    print('Gauss area estimation: ', usGaussArea2)
        
print(np.shape(usContourValues_DCE))
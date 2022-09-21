# HW2 - Virginia Tech - ECE5554 | Rebecca DeSipio | Due Date: July 20th, 2022

# import libraries
import numpy as np
import cv2

import matplotlib.pyplot as plt

## ----------------------------------------------------------------------------------
##                                  QUESTION 1
## Create a template for use in template matching.
## This should be an 8-bit grayscale image of just the marker (128x128 in size)
## ----------------------------------------------------------------------------------
# Draw template using "overlaid" rectangles
T = np.ones((128,128), np.float32) * 255 # start with baseline image set to desired template size
white = (255, 255, 255) 
black = (0,0,0)
start = int(128/9) # starting point white inner rectangle

cv2.rectangle(T, (start, start), (128-start, 128-start), black, -1) # -1 fills in the rectangle with the set color
cv2.rectangle(T, (start*2, start*2), (int(128 - start*2),int(128 - start*2)),white, -1)
cv2.rectangle(T, (start*3, start*3), (int(128 - start*3),int(128 - start*3)),black, -1)

## Uncomment to display the template
# cv2.imshow("Template", T)
# cv2.waitKey()
plt.figure()
plt.matshow(T.astype(np.uint8), cmap='gray')

## ----------------------------------------------------------------------------------
##                                  QUESTION 2 (a-d)
## Define a function to perform template matching
## Draw the markers around the identified matches
## ----------------------------------------------------------------------------------
# compute template matching - https://www.geeksforgeeks.org/template-matching-using-opencv-in-python/
# define a function for perform the process
def computeTemplateMatching(img):
    # start by importing QR_A image and get this baseline working
    filename = img
    qrImg = cv2.imread(filename).astype(np.float32)
    qrImg_gray = ((qrImg[:,:,2] + qrImg[:,:,1] + qrImg[:,:,0]) / 3).astype(np.float32)

    # Perform template matching
    tempMatch = cv2.matchTemplate(qrImg_gray, T, cv2.TM_CCOEFF)
    
    # store the original shape of the resulting template matching
    tempShape = np.shape(tempMatch)

    # convert to 0-255 range
    min = np.min(tempMatch)
    tempMatch = np.abs(min) + tempMatch
    max = np.max(tempMatch)
    tempMatch = ((tempMatch / max) * 255).astype(np.uint8)
    saveResult = tempMatch.copy() # save the result displaying the template match result

    # do some post processing to better highlight points of greater certainty as a match
    for i in range(tempShape[0]):
        for j in range(tempShape[1]):
            if tempMatch[i,j] < (255/2):
                tempMatch[i,j] = 0
            if tempMatch[i,j] > (210):
                tempMatch[i,j] = 255

    print("Filename: ", filename)

    # need to find the LOCAL maxima
    maxLoc = np.where(tempMatch == 255)
    maxY = np.unique(maxLoc[0]); maxX = np.unique(maxLoc[1])
    
    consecutiveY = True; consecutiveX = True
    localMaxY = []; localMaxX = []
    counter = 0
    tempY = 0; tempX = 0
    totalCount = 0

    while consecutiveY:
        try:
            if maxY[counter] == maxY[counter+1]-1: # if they match continue counting
                # store the locations in a variable to get the "center location"
                tempY = tempY + maxY[counter]
                totalCount = totalCount + 1; counter = counter + 1
            else: # if no longer consecutive
                # obtain the "center" value and reset the temp variables
                if totalCount != 0:
                    localMaxY.append(tempY / totalCount)

                tempY = 0; totalCount = 0
                counter = counter + 1
        except: # should enter on out of bounds error
            localMaxY.append(tempY / totalCount)
            consecutiveY=False 
            counter = 0; tempY = 0; tempX = 0; totalCount = 0

    while consecutiveX:
        try:
            if maxX[counter] == maxX[counter+1]-1: # if they match continue counting
                # store the locations in a variable to get the "center location"
                tempX = tempX + maxX[counter]
                totalCount = totalCount + 1; counter = counter + 1
            else: # if no longer consecutive
                # obtain the "center" value and reset the temp variables
                if totalCount != 0:
                    localMaxX.append(tempX / totalCount)

                tempX = 0; totalCount = 0
                counter = counter + 1
        except: # should enter on out of bounds error
            localMaxX.append(tempX / totalCount)
            consecutiveX=False 
            counter = 0; tempY = 0; tempX = 0; totalCount = 0

    # locate the points of the three markers
    finalX = []; finalY = []

    finalX.append(int(np.round(localMaxX[0]))); finalX.append(int(np.round(localMaxX[-1])))
    finalY.append(int(np.round(localMaxY[0]))); finalY.append(int(np.round(localMaxY[-1])))

    markerLocations = np.array([(int(finalX[0]), int(finalY[0])), (int(finalX[0]), int(finalY[1])), (int(finalX[1]), int(finalY[0]))])

    # draw the markers on the image
    color = (0,0,255)
    cv2.rectangle(qrImg, (int(finalX[0]), int(finalY[0])), (int(finalX[0]+128), int(finalY[0])+128), color, 5)
    cv2.rectangle(qrImg, (int(finalX[0]), int(finalY[1])), (int(finalX[0]+128), int(finalY[1])+128), color, 5)
    cv2.rectangle(qrImg, (int(finalX[1]), int(finalY[0])), (int(finalX[1]+128), int(finalY[0])+128), color, 5)

    # print out the coordinates to the console
    print("Marker location coordinates (top left points):")
    print(markerLocations.tolist(), " \n")

    return saveResult, qrImg, markerLocations

# PERFORM TEMPLATE MATCHING ON EACH OF THE IMAGES
qrA_res, qrA_img, qrA_markerLocations = computeTemplateMatching('QR_A.png')
qrB_res, qrB_img, qrB_markerLocations = computeTemplateMatching('QR_B.png')
qrC_res, qrC_img, qrC_markerLocations = computeTemplateMatching('QR_C.png')
qrD_res, qrD_img, qrD_markerLocations = computeTemplateMatching('QR_D.png')
qrE_res, qrE_img, qrE_markerLocations = computeTemplateMatching('QR_E.png')

## ----------------------------------------------------------------------------------
##                                  QUESTION 2 (e-f)
## Define a function to perform affine transformations
## ----------------------------------------------------------------------------------
# Define affine transforms to map the three marker locations in the image to points (50,50), (250,50), (50,250)
def performAffineTransforms(img, qr_markerLocations):
    filename = img
    qrImg = cv2.imread(filename).astype(np.float32)
    mapToLocations = np.array([(50,50), (50, 250), (250,50)])

    qr_markerLocations[1][1] = qr_markerLocations[1][1] + 128 # need to use the bottom left corner
    qr_markerLocations[2][0] = qr_markerLocations[2][0] + 128 # need to use the outer right corner

    qr_affineTransform = cv2.getAffineTransform(qr_markerLocations.astype(np.float32), mapToLocations.astype(np.float32))
    qr_warped = cv2.warpAffine(qrImg, qr_affineTransform, (300, 300))
    
    return qr_warped

# OBTAIN AFFINE TRANSFORMED WARPED IMAGES
qrA_warped = performAffineTransforms('QR_A.png', qrA_markerLocations)
qrB_warped = performAffineTransforms('QR_B.png', qrB_markerLocations)
qrC_warped = performAffineTransforms('QR_C.png', qrC_markerLocations)
qrD_warped = performAffineTransforms('QR_D.png', qrD_markerLocations)
qrE_warped = performAffineTransforms('QR_E.png', qrE_markerLocations)


## ----------------------------------------------------------------------------------
##                                  FINAL RESULTS
## SAVE OFF ALL RESULTS
## To instead just view them, replace imwrite with imshow and add cv2.waitKey() 
## ----------------------------------------------------------------------------------
# save results from match template
cv2.imwrite('qrA_MT.png', qrA_res)
cv2.imwrite('qrB_MT.png', qrB_res)
cv2.imwrite('qrC_MT.png', qrC_res)
cv2.imwrite('qrD_MT.png', qrD_res)
cv2.imwrite('qrE_MT.png', qrE_res)

# save results with found marker locations
cv2.imwrite('qrA_result.png', qrA_img)
cv2.imwrite('qrB_result.png', qrB_img)
cv2.imwrite('qrC_result.png', qrC_img)
cv2.imwrite('qrD_result.png', qrD_img)
cv2.imwrite('qrE_result.png', qrE_img)

# save warped images
cv2.imwrite('qrA_warped.png', qrA_warped)
cv2.imwrite('qrB_warped.png', qrB_warped)
cv2.imwrite('qrC_warped.png', qrC_warped)
cv2.imwrite('qrD_warped.png', qrD_warped)
cv2.imwrite('qrE_warped.png', qrE_warped)
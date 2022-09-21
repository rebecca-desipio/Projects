# import libraries
import numpy as np
import cv2

import matplotlib.pyplot as plt

## ----------------------------------------------------------------------------------
##                                  Part (a)
## Load the images and make a copy of the color version
## ----------------------------------------------------------------------------------
elvis        = cv2.imread('Elvis1956.png').astype(np.float32)
chartres     = cv2.imread('Chartres.png').astype(np.float32)
calvinHobbes = cv2.imread('CalvinAndHobbes.png').astype(np.float32)
allmanBros   = cv2.imread('AllmanBrothers.png').astype(np.float32)

# make copies of the original images
elvis_copy         = elvis.copy()
elvis_copy2        = elvis.copy()
chartres_copy      = chartres.copy()
chartres_copy2     = chartres.copy()
calvinHobbes_copy  = calvinHobbes.copy()
calvinHobbes_copy2 = calvinHobbes.copy()
allmanBros_copy    = allmanBros.copy()
allmanBros_copy2    = allmanBros.copy()

print("Shapes of images: ")
print('Elvis: ', np.shape(elvis), ' | Chartres: ', np.shape(chartres), ' | Calvin and Hobbes: ', np.shape(calvinHobbes), ' | Allman Brothers: ', np.shape(allmanBros))

## ----------------------------------------------------------------------------------
##                                  Part (b)
## Covert the original images to grayscale
## ----------------------------------------------------------------------------------
elvis_gray        = ((elvis[:,:,2] + elvis[:,:,1] + elvis[:,:,0]) / 3)
chartres_gray     = ((chartres[:,:,2] + chartres[:,:,1] + chartres[:,:,0]) / 3)
calvinHobbes_gray = ((calvinHobbes[:,:,2] + calvinHobbes[:,:,1] + calvinHobbes[:,:,0]) / 3)
allmanBros_gray   = ((allmanBros[:,:,2] + allmanBros[:,:,1] + allmanBros[:,:,0]) / 3)

print("Shape of grayscale images: ")
print('Elvis: ', np.shape(elvis_gray), ' | Chartres: ', np.shape(chartres_gray), ' | Calvin and Hobbes: ', np.shape(calvinHobbes_gray), ' | Allman Brothers: ', np.shape(allmanBros_gray))

## ----------------------------------------------------------------------------------
##                                  Part (c)
## Find the top 100 keypoints using the goodFeaturesToTrack function
## ----------------------------------------------------------------------------------
elvis_corners        = cv2.goodFeaturesToTrack(elvis_gray, 100, 0.01, 10)
chartres_corners     = cv2.goodFeaturesToTrack(chartres_gray, 100, 0.01, 10)
calvinHobbes_corners = cv2.goodFeaturesToTrack(calvinHobbes_gray, 100, 0.01, 10)
allmanBros_corners   = cv2.goodFeaturesToTrack(allmanBros_gray, 100, 0.01, 10)

## ----------------------------------------------------------------------------------
##                                  Part (d)
## Print the filename and the [X,Y] coordinates of the top 3 corner points
## ----------------------------------------------------------------------------------
print('Top 3 corner points for each image: ')
print('Elvis: ', elvis_corners[0:3].tolist())
print('Chartres: ', chartres_corners[0:3].tolist())
print('Calvin & Hobbes: ', calvinHobbes_corners[0:3].tolist())
print('Allman Brothers: ', allmanBros_corners[0:3].tolist())

## ----------------------------------------------------------------------------------
##                                  Part (e)
## In the copied images, draw small green circles at each of the 100 keypoints
## ----------------------------------------------------------------------------------
# first place the green circles on the rgb copied images
color = (0,255,0)
for e in elvis_corners:
    X, Y = e.flatten()
    cv2.circle(elvis_copy, (int(X),int(Y)), 6, color, 1)

for c in chartres_corners:
    X, Y = c.flatten()
    cv2.circle(chartres_copy, (int(X),int(Y)), 4, color, 1)

for h in calvinHobbes_corners:
    X, Y = h.flatten()
    cv2.circle(calvinHobbes_copy, (int(X),int(Y)), 4, color, 1)

for a in allmanBros_corners:
    X, Y = a.flatten()
    cv2.circle(allmanBros_copy, (int(X),int(Y)), 4, color, 1)

# display images
# cv2.imshow('Elvis', elvis_copy.astype(np.uint8))
# cv2.waitKey()
# cv2.imshow('Chartres', chartres_copy.astype(np.uint8))
# cv2.waitKey()
# cv2.imshow('Calvin & Hobbes', calvinHobbes_copy.astype(np.uint8))
# cv2.waitKey()
# cv2.imshow('Allman Brothers', allmanBros_copy.astype(np.uint8))
# cv2.waitKey()

## ----------------------------------------------------------------------------------
##                                  Part (f-h)
## Call own implementation of Harris corner detector
## ----------------------------------------------------------------------------------
def harrisImplementation(inputImg, minDistance):
    # Step 1: 
    img = inputImg
    Ix = cv2.Sobel(img, cv2.CV_32F, 1, 0, 3)
    Iy = cv2.Sobel(img, cv2.CV_32F, 0, 1, 3)

    # Step 2:
    Ixx = np.multiply(Ix, Ix)
    Ixy = np.multiply(Ix, Iy)
    Iyy = np.multiply(Iy, Iy)

    # Step 3:
    smoothIxx =cv2.GaussianBlur(src=Ixx, ksize=(3,3), sigmaX=.5, sigmaY=1)
    smoothIxy =cv2.GaussianBlur(src=Ixy, ksize=(3,3), sigmaX=.5, sigmaY=1)
    smoothIyy =cv2.GaussianBlur(src=Iyy, ksize=(3,3), sigmaX=.5, sigmaY=1)

    # Step 4:
    det = np.multiply(smoothIxx ,smoothIyy) - np.multiply(smoothIxy, smoothIxy)
    trace = smoothIxx + smoothIyy
    alpha = 0.05
    Q = det - alpha * (trace**2)

    Qflat = Q.flatten()
    Qsorted = np.sort(Qflat)[::-1]

    nPoints=100
    notYet100 = True
    j = 0
    xCoords = []; yCoords = []
    while notYet100:
        x, y = np.where(Q == Qsorted[j])
        for i in range(1):
            if minDistance == 1:
                anyXL = np.array([x[i] in xCoords, x[i]-1 in xCoords])
                anyXR = np.array([x[i] in xCoords, x[i]+1 in xCoords])
                anyYL = np.array([y[i] in yCoords, y[i]-1 in yCoords])
                anyYR = np.array([y[i] in yCoords, y[i]+1 in yCoords])
            elif minDistance == 2:
                anyXL = np.array([x[i] in xCoords, x[i]-1 in xCoords, x[i]-2 in xCoords])
                anyXR = np.array([x[i] in xCoords, x[i]+1 in xCoords, x[i]+2 in xCoords])
                anyYL = np.array([y[i] in yCoords, y[i]-1 in yCoords, y[i]-2 in yCoords])
                anyYR = np.array([y[i] in yCoords, y[i]+1 in yCoords, y[i]+2 in yCoords])
            else:
                anyXL = np.array([x[i] in xCoords, x[i]-1 in xCoords, x[i]-2 in xCoords, x[i]-3 in xCoords, x[i]-4 in xCoords]) #, x[i]-5 in xCoords])
                anyXR = np.array([x[i] in xCoords, x[i]+1 in xCoords, x[i]+2 in xCoords, x[i]+3 in xCoords, x[i]+4 in xCoords]) #, x[i]+5 in xCoords])
                anyYL = np.array([y[i] in yCoords, y[i]-1 in yCoords, y[i]-2 in yCoords, y[i]-3 in yCoords, y[i]-4 in yCoords]) #, y[i]-5 in yCoords])
                anyYR = np.array([y[i] in yCoords, y[i]+1 in yCoords, y[i]+2 in yCoords, y[i]+3 in yCoords, y[i]+4 in yCoords]) #, y[i]+5 in yCoords])


            if (anyXL.any() | anyXR.any()) & (anyYL.any() | anyYR.any()):
                j = j+1
                continue
            else:
                xCoords.append(int(x[i]))
                yCoords.append(int(y[i]))
                if i == len(x):
                    j=j+1
    
        if len(xCoords) == nPoints:
            notYet100 = False

    return xCoords, yCoords

# Elvis
color = (0,0,255)
elvisX, elvisY = harrisImplementation(elvis_gray, 3)
print('Top 3 corners: Elvis')
print('X coordinates: ', elvisX[0:3])
print('Y coordinates: ', elvisY[0:3])
for i in range(100):
    cv2.circle(elvis_copy2, (int(elvisY[i]),int(elvisX[i])), 6, color, 1)


# Chartres
color = (0,0,255)
chartresX, chartresY = harrisImplementation(chartres_gray, 3)
print('Top 3 corners: Chartres')
print('X coordinates: ', chartresX[0:3])
print('Y coordinates: ', chartresY[0:3])
for i in range(100):
    cv2.circle(chartres_copy2, (int(chartresY[i]),int(chartresX[i])), 4, color, 1)

# Calvin and Hobbes
color = (0,0,255)
calvinHobbesX, calvinHobbesY = harrisImplementation(calvinHobbes_gray, 3)
print('Top 3 corners: Calvin and Hobbes')
print('X coordinates: ', calvinHobbesX[0:3])
print('Y coordinates: ', calvinHobbesY[0:3])
for i in range(100):
    cv2.circle(calvinHobbes_copy2, (int(calvinHobbesY[i]),int(calvinHobbesX[i])), 4, color, 1)

# Allman Brothers
color = (0,0,255)
allmanBrosX, allmanBrosY = harrisImplementation(allmanBros_gray, 3)
print('Top 3 corners: Allman Brothers')
print('X coordinates: ', allmanBrosX[0:3])
print('Y coordinates: ', allmanBrosY[0:3])
for i in range(100):
    cv2.circle(allmanBros_copy2, (int(allmanBrosY[i]),int(allmanBrosX[i])), 4, color, 1)

# display images
# cv2.imshow('Elvis', elvis_copy2.astype(np.uint8))
# cv2.waitKey()
# cv2.imshow('Chartres', chartres_copy2.astype(np.uint8))
# cv2.waitKey()
# cv2.imshow('Calvin & Hobbes', calvinHobbes_copy2.astype(np.uint8))
# cv2.waitKey()
# cv2.imshow('Allman Brothers', allmanBros_copy2.astype(np.uint8))
# cv2.waitKey()

## ----------------------------------------------------------------------------------
##                                  Part (i)
## Put the two display images (own implementation on right) together and save images 
## ----------------------------------------------------------------------------------
elvisComparison = np.concatenate((elvis_copy, elvis_copy2), axis=1)
chartresComparison = np.concatenate((chartres_copy, chartres_copy2), axis=1)
calvinHobbesComparison = np.concatenate((calvinHobbes_copy, calvinHobbes_copy2), axis=1)
allmanBrosComparison = np.concatenate((allmanBros_copy, allmanBros_copy2), axis=1)

cv2.imwrite('Elvis_Comparison.png', elvisComparison)
cv2.imwrite('Chartres_Comparison.png', chartresComparison)
cv2.imwrite('CalvinHobbes_Comparison.png', calvinHobbesComparison)
cv2.imwrite('AllmanBros_Comparison.png', allmanBrosComparison)

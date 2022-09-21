# import libraries
import numpy as np
np.set_printoptions(suppress=True)
import cv2
import matplotlib.pyplot as plt

# define a function to combine two images, return the output image array
# should be working with uint8 as that's what the cv2 functions take as inputs
def imgStitching(img1, img2, filename, run): # img1 and img2 are type uint8
    imgOut_cropped = []

    # convert to grayscale
    if run==1:
        img1 = ((img1.astype(np.float32)[:,:,2] + img1.astype(np.float32)[:,:,1] + img1.astype(np.float32)[:,:,0]) / 3).astype(np.uint8)
        img2 = ((img2.astype(np.float32)[:,:,2] + img2.astype(np.float32)[:,:,1] + img2.astype(np.float32)[:,:,0]) / 3).astype(np.uint8)
    else:
        img2 = ((img2.astype(np.float32)[:,:,2] + img2.astype(np.float32)[:,:,1] + img2.astype(np.float32)[:,:,0]) / 3).astype(np.uint8)


    ## STEP 1
    # Detect keypoints in the image and characterize them
    sift1 = cv2.SIFT_create()
    sift2 = cv2.SIFT_create()

    kp1, des1 = sift1.detectAndCompute(img1, None)
    kp2, des2 = sift2.detectAndCompute(img2, None)

    ## STEP 2
    # Match the keypoints
    bf = cv2.BFMatcher()
    matches = bf.match(des1, des2)

    ## STEP 3
    # Filter the matches
    # reference: https://stackoverflow.com/questions/3766633/how-to-sort-with-lambda-in-python
    matches = sorted(matches, key=lambda x:x.distance)

    idx1 = []
    idx2 = []
    for i in range(25):
        temp1 = matches[i].queryIdx # img1
        temp2 = matches[i].trainIdx # img2

        idx1.append(cv2.KeyPoint_convert(kp1)[temp1])
        idx2.append(cv2.KeyPoint_convert(kp2)[temp2])


    idx1 = np.array(idx1)
    idx2 = np.array(idx2)
    
    ## STEP 4
    # Find the geometric mapping from image 1 to image 2 
    if filename == 'blacksburg':
        h, status = cv2.findHomography(idx2, idx1)
        print(h)
    else:
        h, status = cv2.findHomography(idx2, idx1)
        print(h)

    ## STEP 5
    # Transform the second image to lie in the coords of the first
    # Combine the two images
    if filename == 'blacksburg':
        if run == 1:
            imgOut = cv2.warpPerspective(img2, h, (img2.shape[1]+img1.shape[1], img2.shape[0]+img1.shape[0]))
            savename = filename + '1_warped.png'
            cv2.imwrite(savename, imgOut)
            # -----------------------------
            # perform blending in real time
            halfpt = int(np.round(np.shape(img1)[0] / 2))
            stillBlack=True
            colVal = 0
            while stillBlack:
                if all(imgOut[halfpt][colVal] != [0,0,0]): # if not black
                    # that is the seam value
                    seam1 = colVal
                    stillBlack = False
                colVal = colVal + 1

            seam2 = np.shape(img1)[1]-5

            for row in range(np.shape(img1)[0]-1):
                for col in range(np.shape(imgOut)[1]-1):
                    if (col < seam1):
                        imgOut[row][col] = img1[row][col]
                    elif (col >= seam1) & (col < seam2):
                        w = seam1 / col
                        imgOut[row][col] = (img1[row][col].astype(np.float32) * w + imgOut[row][col].astype(np.float32) * (1-w)).astype(np.int32)
                    else:
                        imgOut[row][col] = imgOut[row][col] #+ diffPixel
        else:
            imgOut = cv2.warpPerspective(img2, h, (img2.shape[1]+img1.shape[1], img2.shape[0]+img1.shape[0]))
            savename = filename + '2_warped.png'
            cv2.imwrite(savename, imgOut)
            
            # find the halfway point
            halfpt = int(np.round(np.shape(img1)[0] / 4))

            # find the column 
            partofpicture=True
            i = 0
            while partofpicture:
                if all(img1[halfpt][i] == [0, 0, 0]):
                    seam2 = i
                    partofpicture = False
                i = i+1

            partofpicture=True
            i = 0
            while partofpicture:
                if all(imgOut[halfpt][i] != [0, 0, 0]):
                    seam1 = i
                    partofpicture = False
                i = i+1

            for row in range(np.shape(img1)[0]-1):
                for col in range(np.shape(img1)[1]-1):
                    if col <= seam1:
                        imgOut[row][col] = img1[row][col] 
                    else:                       
                        imgOut[row][col] = imgOut[row][col] 


    # ---------------------------------
    #    HOMOGRAPHIC TRANSFORMATION
    # ---------------------------------
    else:
        
        if run == 1:
            imgOut = cv2.warpPerspective(img2, h, (img2.shape[1]+img1.shape[1], img2.shape[0]+img1.shape[0]))
            savename = filename + '1_warped.png'
            cv2.imwrite(savename, imgOut)
            # -----------------------------
            # perform blending in real time
            halfpt = int(np.round(np.shape(img1)[0] / 2))
            stillBlack=True
            colVal = 0
            while stillBlack:
                if all(imgOut[halfpt][colVal] != [0,0,0]): # if not black
                    # that is the seam value
                    seam1 = colVal
                    stillBlack = False
                colVal = colVal + 1

            seam2 = np.shape(img1)[1]

            for row in range(np.shape(img1)[0]-1):
                for col in range(np.shape(imgOut)[1]-1):
                    if (col < seam1):
                        imgOut[row][col] = img1[row][col]
                    elif (col >= seam1) & (col < seam2):
                        w = seam1 / col
                        imgOut[row][col] = (img1[row][col].astype(np.float32) * w + imgOut[row][col].astype(np.float32) * (1-w)).astype(np.int32)
                    else:
                        diffPixel = (img1[0][seam2-1].astype(np.float32) - imgOut[0][seam2-1].astype(np.float32)).astype(np.int32)
                        imgOut[row][col] = imgOut[row][col] + diffPixel

        else:
            imgOut = cv2.warpPerspective(img2, h, (img2.shape[1]+img1.shape[1], img2.shape[0]+img1.shape[0]))
            savename = filename + '2_warped.png'
            cv2.imwrite(savename, imgOut)

            halfpt = int(np.round(np.shape(img1)[0] / 4))
            # calculate seam 1
            stillBlack=True
            colVal = 0
            while stillBlack:
                if all(imgOut[halfpt][colVal] != [0,0,0]): # if not black
                    # that is the seam value
                    seam1 = colVal
                    stillBlack = False
                colVal = colVal + 1

            # calculate seam 2
            stillBlack=True
            colVal = 0
            while stillBlack:
                if all(img1[halfpt][colVal] <= [15,15,15]): # if black
                    # that is the seam value
                    seam2 = colVal-20
                    stillBlack = False
                colVal = colVal + 1

            diffPixel = (img1[halfpt][seam1].astype(np.float32) - imgOut[halfpt][seam1+1].astype(np.float32)).astype(np.int32)
            for row in range(np.shape(img1)[0]-1):
                for col in range(np.shape(imgOut)[1]-1):
                    if (col < seam1):
                        imgOut[row][col] = img1[row][col]
                    elif (col >= seam1) & (col < seam2):
                        w = seam1 / col
                        imgOut[row][col] = (img1[row][col].astype(np.float32) * (w) + imgOut[row][col].astype(np.float32) * (1-w)).astype(np.int32)
                    else:
                        if filename == 'diamondhead':
                            imgOut[row][col] = imgOut[row][col]
                        else:
                            imgOut[row][col] = imgOut[row][col] + diffPixel

    if run!=1:
        # crop image
        stillBlack=True
        colVal = 0
        while stillBlack:
            if filename == 'blacksburg':
                if all(imgOut[halfpt-1][colVal] == [0,0,0]): # if black
                    # that is the seam value
                    lastCol = colVal
                    stillBlack = False
                colVal = colVal + 1
            else:
                if all(imgOut[halfpt-1][colVal] < [40,40,40]) | all(imgOut[halfpt][colVal] < [15,15,15]): # if black
                    # that is the seam value
                    lastCol = colVal
                    stillBlack = False
                colVal = colVal + 1

        half_colpt = int(np.round(np.shape(img1)[1] / 1.5))
        stillBlack=True
        rowVal = 500
        while stillBlack:
            if all(imgOut[rowVal][half_colpt] == [0,0,0]): # if black
                # that is the seam value
                lastRow = rowVal+20
                stillBlack = False
            rowVal = rowVal + 1
            
        imgOut_cropped = imgOut[0:lastRow, 0:lastCol]

    return imgOut, imgOut_cropped

# RIO 
# Load the images and convert to grayscale
rio0 = cv2.imread('rio-00.png').astype(np.uint8)
rio1 = cv2.imread('rio-01.png').astype(np.uint8)
rio2 = cv2.imread('rio-02.png').astype(np.uint8)

# call the image stitching function
rio_12, rio_none = imgStitching(rio0, rio1, 'rio', 1) # combined rio images 1 and 2
rio_123, rio_cropped = imgStitching(rio_12, rio2, 'rio', 2) # combined image 1,2 with image 3
cv2.imwrite('rioCombo.png', rio_123)
cv2.imwrite('rioCombo_cropped.png', rio_cropped)

# # # DIAMONDHEAD
# Load the images and convert to grayscale
dh0 = cv2.imread('diamondhead-00.png').astype(np.uint8)
dh1 = cv2.imread('diamondhead-01.png').astype(np.uint8)
dh2 = cv2.imread('diamondhead-02.png').astype(np.uint8)

# call the image stitching function
dh_12, dh_none = imgStitching(dh0, dh1, 'diamondhead', 1) # combined rio images 1 and 2
dh_123, dh_cropped = imgStitching(dh_12, dh2, 'diamondhead', 2) # combined image 1,2 with image 3
cv2.imwrite('diamondheadCombo.png', dh_123)
cv2.imwrite('diamondheadCombo_cropped.png', dh_cropped)

# BLACKSBURG
# Load the images and convert to grayscale
bb0 = cv2.imread('blacksburg-00.png').astype(np.uint8)
bb1 = cv2.imread('blacksburg-01.png').astype(np.uint8)
bb2 = cv2.imread('blacksburg-02.png').astype(np.uint8)

# call the image stitching function
bb_12, bb_none = imgStitching(bb0, bb1, 'blacksburg', 1) # combined rio images 1 and 2
bb_123, bb_cropped = imgStitching(bb_12, bb2, 'blacksburg', 2) # combined image 1,2 with image 3
cv2.imwrite('blacksburgCombo.png', bb_123)
cv2.imwrite('blacksburgCombo_cropped.png', bb_cropped)




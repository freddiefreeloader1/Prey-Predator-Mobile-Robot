import cv2
import matplotlib.pyplot as plt
import skimage
from skimage.filters import try_all_threshold
import matplotlib.patches as mpatches
import numpy as np

def img_processing(imagein):
    img = cv2.imread(imagein)
    imgI = cv2.imread('inverted.jpg')

    '''
    cv2.imshow('image',img)
    k = cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    np.set_printoptions(threshold=np.inf)


    img_gray = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)


    him = cv2.calcHist([img_gray],[0],None,[256],[0,256])
    global_thresh = skimage.filters.threshold_otsu(img_gray)
    binary_global = (img_gray > global_thresh)
    th_img = binary_global.astype(np.uint8)


    block_size = 101
    local_thresh = skimage.filters.threshold_local(img_gray,block_size, offset=10)
    binary_local = img_gray > local_thresh

    th_local = binary_local.astype(np.uint8)
    inverted_img = np.ones((480,640))
    ####
    inverted_gray = cv2.cvtColor(imgI, cv2.COLOR_BGR2GRAY)
    local_th2 = skimage.filters.threshold_local(inverted_gray,block_size, offset=10)
    binary_inv = inverted_gray > local_th2




    for i in range(480):
        for j in range(640):
            if binary_inv[i][j] == 1:
                inverted_img[i][j] = 0
            else:
                inverted_img[i][j] == 1
    #print(inverted_img)
    #plt.imshow(inverted_img, cmap = "gray")
    #plt.show()



    ####


    #plt.imshow(th_local, cmap ="gray")
    #plt.show()
    dimensions = img.shape


    kernel1 = np.ones((17,17), np.uint8)
    kernel2 = np.ones((3,3), np.uint8)

    erosion = cv2.erode(th_local,kernel1,iterations = 2)
    opening = cv2.dilate(erosion,kernel2,iterations = 1)


    kernel = np.ones((17, 17), np.uint8)
    #opening = cv2.morphologyEx(th_local, cv2.MORPH_OPEN, kernel, iterations = 2)
    #closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations = 1)

    #plt.imshow(opening, cmap = "gray")
    #plt.show()

    ## fig, ax = plt.subplots()
    labeled = skimage.measure.label(opening, connectivity = 1)





    #ax.imshow(opening, cmap = "gray")
    centroids = []
    for region in skimage.measure.regionprops(labeled):
        
        # take regions with large enough areas
        if region.area >= 900 and region.area <= 10000 and region.perimeter < 500:
            # draw rectangle around segmented coins
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                    fill=False, edgecolor='green', linewidth=2)
            centroids.append(region.centroid) # for search part
            #ax.add_patch(rect)
        if region.area <= 200 and region.area >= 100:
            # draw rectangle around segmented coins
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                    fill=False, edgecolor='red', linewidth=2)
            #ax.add_patch(rect)

    #ax.set_axis_off()
    #plt.tight_layout()
    #plt.show()
    #print(centroids)
    #print(len(centroids))
    #print(th_img.shape)




    ##############GREEN###############
    image = cv2.imread(imagein)
    #cv2.imshow("Original", image)
    result = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # lower boundary RED color range values; Hue (0 - 10)
    lower1 = np.array([40, 100, 20])
    upper1 = np.array([80, 255, 255])
    lower_mask = cv2.inRange(image, lower1, upper1)
    full_mask = lower_mask
    result = cv2.bitwise_and(result, result, mask=full_mask)

    ##Erosion
    kernel =  np.ones((13,13), np.uint8)
    kernel2 =  np.ones((5,5), np.uint8)
    full_mask = cv2.erode(full_mask,kernel,iterations = 2)
    full_mask = cv2.dilate(full_mask, kernel2, iterations = 2)
    ##i-------i
    ######
    #plt.imshow(full_mask, cmap = 'gray')
    #plt.show()
    for i in range(480):
        for j in range(640):
            if binary_inv[i][j] == 0:
                full_mask[i][j] = 0
            
    #plt.imshow(full_mask, cmap = 'gray')
    #plt.show()

    labeledG = skimage.measure.label(full_mask, connectivity = 1)


    #####
    centroidsG = []
    for region in skimage.measure.regionprops(labeledG):

        # take regions with large enough areas
        if region.area >= 1500 and region.area <= 50000:
            # draw rectangle around segmented coins
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                    fill=False, edgecolor='green', linewidth=2)
            centroidsG.append(region.centroid) # for search part
            #ax.add_patch(rect)
        if region.area <= 200 and region.area >= 100:
            # draw rectangle around segmented coins
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                    fill=False, edgecolor='red', linewidth=2)
            #ax.add_patch(rect)



    #print(centroidsG)
    #print(len(centroidsG))

    #plt.imshow(full_mask, cmap = 'gray')
    #plt.show()
    #print(full_mask.shape)
    ################## - BLUE - #################


    image = cv2.imread(imagein)
    #cv2.imshow("Original", image)
    result = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # lower boundary RED color range values; Hue (0 - 10)
    lower1 = np.array([100, 100, 20])
    upper1 = np.array([140, 255, 255])
    lower_mask = cv2.inRange(image, lower1, upper1)
    full_mask = lower_mask
    result = cv2.bitwise_and(result, result, mask=full_mask)

    ##Erosion
    kernel =  np.ones((13,13), np.uint8)
    kernel2 =  np.ones((5,5), np.uint8)
    full_mask = cv2.erode(full_mask,kernel,iterations = 2)
    full_mask = cv2.dilate(full_mask, kernel2, iterations = 2)
    ##i-------i
    ##
    #plt.imshow(full_mask, cmap = 'gray')
    #plt.show()
    for i in range(480):
        for j in range(640):
            if binary_inv[i][j] == 0:
                full_mask[i][j] = 0

    #plt.imshow(full_mask, cmap = 'gray')
    #plt.show()

    ##

    labeledB = skimage.measure.label(full_mask, connectivity = 1)

    centroidsB = []

    for region in skimage.measure.regionprops(labeledB):

        # take regions with large enough areas
        if region.area >= 800 and region.area <= 50000:
            # draw rectangle around segmented coins
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                    fill=False, edgecolor='green', linewidth=2)
            centroidsB.append(region.centroid) # for search part
            #ax.add_patch(rect)
        if region.area <= 200 and region.area >= 100:
            # draw rectangle around segmented coins
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                    fill=False, edgecolor='red', linewidth=2)
            #ax.add_patch(rect)

    #print(len(centroidsB))

    #plt.imshow(full_mask, cmap = 'gray')
    #plt.show()



    ############### - RED - #################

    img = cv2.imread(imagein)

    result = img.copy()

    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # lower boundary RED color range values; Hue (0 - 10)
    lower1 = np.array([0, 100, 20])
    upper1 = np.array([10, 255, 255])
    
    # upper boundary RED color range values; Hue (160 - 180)
    lower2 = np.array([160,100,20])
    upper2 = np.array([179,255,255])
    
    lower_mask = cv2.inRange(img, lower1, upper1)
    upper_mask = cv2.inRange(img, lower2, upper2)

    full_mask = lower_mask + upper_mask;


    result = cv2.bitwise_and(result, result, mask=full_mask)


    ##Erosion
    kernel =  np.ones((13,13), np.uint8)
    kernel2 =  np.ones((5,5), np.uint8)
    full_mask = cv2.erode(full_mask,kernel,iterations = 2)
    full_mask = cv2.dilate(full_mask, kernel2, iterations = 2)
    ##i-------i
    ##
    #plt.imshow(full_mask, cmap = 'gray')
    #plt.show()
    for i in range(480):
        for j in range(640):
            if binary_inv[i][j] == 0:
                full_mask[i][j] = 0

    #plt.imshow(full_mask, cmap = 'gray')
    #plt.show()

    ##
    labeledR = skimage.measure.label(full_mask, connectivity = 1)

    centroidsR = []

    for region in skimage.measure.regionprops(labeledR):

        # take regions with large enough areas
        if region.area >= 1500 and region.area <= 50000:
            # draw rectangle around segmented coins
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                    fill=False, edgecolor='green', linewidth=2)
            centroidsR.append(region.centroid) # for search part
            #ax.add_patch(rect)
        if region.area <= 200 and region.area >= 100:
            # draw rectangle around segmented coins
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                    fill=False, edgecolor='red', linewidth=2)
            #ax.add_patch(rect)



    #print(centroidsR)
    #print(len(centroidsR))

    #plt.imshow(full_mask, cmap = 'gray')
    #plt.show()

    ############ - ORANGE - ################

    image = cv2.imread(imagein)
    #cv2.imshow("Original", image)
    result = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # lower boundary RED color range values; Hue (0 - 10)
    lower1 = np.array([15, 100, 20])
    upper1 = np.array([40, 255, 255])
    lower_mask = cv2.inRange(image, lower1, upper1)
    full_mask = lower_mask
    result = cv2.bitwise_and(result, result, mask=full_mask)

    ##Erosion
    kernel =  np.ones((13,13), np.uint8)
    kernel2 =  np.ones((5,5), np.uint8)
    full_mask = cv2.erode(full_mask,kernel,iterations = 2)
    full_mask = cv2.dilate(full_mask, kernel2, iterations = 2)
    ##i-------i
    ##
    #plt.imshow(full_mask, cmap = 'gray')
    #plt.show()
    for i in range(480):
        for j in range(640):
            if binary_inv[i][j] == 0:
                full_mask[i][j] = 0

    #plt.imshow(full_mask, cmap = 'gray')
    #plt.show()


    ##
    labeledO = skimage.measure.label(full_mask, connectivity = 1)

    centroidsO = []

    for region in skimage.measure.regionprops(labeledO):

        # take regions with large enough areas
        if region.area >= 1500 and region.area <= 50000:
            # draw rectangle around segmented coins
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                    fill=False, edgecolor='green', linewidth=2)
            centroidsO.append(region.centroid) # for search part
            #ax.add_patch(rect)
        if region.area <= 200 and region.area >= 100:
            # draw rectangle around segmented coins
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                    fill=False, edgecolor='red', linewidth=2)
            #ax.add_patch(rect)


    #print(centroidsO)
    #print(len(centroidsO))

    #plt.imshow(full_mask, cmap = 'gray')
    #plt.show()




    #################### Convert to Grids #################


    cy = []
    cx = []
    for i in range(len(centroids)):
        cy.append(centroids[i][0])
        cx.append(centroids[i][1])

    #cx.sort()
    miny = min(cy)
    maxy = max(cy)
    minx = min(cx)
    maxx = max(cx)

    disty = (maxy - miny)/5
    distx = (maxx - minx)/7


    redy = []
    redx = []
    greeny = []
    greenx = []
    bluey = []
    bluex = []
    orangey = []
    orangex = []

    for k in range(len(centroidsR)):
        redy.append(round((centroidsR[k][0]-miny)/disty))
        redx.append(round((centroidsR[k][1]-minx)/distx))
    for k in range(len(centroidsG)):
        greeny.append(round((centroidsG[k][0]-miny)/disty))
        greenx.append(round((centroidsG[k][1]-minx)/distx))
    for k in range(len(centroidsB)):
        bluey.append(round((centroidsB[k][0]-miny)/disty))
        bluex.append(round((centroidsB[k][1]-minx)/distx))
    for k in range(len(centroidsO)):
        orangey.append(round((centroidsO[k][0]-miny)/disty))
        orangex.append(round((centroidsO[k][1]-minx)/distx))



    game_map = np.zeros((6,8),dtype = str)
    for i in range(6):
        for j in range(8):
            game_map[i][j] = '.'


    for i in range(len(redy)):
        game_map[redy[i],redx[i]] = 'R'
    for i in range(len(greeny)):
        game_map[greeny[i], greenx[i]] = 'G'
    for i in range(len(bluey)):
        game_map[bluey[i],bluex[i]] = 'B'
    for i in range(len(orangey)):
        game_map[orangey[i],orangex[i]] = 'O'

    #print(game_map)
    #print(i for i in game_map[1])
    stri = ''
    finalmap = []
    for i in range(6):
        for k in range(8):
            stri = stri + game_map[i][k]
        finalmap.append(stri) 
        stri = ''
    #print(finalmap)
    return finalmap
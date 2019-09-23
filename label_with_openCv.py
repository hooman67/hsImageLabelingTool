import cv2,glob,numpy as np
import xml.etree.ElementTree as ET
from matplotlib import pyplot as plt


def saveStoredPointsAsXml(file_name, output_folder):
    global  stored_xy_tt, stored_xy_ls, stored_xy_le, stored_xy_cl, stored_xy_bk, width, length, length_orig, width_orig

    new_root = ET.Element("hs_frame_wear_landmarks")

    img_name=ET.SubElement(new_root,"img_name")
    img_name.text=file_name



    np_tt=np.array(stored_xy_tt,dtype=np.float)
    np_tt[:,0]=np_tt[:,0]/width
    np_tt[:,1]=np_tt[:,1]/length

   # np_tt=np.transpose(np_tt)

    tt_landmarks=ET.SubElement(new_root,"toothTip")
    counter = 1
    for point in np_tt:
        name = 'toothTip_' + str(counter)
        ET.SubElement(tt_landmarks, name, x=str(point[0]), y=str(point[1]))
        counter+=1


    np_ls=np.array(stored_xy_ls,dtype=np.float)
    np_ls[:,0]=np_ls[:,0]/width
    np_ls[:,1]=np_ls[:,1]/length

   # np_ls=np.transpose(np_ls)

    ls_landmarks=ET.SubElement(new_root,"lipShroud")
    counter = 1
    for point in np_ls:
        name = 'lipShroud_' + str(counter)
        ET.SubElement(ls_landmarks, name, x=str(point[0]), y=str(point[1]))
        counter+=1



    np_le=np.array(stored_xy_le,dtype=np.float)
    np_le[:,0]=np_le[:,0]/width
    np_le[:,1]=np_le[:,1]/length

  #  np_le=np.transpose(np_le)

    le_landmarks=ET.SubElement(new_root,"liftingEye")

    counter = 1
    for point in np_le:
        name = 'liftingEye_' + str(counter)
        ET.SubElement(le_landmarks, name, x=str(point[0]), y=str(point[1]))
        counter+=1



    np_cl=np.array(stored_xy_cl,dtype=np.float)
    np_cl[:,0]=np_cl[:,0]/width
    np_cl[:,1]=np_cl[:,1]/length

  #  np_cl=np.transpose(np_cl)

    cl_landmarks=ET.SubElement(new_root,"castLip")

    counter = 1
    for point in np_cl:
        name = 'castLip_' + str(counter)
        ET.SubElement(cl_landmarks, name, x=str(point[0]), y=str(point[1]))
        counter+=1



    np_bk=np.array(stored_xy_bk,dtype=np.float)
    np_bk[:,0]=np_bk[:,0]/width
    np_bk[:,1]=np_bk[:,1]/length

   # np_bk=np.transpose(np_bk)

    bk_landmarks=ET.SubElement(new_root,"bucketLandmark")
    counter = 1
    for point in np_bk:
        name = 'bucketLandmark_' + str(counter)
        ET.SubElement(bk_landmarks, name, x=str(point[0]), y=str(point[1]))
        counter+=1



    tree = ET.ElementTree(new_root)
    tree.write(output_folder+file_name+'.xml')# wrap it in an ElementTree instance, and save as XML
    print('XMLs created')
    return None


def click_and_crop(event, x, y, flags, param):
    global  numberOfTeeth, stored_xy_tt, stored_xy_ls, stored_xy_le, stored_xy_cl, stored_xy_bk, width, length

    if event == cv2.EVENT_LBUTTONDOWN:

        if len(stored_xy_tt) < numberOfTeeth:
            cv2.rectangle(image,(x-2,y-2),(x+2,y+2),(0, 255, 0))
            cv2.imshow(window_title, image)
            
            stored_xy_tt.append([x,y])

        elif len(stored_xy_ls) < numberOfTeeth:
            cv2.rectangle(image,(x-2,y-2),(x+2,y+2),(255, 0, 0))
            cv2.imshow(window_title, image)
            
            stored_xy_ls.append([x,y])

        elif len(stored_xy_le) < numberOfTeeth:
            cv2.rectangle(image,(x-2,y-2),(x+2,y+2),(0, 0, 255))
            cv2.imshow(window_title, image)
            
            stored_xy_le.append([x,y])

        elif len(stored_xy_cl) < numberOfTeeth:
            cv2.rectangle(image,(x-2,y-2),(x+2,y+2),(255, 255, 0))
            cv2.imshow(window_title, image)
            
            stored_xy_cl.append([x,y])

        elif len(stored_xy_bk) < numberOfTeeth:
            cv2.rectangle(image,(x-2,y-2),(x+2,y+2),(0, 255, 255))
            cv2.imshow(window_title, image)
            
            stored_xy_bk.append([x,y])
      
        else:
            pass
      

def overlap_image_labels(image):
    stored_xy_tt, stored_xy_ls, stored_xy_le, stored_xy_cl, stored_xy_bk, 
    overlapped_im=image
    for point in stored_xy_tt:
        overlapped_im[point[1]-2:point[1]+2,point[0]-2:point[0]+2,0]=0
        overlapped_im[point[1]-2:point[1]+2,point[0]-2:point[0]+2,1]=255
        overlapped_im[point[1]-2:point[1]+2,point[0]-2:point[0]+2,2]=0

    for point in stored_xy_ls:
        overlapped_im[point[1]-2:point[1]+2,point[0]-2:point[0]+2,0]=255
        overlapped_im[point[1]-2:point[1]+2,point[0]-2:point[0]+2,1]=0
        overlapped_im[point[1]-2:point[1]+2,point[0]-2:point[0]+2,2]=0

    for point in stored_xy_le:
        overlapped_im[point[1]-2:point[1]+2,point[0]-2:point[0]+2,0]=0
        overlapped_im[point[1]-2:point[1]+2,point[0]-2:point[0]+2,1]=0
        overlapped_im[point[1]-2:point[1]+2,point[0]-2:point[0]+2,2]=255

    for point in stored_xy_cl:
        overlapped_im[point[1]-2:point[1]+2,point[0]-2:point[0]+2,0]=255
        overlapped_im[point[1]-2:point[1]+2,point[0]-2:point[0]+2,1]=255
        overlapped_im[point[1]-2:point[1]+2,point[0]-2:point[0]+2,2]=0

    for point in stored_xy_bk:
        overlapped_im[point[1]-2:point[1]+2,point[0]-2:point[0]+2,0]=0
        overlapped_im[point[1]-2:point[1]+2,point[0]-2:point[0]+2,1]=255
        overlapped_im[point[1]-2:point[1]+2,point[0]-2:point[0]+2,2]=255

    return overlapped_im


def printLabels():
    print('StoredLabels:\n')
    print('stored_xy_tt')
    print(stored_xy_tt)
    print('stored_xy_ls')
    print(stored_xy_ls)
    print('stored_xy_le')
    print(stored_xy_le)
    print('stored_xy_cl')
    print(stored_xy_cl)
    print('stored_xy_bk')
    print(stored_xy_bk)
    print('\n\n')

    image = overlap_image_labels(clone.copy())


'''
#############################################################################
#####################   Press [q] to reset the labels   #####################
#############################################################################
#####################   Press [s] to export the labels  #####################
#############################################################################
#####################   Press [p] to print the labels   #####################
#############################################################################
'''
numberOfTeeth = 6
folder_source = '/media/hooman/961293e3-04a5-40c5-afc0-2b205d0a7067/WM_PROJECT/algorithmDev/wmAlgo_usingWearLandmarsk_optical_hydraulics/try1/wmdlLogs_aitik_Komatsu_SH1142_PC5500_2019-02-26_to_2019-03-10/referenceFrames/temp/i/' # location of images to be labeled
output_folder = '/media/hooman/961293e3-04a5-40c5-afc0-2b205d0a7067/WM_PROJECT/algorithmDev/wmAlgo_usingWearLandmarsk_optical_hydraulics/try1/wmdlLogs_aitik_Komatsu_SH1142_PC5500_2019-02-26_to_2019-03-10/referenceFrames/temp/o/' # where to store the labels 

global_image_list=glob.glob(folder_source+'*.png') # Generating the list of images to be labeled
# change the '.jpg' extension if other image types are used...

fig = plt.figure()
plt.ion()
for (image_nr,image_path) in enumerate(global_image_list):
    window_title='image'
                 
    if image_nr<0: # In case the previous labeling session was suddenly stopped. It basically overlooks all previous images
        pass
    else:
        image_original = cv2.imread(image_path,cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR) # read the image having the orientation it was saved with, otherwise its rotation is reset
        length_orig, width_orig, dim=np.shape(image_original) # image width, length and dimensions

        image = cv2.resize(image_original,(256*4,160*4)) # resizin the image to something that can fit easily on the screen
        length, width, dim=np.shape(image)

        clone = image.copy() # the initial image is stored, just in case
        cv2.namedWindow(window_title)
        cv2.setMouseCallback(window_title, click_and_crop)

        stored_xy_tt=[]
        stored_xy_ls=[]
        stored_xy_le=[]
        stored_xy_cl=[]
        stored_xy_bk=[]


         
    # keep looping until the 's' key is pressed
        while True:
    # display the image and wait for a keypress
            cv2.imshow(window_title, image)
            key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, reset the labels
            if key == ord("q"):
                image = clone.copy()
                stored_xy_tt=[]
                stored_xy_ls=[]
                stored_xy_le=[]
                stored_xy_cl=[]
                stored_xy_bk=[]

    # if the 's' key is pressed, break from the loop
            elif key == ord("s"):
                overlapped_image=overlap_image_labels(image)

                splits=str.split(image_path,'/')

                image_name = splits[-1][:-4]

                fig_name = image_name+'_labeled.png'

                cv2.imwrite(output_folder + fig_name,overlapped_image)
                
                plt.imshow(cv2.cvtColor(overlapped_image,cv2.COLOR_BGR2RGB))
                plt.title('image:[%s]:' % image_name)
                plt.tight_layout()
                plt.show()

                xml_name=image_name+'_landmarkCoords'
                saveStoredPointsAsXml(xml_name, output_folder)

                print ('Created XML for image Nr%d' % image_nr)
                break

    # if the 'p' key is pressed,  print the stored points...
            elif key == ord("p"): #let's POP the last element in the list!!!
                printLabels()
                 
                 
plt.ioff()
cv2.destroyAllWindows()
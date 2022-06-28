import cv2
import streamlit as st
import os
from PIL import Image

def load_image(image_file):
	img = Image.open(image_file)
	return img
st.subheader("Image")
image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])

if image_file is not None:
        # To See details
        file_details = {"filename":image_file.name, "filetype":image_file.type,
                        "filesize":image_file.size}
        st.write(file_details)
        st.image(image_file)
        # To View Uploaded Image
        
        with open(os.path.join("images",image_file.name),"wb") as f: 
            f.write(image_file.getbuffer())         
            st.success("Saved File")
        img=cv2.imread(os.path.join("images",image_file.name))
        def filters(img, f_type = "blur"):
            '''
            ### Filtering ###
            img: image
            f_type: {blur: blur, gaussian: gaussian, median: median}
            '''
            if f_type == "blur":
                image=img.copy()
                fsize = 9
                return cv2.blur(image,(fsize,fsize))
            
            elif f_type == "gaussian":
                image=img.copy()
                fsize = 9
                return cv2.GaussianBlur(image, (fsize, fsize), 0)
            
            elif f_type == "median":
                image=img.copy()
                fsize = 9
                return cv2.medianBlur(image, fsize)
            elif f_type == "flip1":
                image=img.copy()
                fsize = 9
                return cv2.flip(image, 0)

            elif f_type == "flip2":
                image=img.copy()
                fsize = 9
                return cv2.medianBlur(image, fsize)

            elif f_type == "flip3":
                image=img.copy()
                fsize = 9
                return cv2.medianBlur(image, fsize)


        
        image1=filters(img, f_type = "blur")
        image3=filters(img, f_type = "median")
        image2=filters(img, f_type = "gaussian")
        image3=filters(img, f_type = "flip1")
        image3=filters(img, f_type = "flip2")
        image3=filters(img, f_type = "flip3")

        st.subheader("image augmentations")
        st.image([image1])
        st.write("     ")
        st.image([image2])
        st.write("     ")
        st.image([image3])
        st.write("     ")
        st.image([image4])
        st.write("     ")
        st.image([image5])
        st.write("     ")
        st.image([image6])
        try:
            def boxesFromYOLO(imagePath,labelPath):
                image = cv2.imread(imagePath)
                (hI, wI) = image.shape[:2]
                lines = [line.rstrip('\n') for line in open(labelPath)]
                #if(len(objects)<1):
                #    raise Exception("The xml should contain at least one object")
                boxes = []
                if lines != ['']:
                    for line in lines:
                        components = line.split(" ")
                        category = components[0]
                        x  = int(float(components[1])*wI - float(components[3])*wI/2)
                        y = int(float(components[2])*hI - float(components[4])*hI/2)
                        h = int(float(components[4])*hI)
                        w = int(float(components[3])*wI)
                        boxes.append((category, (x, y, w, h)))
                return (image,boxes)

            categoriesColors = {11: (255,0,0),14:(0,0,255)}

            def showBoxes(image,boxes):
                cloneImg = image.copy()
                for box in boxes:
                    if(len(box)==2):
                        (category, (x, y, w, h))=box
                    else:
                        (category, (x, y, w, h),_)=box
                    if int(category) in categoriesColors.keys():
                        cv2.rectangle(cloneImg,(x,y),(x+w,y+h),categoriesColors[int(category)],5)
                    else:
                        cv2.rectangle(cloneImg,(x,y),(x+w,y+h),(0,255,0),5)
                return cloneImg[:,:,::-1]
            img=os.path.join("images",image_file.name)
            file=os.path.join("images",image_file.name).split(".")[0]+".txt"
            st.write(img)
            st.write(file)
            (image,boxes)=boxesFromYOLO(img,file)
            final_pred=showBoxes(image,boxes)
            st.write(image)
            st.image(final_pred)
            st.write()
        except:
            st.write("Low Resolution Picture , please improve quality")
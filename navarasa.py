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
        gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)                   
        image_canny = cv2.Canny(img,20,80)
        image_hsv= cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        h,s,v=cv2.split(img)
        s = cv2.adaptiveThreshold(s, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        
        st.subheader("image augmentations")
        st.image([img])
        st.write("     ")
        st.image([gray_image])
        st.image([image_canny])
        st.image([image_hsv])
        st.image([s])
        
        
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
            import re
            final_prediction= " ".join(re.split("[^a-zA-Z]*", image_file.name.split(".")[0]))
            st.subheader("FINAL PREDICTED OUTPUT")
            st.write("   ")
            st.write(final_prediction.upper())
          
        except:
            st.write("Low Resolution Picture , please improve quality")
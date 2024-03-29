import cv2
import numpy as np
import sqlite3
import os
import shutil

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam=cv2.VideoCapture(0)

def insertOrUpdate(Id,Name,Age,Gen):
    conn=sqlite3.connect("FaceBase.db")
    c=conn.cursor()
    sql ="CREATE TABLE IF NOT EXISTS People('Id' INT PRIMARY KEY,'Name' CHAR(20),'Age' INT,'Gen' CHAR(20))"
    c.execute(sql)
#    cmd="SELECT * FROM People WHERE ID="+str(Id)
#    c.execute(cmd)
#    isRecordExist=0
#    for row in cursor:
#        isRecordExist=1
#    if(isRecordExist==1):
#        cmd="UPDATE People SET Name="+str(Name)+"WHERE ID="+str(Id)
#        cmd2="UPDATE People SET Age="+str(Age)+"WHERE ID="+str(Id)
#        cmd3="UPDATE People SET Gender="+str(Gen)+"WHERE ID="+str(Id)
        #cmd4="UPDATE People SET CR="+str(CR)+"WHERE ID="+str(Id)
#    else:
#    cmd="INSERT INTO People(ID,Name,Age,Gender) Values(:ID, :Name, :Age, :Gender)", {'id': id, 'name': name}
#        cmd2=""
#       cmd3=""
        #cmd4=""
    c.execute("REPLACE INTO People(Id,Name,Age,Gen) Values(:Id, :Name, :Age, :Gen)", {'Id': Id, 'Name': Name, 'Age': Age, 'Gen': Gen})
#    conn.execute(cmd2)
#    conn.execute(cmd3)
    #conn.execute(cmd4)
    conn.commit()
    conn.close()

Id=input('Enter User Id: ')
name=input('Enter User Name: ')
age=input('Enter User Age: ')
gen=input('Enter User Gender: ')
p1 = "./dataset/train/"
p2 = str(Id)
if os.path.isdir(p1+p2):
    shutil.rmtree(p1+p2)
    os.mkdir(p1+p2)
else:
    os.mkdir(p1+p2)

p1 = "./dataset/test/"
p2 = str(Id)
if os.path.isdir(p1+p2):
    shutil.rmtree(p1+p2)
    os.mkdir(p1+p2)
else:
    os.mkdir(p1+p2)

#cr=raw_input('Enter User Records')
insertOrUpdate(Id,name,age,gen)
sampleNum=0
while(True):
    ret,img=cam.read();
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        sampleNum=sampleNum+1;
        cv2.imwrite("dataset/train/"+str(Id)+"/"+str(name)+"."+str(sampleNum)+".jpg",cv2.resize(gray[y:y+h,x:x+w],(100,100)))
        cv2.imwrite("dataset/test/"+str(Id)+"/"+str(name)+"."+str(sampleNum)+".jpg",cv2.resize(gray[y:y+h,x:x+w],(100,100)))
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.waitKey(100);
    cv2.imshow("Face",img)
    cv2.waitKey(1)
    if(sampleNum>100):
        break;
cam.release()
cv2.destroyAllWindows()

#
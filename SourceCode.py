import cvzone
import cv2
import rotatescreen

import tkinter as tk
from tkinter import messagebox, simpledialog

from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

window = tk.Tk()

cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)
id_list=[22,23,24,26,110,157,158,159,160,161,130,243]
plotY = LivePlot(640,360,[3,5],invert=False)

ratioList=[]

c=1

while(True):

            success,img = cap.read()
            img,faces = detector.findFaceMesh(img,False)
            if(faces):
                face = faces[0]
                for i in id_list:
                    cv2.circle(img,face[i],2,(255,0,255),cv2.FILLED)

                leftUp = face[159]
                leftDown = face[145]
                leftLeft = face[130]
                rightRight = face[243]
                hor,_ = detector.findDistance(leftLeft,rightRight)
                ver,_ = detector.findDistance(leftUp,leftDown)
                cv2.line(img,leftUp,leftDown,(0,200,0),3)
                cv2.line(img,leftLeft,rightRight,(0,200,0),3)

                # ver*=100
                ratio =  (((hor/ver)))
                ratioList.append(ratio)
                if(len(ratioList)>3):
                     ratioList.pop(0)

                ratioAvg=sum(ratioList)/len(ratioList)
                
                #DISTANCE

                pointLeft = face[145]
                pointRight = face[374]

                cv2.line(img, pointLeft, pointRight, (0, 200, 0), 3)
                cv2.circle(img,pointLeft,5,(255,0,255),cv2.FILLED)
                cv2.circle(img, pointRight, 5, (255, 0, 255), cv2.FILLED)

                w,_ = detector.findDistance(pointLeft,pointRight)
                W=6.3

                f=650
                d =  (W*f)/w

                screen = rotatescreen.get_primary_display()
                # window.withdraw()
                if(d<40 and ratioAvg<4.2):
                    c+=1
                    if(c>120):
                        screen.rotate_to(180)

                        # messagebox.showwarning("You are too close to the Screen !!!")
                elif(d>40 and ratioAvg<4.2):
                    c+=1
                    if(c>120):
                        screen.rotate_to(180)
                        # messagebox.showwarning("Blink your eyes !!!")
                elif(d<40):
                    screen.rotate_to(180)
                    # messagebox.showwarning("You are too close to the Screen !!!")
                else:
                    screen.rotate_to(0)
                    c = 0


                imgPlot=plotY.update(ratioAvg)
                cvzone.putTextRect(img, f'Distance: {int(d)}cm', (face[10][0] , face[10][1])#100
                           , scale=1)
                cv2.imshow("plot",imgPlot)
                cv2.imshow("image",img)


            if cv2.waitKey(1) == ord("q"):
                screen.rotate_to(0)
                window.withdraw()
                messagebox.showwarning("You are trying to quit")
                password = simpledialog.askstring("Password", "Enter your password:", show='*')

                if(password=="58529999"):
                    break
                else:
                    window.destroy()
                    window = tk.Tk()

                break

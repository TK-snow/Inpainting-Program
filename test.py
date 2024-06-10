from PyQt6 import  uic
from PyQt6.QtWidgets import QApplication, QFileDialog,QMainWindow
from PyQt6.QtGui import QPixmap, QImage,QIcon,QPainter,QPen
from PyQt6.QtCore import Qt,QPointF


import sys
from pathlib import Path
import cv2 as cv
import numpy as np
import tempfile

import controller.ui_controller as ui

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/in_painting.ui', self)
        
        self.temp_mark = tempfile.NamedTemporaryFile(suffix='.png', delete=False)

        self.hasSelect = False
        self.hasMark = False
        self.hasResult = False
        self.drawEnable = False

        self.offset = QPointF(40,150)



        self.select_image_menu.triggered.connect(self.select_image)
        self.load_mark_menu.triggered.connect(self.select_mark)
        self.save_mark_menu.triggered.connect(self.save_image)

        self.image_btn.clicked.connect(self.image_button)
        self.mark_btn.clicked.connect(self.create_mark)
        self.inpaint_ns_btn.clicked.connect(self.inpaint_ns)
        self.inpaint_fmm_btn.clicked.connect(self.inpaint_fmm)


       




        self.show()
    
    def select_image(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            r"D:/", 
            "Images (*.png *.jpg *.jpeg)"
        )
        if filename:
            path = Path(filename)
            self.image_data = ui.image_frame.setUpPixmap(self,str(path),960,600)


            thumbnial = ui.image_frame.setUpPixmap(self,str(path),130,80)
            thumbnial = QIcon(thumbnial)
            self.image_btn.setIcon(thumbnial)
            self.image_btn.setText("")
            self.image.setPixmap(self.image_data) 


            self.image_origin_path = filename
            self.hasSelect = True            
            

            original = cv.imread(str(path))
            height, width = original.shape[:2]
            img = np.zeros((height,width, 1), dtype = "uint8")
            cv.imwrite(self.temp_mark.name,img)
            self.drawEnable = False
            self.painter.end()
            
           

    def select_mark(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            r"D:/", 
            "Images (*.png *.jpg *.jpeg)"
        )
        if filename:
            path = Path(filename)
            mark = cv.imread(str(path))
            self.mark_data = ui.image_frame.setUpPixmap(self,str(path),960,600)
            thumbnial = ui.image_frame.openCVtoPixmap(self,mark,130,80)
            self.image.setPixmap(self.mark_data)
            thumbnial = QIcon(thumbnial)
            self.mark_btn.setIcon(thumbnial)
            self.mark_btn.setText("")
            self.mark_path = filename
            self.hasMark = True

            
            cv.imwrite(self.temp_mark.name,mark)

    def create_mark(self):
        mark = cv.imread(self.temp_mark.name)
        self.mark_data = ui.image_frame.openCVtoPixmap(self,mark,960,700)
        self.painter = QPainter(self.mark_data)
        self.pen = QPen(Qt.GlobalColor.white)
        self.pen.setWidth(20)
        self.painter.setPen(self.pen)
        self.image.setPixmap(self.mark_data)
        
        
        thumbnial = ui.image_frame.openCVtoPixmap(self,mark,130,80)
        thumbnial = QIcon(thumbnial)
        self.mark_btn.setIcon(thumbnial)
        self.mark_btn.setText("")
        self.mark_path = self.temp_mark.name

        
        self.hasMark = True
        self.drawEnable = True

        

        

            
    
    
    def save_mark(self):
        if not self.hasMark :
            ui.message.alert(self,message="no Mark generate yet!")
        else:
            ui.button_control.save_image(self,img_data=self.img_data)

    def image_button(self):
        if not self.hasSelect:
            filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            r"D:/", 
            "Images (*.png *.jpg *.jpeg)"
            )
            if filename:
                path = Path(filename)
                self.image_data = ui.image_frame.setUpPixmap(self,str(path),960,600)

                offsetX = self.image_data.width()/4
                offsety = 0

                offset_image = QPointF(offsetX,offsety)

                self.offset += offset_image

                thumbnial = ui.image_frame.setUpPixmap(self,str(path),130,80)
                thumbnial = QIcon(thumbnial)
                self.image_btn.setIcon(thumbnial)
                self.image_btn.setText("")
                self.image.setPixmap(self.image_data) 
                self.image_origin_path = filename
                self.hasSelect = True

   
                original = cv.imread(str(path))
                height, width = original.shape[:2]
                img = np.zeros((height,width, 1), dtype = "uint8")
                cv.imwrite(self.temp_mark.name,img)

                
        else:
            self.image.setPixmap(self.image_data)
            self.drawEnable = False
            self.painter.end()

    def mark_button(self):
        if not self.hasMark:
            filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            r"D:/", 
            "Images (*.png *.jpg *.jpeg)"
            )
            if filename:
                path = Path(filename)
                mark = cv.imread(str(path))
                self.mark_data = ui.image_frame.setUpPixmap(self,str(path),960,700)
                thumbnial = ui.image_frame.openCVtoPixmap(self,mark,130,80)
                self.image.setPixmap(self.mark_data)
                thumbnial = QIcon(thumbnial)
                self.mark_btn.setIcon(thumbnial)
                self.mark_btn.setText("")
                self.mark_path = filename
                self.hasMark = True

                
                cv.imwrite(self.temp_mark.name,mark)
        else:
            self.image.setPixmap(self.mark_data)
            self.painter.begin(self.mark_data)



    def inpaint_ns(self):
        if not self.hasSelect:
            ui.message.alert(self,message="please choose image first!")
        else :
            if not self.hasMark:
                ui.message.alert(self,message="please choose mark of image too!")
            else:
                original_image = cv.imread(self.image_origin_path)
                mark_image = cv.imread(self.temp_mark.name,0)

                height, width = original_image.shape[:2]
                dsize = (width, height)
                mark_image = cv.resize(mark_image,dsize)

                output = cv.inpaint(original_image, mark_image, 3, cv.INPAINT_NS)
                
                self.image_data = ui.image_frame.openCVtoPixmap(self,output,960,700)
                thumbnial = ui.image_frame.openCVtoPixmap(self,output,130,80)
                thumbnial = QIcon(thumbnial)
                self.image_btn.setIcon(thumbnial)
                self.image_btn.setText("")
                self.image.setPixmap(self.image_data)
                ui.message.finish(self,message="Fixing Damage image using inpainting Navier-Stoke Method finish!")
                self.hasResult = True
                self.drawEnable = False
                self.painter.end()

    def inpaint_fmm(self):
        if not self.hasSelect:
            ui.message.alert(self,message="please choose image first!")
        else :
            if not self.hasMark:
                ui.message.alert(self,message="please choose mark of image too!")
            else:
                original_image = cv.imread(self.image_origin_path)
                mark_image = cv.imread(self.temp_mark.name,0)

                height, width = original_image.shape[:2]
                dsize = (width, height)
                mark_image = cv.resize(mark_image,dsize)

                output = cv.inpaint(original_image, mark_image, 3, cv.INPAINT_TELEA)
                
                self.image_data = ui.image_frame.openCVtoPixmap(self,output,960,700)
                thumbnial = ui.image_frame.openCVtoPixmap(self,output,130,80)
                thumbnial = QIcon(thumbnial)
                self.image_btn.setIcon(thumbnial)
                self.image_btn.setText("")
                self.image.setPixmap(self.image_data)
                ui.message.finish(self,message="Fixing Damage image using inpainting Fast Matching Method finish!")
                self.hasResult = True
                self.drawEnable = False
                self.painter.end()
    
    def mouseMoveEvent(self, event):
        pos = event.globalPosition()
        
        print(pos)
        if self.drawEnable == True :
            if self.last:
                self.painter.drawLine(self.last, event.position()- self.offset )
                self.last = event.position()- self.offset
                self.image.setPixmap(self.mark_data)
    

    def mousePressEvent(self, event):
        if self.drawEnable == True :
            self.last = event.position() - self.offset
        

    def mouseReleaseEvent(self, event):
         if self.drawEnable == True :
            self.last = None
            thumbnial = ui.image_frame.setUpPixmap(self,self.mark_data,130,80)
            thumbnial = QIcon(thumbnial)
            self.mark_btn.setIcon(thumbnial)
            self.mark_btn.setText("")

            if self.temp_mark:
                with open(self.temp_mark.name, "wb") as f:
                    self.mark_data.save(self.temp_mark.name)

    def save_image(self):
        if not self.hasMark :
            ui.message.alert(self,message="no result generate yet!")
        else:
            ui.button_control.save_image(self,img_data=self.mark_data)



app = QApplication(sys.argv)
window = Ui()
app.exec()
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

import numpy as np


class button_control :
    def save_image(self,img_data):
        fileName, _ = QFileDialog.getSaveFileName(
                            self, "Save Image",r"D:/" , "Images (*.png *.jpg *.jpeg)"
                            )

        if fileName:
            with open(fileName, "wb") as f:
                img_data.save(fileName)

class message:
    def alert(self,message):
        msg = QMessageBox()
        msg.setWindowTitle("Alert!")
        msg.setText(message)
 
        x = msg.exec()

    def finish(self,message):
        msg = QMessageBox()
        msg.setWindowTitle("Operation Finsih!")
        msg.setText(message)
 
        x = msg.exec()

class image_frame :
    img_path = ""
    select = False


    def openCVtoPixmap(self,output,maxW,maxH):
        height, width = output.shape[:2]
        bytesPerLine = 3 * width
        output2 = np.require(output, np.uint8, 'C')
        output = QImage(output2, width, height,bytesPerLine,QImage.Format.Format_RGB888).rgbSwapped()
        img_data = QPixmap(QPixmap.fromImage(output))
        w = img_data.width()
        h = img_data.height()

        img_data = img_data.scaled(maxW,maxH,Qt.AspectRatioMode.KeepAspectRatio)

        

        return img_data
     
    def setUpPixmap(self,path,maxW,maxH):
            img_data = QPixmap(path)
            w = img_data.width()
            h = img_data.height()

            img_data = img_data.scaled(maxW,maxH,Qt.AspectRatioMode.KeepAspectRatio)

            """
            if not (w < maxW):
                if(w > h):
                    img_data = img_data.scaledToWidth(maxW)
                else:
                    img_data = img_data.scaledToHeight(maxH)
            elif not (h < maxH):
                if(w > h):
                    img_data = img_data.scaledToWidth(maxW)
                else:
                    img_data = img_data.scaledToHeight(maxH)
            """

            return img_data
    
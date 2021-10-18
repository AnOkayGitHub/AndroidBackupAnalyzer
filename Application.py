import math

from PyQt5.uic import loadUi
import sms_backup_reader as sbr
import os
from PyQt5.QtWidgets import *
from fpdf import FPDF
from platform import system


# Class to handle all GUI related code
class Application(QMainWindow):

    # Class attributes for file handling and button state control
    path = ""
    desktop = ""
    out_path = ""
    out_name = "output"
    tb_states = [1, 0, 0]
    tbs = []
    out_type = ".txt"
    sys = system()

    # Constructor
    def __init__(self):
        super(Application, self).__init__()

        # Load ui file from PyQT Designer
        loadUi("WindowMain.ui", self)

        # Try to find a desktop location (Windows only)
        try:
            self.desktop = os.path.join(os.path.join(os.environ["HOMEPATH"]), "OneDrive\Desktop")
        except Exception as e:
            self.desktop = "/"

        # Update initial values and connect functionality to buttons
        self.validate()
        self.tbs = [self.tBody, self.tDate, self.tName]
        self.out_path = self.desktop
        self.outputFilePath.setText(self.out_path)
        self.analyzeButton.setEnabled(False)
        self.set_status("")
        self.init_buttons()

    # Determine if we can analyze the file based on the given information
    def validate(self):
        self.analyzeButton.setEnabled(1 in self.tb_states and self.path != "" and self.out_path != "" and self.out_name != "")

    # Assign functions to button clicks.
    def init_buttons(self):
        self.browseButton.clicked.connect(self.browse_files)
        self.browseButton_2.clicked.connect(self.browse_location)
        self.analyzeButton.clicked.connect(self.analyze)
        self.tBody.clicked.connect(self.toggle_button)
        self.tDate.clicked.connect(self.toggle_button)
        self.tName.clicked.connect(self.toggle_button)
        self.outTypeButton.clicked.connect(self.toggle_out_type)

    # Get output file type (.pdf or .txt)
    def get_out_type(self):
        return self.outTypeButton.text()

    # Set the output file type text on GUI
    def set_out_type(self):
        self.outTypeButton.setText(self.out_type)

    # Toggle the output type between TXT and PDF
    def toggle_out_type(self):
        self.out_type = ".txt" if self.out_type == ".pdf" else ".pdf"

        if self.out_type == ".pdf":
            self.outTypeButton.setStyleSheet("""
                        QPushButton#outTypeButton {
                            font: 8pt "Gadugi";
                            background-color: rgba(255, 142, 0, 0.1);
                            border: 1px solid rgb(255, 142, 0);
                            border-radius: 5px;
                            color: white;
                            text-align: center;
                            padding-bottom:1%;
                        }
                        
                        QPushButton#outTypeButton:hover {
                            font: 8pt "Gadugi";
                            background-color: rgba(255, 142, 0, 0.2);
                            border: 1px solid rgb(255, 142, 0);
                            border-radius: 5px;
                            color: white;
                            text-align: center;
                            padding-bottom:1%;
                        }
                        """)
        else:
            self.outTypeButton.setStyleSheet("""
                        QPushButton#outTypeButton {
                            font: 8pt "Gadugi";
                            background-color: rgba(0, 200, 200, 0.1);
                            border: 1px solid rgb(0, 200, 200);
                            border-radius: 5px;
                            color: white;
                            text-align: center;
                            padding-bottom:1%;
                        }
                        
                        QPushButton#outTypeButton:hover {
                            font: 8pt "Gadugi";
                            background-color: rgba(0, 200, 200, 0.2);
                            border: 1px solid rgb(0, 200, 200);
                            border-radius: 5px;
                            color: white;
                            text-align: center;
                            padding-bottom:1%;
                        }

                        """)

        self.set_out_type()

    # Update the status widget and provide whether or not the message is an error (becomes red)
    def set_status(self, status, error=False):
        if error:
            self.status.setStyleSheet("""
                font: 8pt "Gadugi";
                color: rgb(255, 142, 142);
                """
            )
        else:
            self.status.setStyleSheet("""
                font: 8pt "Gadugi";
                color: rgb(142, 255, 142);
                """
                          )
        self.status.setText(status)

    # Set the output file name if possible, if not revert to default
    def set_out_name(self):
        text = self.outputFileName.text()
        if text != "":
            self.out_name = self.outputFileName.text()
        else:
            self.outputFileName.setText("output") + self.get_out_type()

    # Set the output path if possible, if not revert to desktop.
    def set_out_path(self):
        text = self.outputFilePath.text()
        if text != "":
            self.out_path = text
        else:
            self.outputFileName.setText(self.desktop)

    # File browser for choosing an XML file
    def browse_files(self):
        try:
            file_name = QFileDialog.getOpenFileName(self, "Choose File", self.desktop, "XML Files (*.xml)")
            self.update_path(file_name[0])

            with open(self.path, "r") as f:
                self.set_status("")
        except Exception as e:
            pass
        self.validate()

    # File browser for choosing an output location
    def browse_location(self):
        try:
            out = QFileDialog.getExistingDirectory(self, "Choose Location", self.desktop)

            if out != "":
                self.outputFilePath.setText(out)
            else:
                self.outputFilePath.setText(self.desktop)
        except Exception as e:
            pass

        self.validate()

    # Analyze file and generate output report
    def analyze(self):
        try:
            self.set_out_path()
            self.set_out_name()
            reader = sbr.BackupReader(self.path)
            data = reader.get_texts_formatted(self.tb_states)
            keywords = self.keywordInput.text().split(",")
            cleaned_data = ""

            keyword_size = len(keywords)
            if keywords[0] == "" and keyword_size == 1:
                keyword_size = 0
            else:
                for d in data.split("\n"):
                    for keyword in keywords:
                        kw = keyword.strip()
                        if kw in d and d not in cleaned_data:
                            cleaned_data += d + "\n"

            out = ""
            if self.sys == "Windows":
                out = "\\" + self.out_name + ".txt"
            else:
                out = "/" + self.out_name + ".txt"

            if cleaned_data == "" and keyword_size > 0:
                self.set_status("No keywords found in backup.", True)
            elif cleaned_data != "" and keyword_size > 0:
                output = open(out, "w+", encoding="utf-8")
                output.write(cleaned_data)
                output.close()
                self.set_status(format("File %s created at location:\n%s" % (self.out_name + self.get_out_type(), self.out_path)))
            elif keyword_size == 0:
                output = open(out, "w+", encoding="utf-8")
                output.write(data)
                output.close()
                self.set_status(format("File %s created at location:\n%s" % (self.out_name + self.get_out_type(), self.out_path)))
            if self.get_out_type() == ".pdf":
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=8)
                f_name = out

                f = open(f_name, "r")
                size = 140
                for x in f:
                    print(x)
                    y = x.split(" ")
                    cell = ""
                    if len(x) > size:
                        for word in y:
                            if len(cell + word) <= size:
                                cell += word + " "

                            else:
                                pdf.cell(size, 5, txt=cell, ln=1, align="L")
                                cell = word + " "
                            print(cell)
                    if cell != "":
                        pdf.cell(size, 5, txt=cell, ln=1, align="L")

                    else:
                        pdf.cell(size, 5, txt=x, ln=1, align="L")

                pdf.output(self.out_path + "\\" + self.out_name + ".pdf")
                f.close()
                os.remove(f_name)

            self.validate()

        except Exception as e:
            self.set_status("Invalid file or directory.", True)
            self.reset()
            print(e)
            pass

    # Reset app to original state
    def reset(self):
        self.update_path("")
        self.update_location(self.desktop)
        self.validate()

    # Update the output location
    def update_location(self, new_location):
        self.out_path = new_location
        self.outputFilePath.setText(self.out_path)

    # Update the file path
    def update_path(self, new_path):
        self.path = new_path
        self.fileName.setText(self.path)

    # Handle toggle buttons for including data
    def toggle_button(self):
        tb = self.sender()
        ind = self.tbs.index(tb)
        self.tb_states[ind] = (1 if self.tb_states[ind] == 0 else 0)
        self.validate()

        if self.tb_states[ind] == 1:
            self.tbs[ind].setStyleSheet(format("""
                QPushButton#%s {
                    font: 10pt "Gadugi";
                    color: rgb(255, 255, 255);
                    background-color: rgba(142, 255, 142, 0.2);
                    border: 1px solid  rgb(142, 255, 142);
                    border-radius: 5px;
                    color:rgb(142, 255, 142);
                }
                
                QPushButton#%s:hover {
                    font: 10pt "Gadugi";
                    color: rgb(255, 255, 255);
                    background-color: rgba(142, 255, 142, 0.4);
                    border: 1px solid  rgb(142, 255, 142);
                    border-radius: 5px;
                    color:rgb(142, 255, 142);
                }
                """ % (self.tbs[ind].objectName(), self.tbs[ind].objectName())))
        else:
            self.tbs[ind].setStyleSheet(format("""
                QPushButton#%s {
                    font: 10pt "Gadugi";
                    background-color: rgba(255, 142, 142, 0.2);
                    border: 1px solid rgb(255, 142, 142);
                    border-radius: 5px;
                    color: rgb(255, 142, 142);
                }
                
                QPushButton#%s:hover {
                    font: 10pt "Gadugi";
                    background-color: rgba(255, 142, 142, 0.4);
                    border: 1px solid rgb(255, 142, 142);
                    border-radius: 5px;
                    color: rgb(255, 142, 142);
                }
                """ % (self.tbs[ind].objectName(), self.tbs[ind].objectName())))

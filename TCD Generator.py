import tkinter as tk
from tkinter import ttk, filedialog, messagebox,PhotoImage
from PIL import Image, ImageTk
import shutil
 
class TCDGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("WSS TCD Generator")
        self.master.state('zoomed')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.left_frame = ttk.Frame(self.master)
        self.left_frame.grid(row=0, column=0)
        self.right_frame = ttk.Frame(self.master)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.SOI = {
            'Direct': {
                 'Multipole Encoder': {
                     'Axial Side': {
                         'KMI7XXP': ['s', 'i', 'v'],
                         'KMI7XXE/F': ['s', 'i', 'v']
                     },
                     'Axial Bottom': {
                         'KMI7XXP': ['s', 'i', 'v'],
                         'KMI7XXE/F': ['s', 'i', 'v']
                     },
                     'Radial Side': {
                         'KMI7XXP': ['s', 'i', 'v'],
                         'KMI7XXE/F': ['s', 'i', 'v']
                     },
                     'Radial Bottom': {
                         'KMI7XXP': ['s', 'i', 'v'],
                         'KMI7XXE/F': ['s', 'i', 'v']
                     }
                 },
                 'Steel Wheel': {
                     'Axial Side': {
                         'KMI7XXP': ['s', 'i', 'v'],
                         'KMI7XXE/F': ['s', 'i', 'v']
                     },
                     'Axial Bottom': {
                         'KMI7XXP': ['s', 'i', 'v'],
                         'KMI7XXE/F': ['s', 'i', 'v']
                     },
                     'Radial Side': {
                         'KMI7XXP': ['s', 'i', 'v'],
                         'KMI7XXE/F': ['s', 'i', 'v']
                     },
                     'Radial Bottom': {
                         'KMI7XXP': ['s', 'i', 'v'],
                         'KMI7XXE/F': ['s', 'i', 'v']
                     }
                 }
             },
            'Harness': {
                'Multipole Encoder': {
                    'Axial Side': {
                        'KMI7XXP': ['s', 'i', 'v'],
                        'KMI7XXE/F': ['s', 'i', 'v']
                    },
                    'Axial Bottom': {
                        'KMI7XXP': ['s', 'i', 'v'],
                        'KMI7XXE/F': ['s', 'i', 'v']
                    },
                    'Radial Side': {
                        'KMI7XXP': ['s', 'i', 'v'],
                        'KMI7XXE/F': ['s', 'i', 'v']
                    },
                    'Radial Bottom': {
                        'KMI7XXP': ['s', 'i', 'v'],
                        'KMI7XXE/F': ['s', 'i', 'v']
                    }
                },
                'Steel Wheel': {
                    'Radial Side': {
                        'KMI7XXP': ['s', 'i', 'v'],
                        'KMI7XXE/F': ['s', 'i', 'v']
                    },
                    'Axial Bottom': {
                        'KMI7XXP': ['s', 'i', 'v'],
                        'KMI7XXE/F': ['s', 'i', 'v']
                    },
                    'Radial Bottom': {
                        'KMI7XXP': ['s', 'i', 'v'],
                        'KMI7XXE/F': ['s', 'i', 'v']
                    }
                }
            }
        }
        self.selections = {}
        self.buttons = {}
        self.create_SOI()
        self.image_label = ttk.Label(self.right_frame)
        self.image_label.grid(row=4, column=1,sticky="nsew")
        self.current_image = None
     
    def create_SOI(self):
        style = ttk.Style()
        style.configure('TButton', font=('Bosch Sans Global Black', 35), foreground='Black', background='light gray',relief='raised')
        for i, SOI in enumerate(self.SOI.keys(), start=1):
            button = ttk.Button(self.left_frame, text=SOI, command=lambda s=SOI: self.show_Encoder(s))
            button.grid(row=i, column=0, sticky="nsew")
            self.buttons[SOI] = button
 
    def show_Encoder(self, SOI):
        self.selections['SOI'] = SOI
        self.clear_buttons()
        for i, Encoder in enumerate(self.SOI[SOI].keys(), start=1):
            button = ttk.Button(self.left_frame, text=Encoder, command=lambda e=Encoder: self.show_RP(SOI, e))
            button.grid(row=i, column=1, sticky="nsew")
            self.buttons[Encoder] = button
 
    def show_RP(self, SOI, Encoder):
        self.selections['Encoder'] = Encoder
        self.clear_buttons()
        for i, RP in enumerate(self.SOI[SOI][Encoder], start=1):
            button = ttk.Button(self.left_frame, text=RP, command=lambda r=RP: self.show_ASIC(SOI, Encoder, r))
            button.grid(row=i, column=2, sticky="nsew")
            self.buttons[RP] = button
 
    def show_ASIC(self, SOI, Encoder, RP):
        self.selections['RP'] = RP
        self.clear_buttons()
        for i, ASIC in enumerate(self.SOI[SOI][Encoder][RP], start=1):
            button = ttk.Button(self.left_frame, text=ASIC, command=lambda a=ASIC: self.show_Variants(SOI, Encoder, RP, a))
            button.grid(row=i, column=3, sticky="nsew")
            self.buttons[ASIC] = button
 
    def show_Variants(self, SOI, Encoder, RP, ASIC):
        self.selections['ASIC'] = ASIC
        self.clear_buttons()
        for i, Variants in enumerate(self.SOI[SOI][Encoder][RP][ASIC], start=1):
            button = ttk.Button(self.left_frame, text=Variants, command=lambda v=Variants: self.save_document(v, SOI, Encoder, RP, ASIC))
            button.grid(row=i, column=4, sticky="nsew")
            self.buttons[Variants] = button

    def load_image(self, file_path):
        image = Image.open(file_path)
        width, height = image.size
        max_width = 990
        max_height = 660
        if width > max_width or height > max_height:
            ratio = min(max_width/width, max_height/height)
            new_size = (int(width*ratio), int(height*ratio))
            image = image.resize(new_size)
        self.current_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.current_image)
        
    def save_document(self, Variants, SOI, Encoder, RP, ASIC):
        self.selections['Variants'] = Variants
        source_path = self.get_source_path(SOI, Encoder, RP, ASIC, Variants)
        if source_path:
         file_path = filedialog.asksaveasfilename(defaultextension=".docx")
         if file_path:
             shutil.copyfile(source_path, file_path)
             self.master.destroy()
        else:
         messagebox.showerror("Error", "Document not available for the selected options.")
         self.master.destroy()
 
    def get_source_path(self, SOI, Encoder, RP, ASIC, Variants):
        if SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Axial Bottom' and ASIC == 'KMI7XXE/F' and Variants == 'i':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-AxailBottom-E-i.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Axial Bottom' and ASIC == 'KMI7XXE/F' and Variants == 's':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-AxailBottom-E-s.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Axial Bottom' and ASIC == 'KMI7XXE/F' and Variants == 'v':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-AxailBottom-E-v.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Axial Bottom' and ASIC == 'KMI7XXP' and Variants == 'i':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-AxailBottom-P-i.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Axial Bottom' and ASIC == 'KMI7XXP' and Variants == 's':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-AxailBottom-P-s.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Axial Bottom' and ASIC == 'KMI7XXP' and Variants == 'v':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-AxailBottom-P-v.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Axial Side' and ASIC == 'KMI7XXE/F' and Variants == 'i':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-AxailSide-E-i.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Axial Side' and ASIC == 'KMI7XXE/F' and Variants == 's':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-AxailSide-E-s.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Axial Side' and ASIC == 'KMI7XXE/F' and Variants == 'v':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-AxailSide-E-v.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Axial Side' and ASIC == 'KMI7XXP' and Variants == 'i':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-AxailSide-P-i.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Axial Side' and ASIC == 'KMI7XXP' and Variants == 's':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-AxailSide-P-s.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Axial Side' and ASIC == 'KMI7XXP' and Variants == 'v':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-AxailSide-P-v.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Radial Bottom' and ASIC == 'KMI7XXE/F' and Variants == 'i':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-RadialBottom-E-i.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Radial Bottom' and ASIC == 'KMI7XXE/F' and Variants == 's':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-RadialBottom-E-s.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Radial Bottom' and ASIC == 'KMI7XXE/F' and Variants == 'v':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-RadialBottom-E-v.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Radial Bottom' and ASIC == 'KMI7XXP' and Variants == 'i':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-RadialBottom-P-i.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Radial Bottom' and ASIC == 'KMI7XXP' and Variants == 's':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-RadialBottom-P-s.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Radial Bottom' and ASIC == 'KMI7XXP' and Variants == 'v':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-RadialBottom-P-v.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Radial Side' and ASIC == 'KMI7XXE/F' and Variants == 'i':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-RadialSide-E-i.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Radial Side' and ASIC == 'KMI7XXE/F' and Variants == 's':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-RadialSide-E-s.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Radial Side' and ASIC == 'KMI7XXE/F' and Variants == 'v':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-RadialSide-E-v.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Radial Side' and ASIC == 'KMI7XXP' and Variants == 'i':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-RadialSide-P-i.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Radial Side' and ASIC == 'KMI7XXP' and Variants == 's':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-RadialSide-P-s.docx"
        elif SOI == 'Harness' and Encoder == 'Multipole Encoder' and RP == 'Radial Side' and ASIC == 'KMI7XXP' and Variants == 'v':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-Multipole-RadialSide-P-v.docx"
        elif SOI == 'Harness' and Encoder == 'Steel Wheel' and RP == 'Axial Bottom' and ASIC == 'KMI7XXE/F' and Variants == 'i':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-SteelWheel-AxialBottom-E-i.docx"
        elif SOI == 'Harness' and Encoder == 'Steel Wheel' and RP == 'Axial Bottom' and ASIC == 'KMI7XXE/F' and Variants == 's':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-SteelWheel-AxialBottom-E-s.docx"
        elif SOI == 'Harness' and Encoder == 'Steel Wheel' and RP == 'Axial Bottom' and ASIC == 'KMI7XXE/F' and Variants == 'v':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-SteelWheel-AxialBottom-E-v.docx"
        elif SOI == 'Harness' and Encoder == 'Steel Wheel' and RP == 'Axial Bottom' and ASIC == 'KMI7XXP' and Variants == 'i':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-SteelWheel-AxialBottom-P-i.docx"
        elif SOI == 'Harness' and Encoder == 'Steel Wheel' and RP == 'Axial Bottom' and ASIC == 'KMI7XXP' and Variants == 's':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-SteelWheel-AxialBottom-P-s.docx"
        elif SOI == 'Harness' and Encoder == 'Steel Wheel' and RP == 'Axial Bottom' and ASIC == 'KMI7XXP' and Variants == 'v':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-SteelWheel-AxialBottom-P-v.docx"
        elif SOI == 'Harness' and Encoder == 'Steel Wheel' and RP == 'Radial Bottom' and ASIC == 'KMI7XXE/F' and Variants == 'i':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-SteelWheel-RadialBottom-E-i.docx"
        elif SOI == 'Harness' and Encoder == 'Steel Wheel' and RP == 'Radial Bottom' and ASIC == 'KMI7XXE/F' and Variants == 's':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-SteelWheel-RadialBottom-E-s.docx"
        elif SOI == 'Harness' and Encoder == 'Steel Wheel' and RP == 'Radial Bottom' and ASIC == 'KMI7XXE/F' and Variants == 'v':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-SteelWheel-RadialBottom-E-v.docx"
        elif SOI == 'Harness' and Encoder == 'Steel Wheel' and RP == 'Radial Bottom' and ASIC == 'KMI7XXP' and Variants == 'i':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-SteelWheel-RadialBottom-P-i.docx"
        elif SOI == 'Harness' and Encoder == 'Steel Wheel' and RP == 'Radial Bottom' and ASIC == 'KMI7XXP' and Variants == 's':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-SteelWheel-RadialBottom-P-s.docx"
        elif SOI == 'Harness' and Encoder == 'Steel Wheel' and RP == 'Radial Bottom' and ASIC == 'KMI7XXP' and Variants == 'v':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-SteelWheel-RadialBottom-P-v.docx"
        elif SOI == 'Harness' and Encoder == 'Steel Wheel' and RP == 'Radial Side' and ASIC == 'KMI7XXE/F' and Variants == 'i':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-SteelWheel-RadialSide-E-i.docx"
        elif SOI == 'Harness' and Encoder == 'Steel Wheel' and RP == 'Radial Side' and ASIC == 'KMI7XXE/F' and Variants == 's':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-SteelWheel-RadialSide-E-s.docx"
        elif SOI == 'Harness' and Encoder == 'Steel Wheel' and RP == 'Radial Side' and ASIC == 'KMI7XXE/F' and Variants == 'v':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-SteelWheel-RadialSide-E-v.docx"
        elif SOI == 'Harness' and Encoder == 'Steel Wheel' and RP == 'Radial Side' and ASIC == 'KMI7XXP' and Variants == 'i':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-SteelWheel-RadialSide-P-i.docx"
        elif SOI == 'Harness' and Encoder == 'Steel Wheel' and RP == 'Radial Side' and ASIC == 'KMI7XXP' and Variants == 's':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-SteelWheel-RadialSide-P-s.docx"
        elif SOI == 'Harness' and Encoder == 'Steel Wheel' and RP == 'Radial Side' and ASIC == 'KMI7XXP' and Variants == 'v':
            return r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Project Templates\Harness-SteelWheel-RadialSide-P-v.docx"
        
        else:
            return ""
 
    def clear_buttons(self):
        for button in self.buttons.values():
            button.grid_forget()
        self.buttons.clear()
 
    def access_button(self, button_name):
        if button_name in self.buttons:
            self.buttons[button_name].invoke()
        else:
            print(f"Button '{button_name}' not found.")
 
def main():
    root = tk.Tk()
    app = TCDGeneratorApp(root)
    app.load_image(r"P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Icons and Photos\Bosch TCD Generator.png")
    root.iconbitmap(r'P:\Engineering\ChkP\ActiveSafety\Projects\12_Sensors\Files_Parth\Project - TCD Generator\Icons and Photos\bosch.ico')
    root.configure(background="light gray")
    root.mainloop()
 
if __name__ == "__main__":
    main()
import customtkinter
import os
from PIL import Image, ImageDraw, ImageFont, ImageWin
import mysql.connector
import random
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import messagebox
import win32print
import win32ui
import qrcode


mydb = mysql.connector.connect(
    host='127.0.0.1',
    password='Aspire2023',
    user='root',
    database="iksuda"
)


class LoginApp(customtkinter.CTk):
    width = 900
    height = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("CustomTkinter example_background_image.py")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/test_images/test_background.jpg"),
                                               size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        login_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(login_image_path, "iksuda_logo.png")), size=(300, 150))


        self.login_logo = customtkinter.CTkLabel(self.login_frame, text="", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.login_logo.grid(row=0, column=0, padx=20, pady=20)

        self.login_label = customtkinter.CTkLabel(self.login_frame, text="Inventory",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(150, 15))

        self.username_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login_event, width=200)
        self.login_button.grid(row=3, column=0, padx=30, pady=(15, 15))

        self.bind("<Return>", lambda event: self.login_event())

    def login_event(self):
        # Check login credentials
        if self.username_entry.get() == "1" and self.password_entry.get() == "1":
            # Successful login
            self.destroy()  # Close the login app
            main_app = MainApp()  # Create an instance of the main app
            main_app.title("Inventory Iksuda")  # Set the title for the main app
            main_app.mainloop()  # Run the main app
        else:
            # Invalid login, show an error message or handle as needed
            pass


class MainApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.radiobutton_frame = None
        self.scrollable_frame_switches = []
        self.asset_numbers = []
        

        self.title("Inventory Iksuda")
        self.geometry("1650x800")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Iksuda.png")), size=(26, 26))

        self.consumables_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "consumables_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "consumables_light.png")), size=(20, 20))
        self.solutions_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "conical_flask_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "conical_flask_light.png")), size=(20, 20))
        self.search_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "magnifying_glass_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "magnifying_glass_light.png")), size=(20, 20))
        self.antibody_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "antibody_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "antibody_light.png")), size=(20, 20))
        self.adc_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "ADC_dark.png")),
                                                    dark_image=Image.open(os.path.join(image_path, "ADC_light.png")), size=(20, 20))


        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=" Iksuda Inventory", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.search_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Search",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.search_image, anchor="w", command=self.Search_button_event)
        self.search_button.grid(row=1, column=0, sticky="ew")        

        self.consumables_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Consumables",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.consumables_image, anchor="w", command=self.Consumables_button_event)
        self.consumables_button.grid(row=2, column=0, sticky="ew")

        self.solutions_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Solutions",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.solutions_image, anchor="w", command=self.Solutions_button_event)
        self.solutions_button.grid(row=3, column=0, sticky="ew")

        self.antibody_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Antibody",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.antibody_image, anchor="w", command=self.Antibody_button_event)
        self.antibody_button.grid(row=4, column=0, sticky="ew")

        self.adc_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="ADC",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.adc_image, anchor="w", command=self.adc_button_event)
        self.adc_button.grid(row=5, column=0, sticky="ew")


        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create search frame------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.search_frame = customtkinter.CTkTabview(self, width=1400, height=400)
        self.search_frame.grid(row=0, column=1, padx=(20, 20), pady=(0, 0), sticky="nsew")
        self.search_frame.add("Search by Asset Number")
        self.search_frame.add("Search Consumables")
        self.search_frame.add("Search Toxins")
        self.search_frame.add("Search Antibodies")
        self.search_frame.add("Search ADC")
        self.search_frame.tab("Search by Asset Number").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.search_frame.tab("Search Consumables").grid_columnconfigure(0, weight=1)
        self.search_frame.tab("Search Toxins").grid_columnconfigure(0, weight=1)
        self.search_frame.tab("Search Antibodies").grid_columnconfigure(0, weight=1)       
        self.search_frame.tab("Search ADC").grid_columnconfigure(0, weight=1)

        self.search_title = customtkinter.CTkLabel(self.search_frame.tab("Search by Asset Number"),text="Retrieve Asset number Information",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.search_title.grid(row=0, column=0, padx=20, pady=(20,5))                                                                   
        self.search_asset = customtkinter.CTkEntry(self.search_frame.tab("Search by Asset Number"), placeholder_text="Search By Asset Number", width=160)
        self.search_asset.grid(row=1, column=0, padx=20, pady=(20, 0))
        self.search_Submit = customtkinter.CTkButton(self.search_frame.tab("Search by Asset Number"), text="Search Asset Number", command = self.retrieve_data_by_asset_number)
        self.search_Submit.grid(row=2, column=0, padx=0, pady=(10, 0))


        #create a search consumables slide bar frame----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        self.consumables_search_title = customtkinter.CTkLabel(self.search_frame.tab("Search Consumables"),text="Search consumables by name",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.consumables_search_title.grid(row=0, column=0, padx=20, pady=(20,5))
        self.search_consumables_name_input = customtkinter.CTkEntry(self.search_frame.tab("Search Consumables"), placeholder_text="Insert Consumable Name", width=160)
        self.search_consumables_name_input.grid(row=1, column=0, padx=20, pady=(20, 0))
        self.search_consumables_submit = customtkinter.CTkButton(self.search_frame.tab("Search Consumables"), text="Search", command=self.search_consumables, width=160)
        self.search_consumables_submit.grid(row=2, column=0, padx=1, pady=(20, 0))
        self.search_slide_consumables_results = customtkinter.CTkScrollableFrame(self.search_frame.tab("Search Consumables"),width=1300, height=400)
        self.search_slide_consumables_results.grid(row=3, column=0, padx=20, pady=(10,0))

        #create a search  solutions slide bar frame----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        self.solutions_search_title = customtkinter.CTkLabel(self.search_frame.tab("Search Toxins"),text="Search solutions by name",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.solutions_search_title.grid(row=0, column=0, padx=20, pady=(20,5))
        self.search_solutions_name_input = customtkinter.CTkEntry(self.search_frame.tab("Search Toxins"), placeholder_text="Insert Solution Name", width=160)
        self.search_solutions_name_input.grid(row=1, column=0, padx=20, pady=(20, 0))
        self.search_solutions_submit = customtkinter.CTkButton(self.search_frame.tab("Search Toxins"), text="Search", command=self.search_solutions, width=160)
        self.search_solutions_submit.grid(row=2, column=0, padx=1, pady=(20, 0))
        self.search_slide_solutions_results = customtkinter.CTkScrollableFrame(self.search_frame.tab("Search Toxins"),width=1300, height=400)
        self.search_slide_solutions_results.grid(row=3, column=0, padx=20, pady=(10,0))
  
  
        #create a search antibodies slide bar frame----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        self.antibodies_search_title = customtkinter.CTkLabel(self.search_frame.tab("Search Antibodies"),text="Search antibodies by name",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.antibodies_search_title.grid(row=0, column=0, padx=20, pady=(20,5))
        self.search_antibodies_name_input = customtkinter.CTkEntry(self.search_frame.tab("Search Antibodies"), placeholder_text="Insert antibodies Name", width=160)
        self.search_antibodies_name_input.grid(row=1, column=0, padx=20, pady=(20, 0))
        self.search_antibodies_submit = customtkinter.CTkButton(self.search_frame.tab("Search Antibodies"), text="Search", command=self.search_antibodies, width=160)
        self.search_antibodies_submit.grid(row=2, column=0, padx=1, pady=(20, 0))
        self.search_slide_antibodies_results = customtkinter.CTkScrollableFrame(self.search_frame.tab("Search Antibodies"),width=1300, height=400)
        self.search_slide_antibodies_results.grid(row=3, column=0, padx=20, pady=(10,0))

        #create a search adc slide bar frame----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        self.adc_search_title = customtkinter.CTkLabel(self.search_frame.tab("Search ADC"),text="Search ADC by name",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.adc_search_title.grid(row=0, column=0, padx=20, pady=(20,5))
        self.search_adc_input = customtkinter.CTkEntry(self.search_frame.tab("Search ADC"), placeholder_text="Insert ADC Name", width=160)
        self.search_adc_input.grid(row=1, column=0, padx=20, pady=(20, 0))
        self.search_adc_submit = customtkinter.CTkButton(self.search_frame.tab("Search ADC"), text="Search", command=self.search_adc, width=160)
        self.search_adc_submit.grid(row=2, column=0, padx=1, pady=(20, 0))
        self.search_slide_adc_results = customtkinter.CTkScrollableFrame(self.search_frame.tab("Search ADC"),width=1300, height=400)
        self.search_slide_adc_results.grid(row=3, column=0, padx=20, pady=(10,0))

        # Bind the "Enter" key to trigger the respective search functions
        self.search_asset.bind("<Return>", lambda event: self.retrieve_data_by_asset_number())
        self.search_consumables_name_input.bind("<Return>", lambda event: self.search_consumables())
        self.search_solutions_name_input.bind("<Return>", lambda event: self.search_solutions())
        self.search_antibodies_name_input.bind("<Return>", lambda event: self.search_antibodies())
        self.search_adc_input.bind("<Return>", lambda event: self.search_adc())


        #create checkout frame----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.checkout_frame = customtkinter.CTkFrame(self, width=1000)
        self.checkout_frame.grid_columnconfigure(0, weight=1)

        self.checkout_title = customtkinter.CTkLabel(self.checkout_frame, text="Checkout",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.checkout_title.grid(row=0, column=0, padx=20, pady=1)
        self.checkout_asset_number = customtkinter.CTkEntry(self.checkout_frame, placeholder_text="Asset Number")
        self.checkout_asset_number.grid(row=1, column=0, padx=20, pady=1)
        self.checkout_amount = customtkinter.CTkEntry(self.checkout_frame, placeholder_text="Amount")
        self.checkout_amount.grid(row=2, column=0, padx=20, pady=1)
        self.checkout_location = customtkinter.CTkEntry(self.checkout_frame, placeholder_text="Location")
        self.checkout_location.grid(row=3, column=0, padx=20, pady=1)
        self.checkout_item_button = customtkinter.CTkButton(self.checkout_frame, text="Checkout")
        self.checkout_item_button.grid(row=4, column=0, padx=20,pady=(10, 0))


        # create Consumables frame----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.consumables_tab = customtkinter.CTkTabview(self, width=1000)
        self.consumables_tab.grid(row=0, column=1, padx=(20, 20), pady=(0, 0), sticky="nsew")
        self.consumables_tab.add("Check-In")
        self.consumables_tab.add("Check-Out")
        self.consumables_tab.add("Location Change")
        self.consumables_tab.tab("Check-In").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.consumables_tab.tab("Check-Out").grid_columnconfigure(0, weight=1)
        self.consumables_tab.tab("Location Change").grid_columnconfigure(0, weight=1)


        self.consumables_checkin_title = customtkinter.CTkLabel(self.consumables_tab.tab("Check-In"), text="Consumables Check-In",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.consumables_checkin_title.grid(row=1, column=0, padx=20, pady=(20,5))
        self.consumables_checkin_frame_Consumable_Name = customtkinter.CTkEntry(self.consumables_tab.tab("Check-In"), placeholder_text="Name")
        self.consumables_checkin_frame_Consumable_Name.grid(row=2, column=0, padx=20, pady=(20, 0))
        self.consumables_checkin_frame_Consumable_Vendor = customtkinter.CTkEntry(self.consumables_tab.tab("Check-In"),placeholder_text="Vendor")
        self.consumables_checkin_frame_Consumable_Vendor.grid(row=3, column=0, padx=20, pady=1)
        self.consumables_checkin_frame_Consumable_Catalogue = customtkinter.CTkEntry(self.consumables_tab.tab("Check-In"), placeholder_text="Catalogue Number")
        self.consumables_checkin_frame_Consumable_Catalogue.grid(row=4, column=0, padx=20, pady=1)
        self.consumables_checkin_frame_Consumable_Lot = customtkinter.CTkEntry(self.consumables_tab.tab("Check-In"), placeholder_text="Lot Number")
        self.consumables_checkin_frame_Consumable_Lot.grid(row=5, column=0, padx=20, pady=1)
        self.consumables_checkin_frame_consumable_Prep_Date = DateEntry(self.consumables_tab.tab("Check-In"), date_pattern="yyyy/mm/dd", width=20)
        self.consumables_checkin_frame_consumable_Prep_Date.grid(row=6, column=0, padx=20, pady=1)
        self.consumables_checkin_frame_Consumable_Exp_Date = DateEntry(self.consumables_tab.tab("Check-In"), date_pattern="yyyy/mm/dd", width=20)
        self.consumables_checkin_frame_Consumable_Exp_Date.grid(row=7, column=0, padx=20, pady=1)
        self.consumables_checkin_frame_Consumable_location = customtkinter.CTkEntry(self.consumables_tab.tab("Check-In"), placeholder_text="Location")
        self.consumables_checkin_frame_Consumable_location.grid(row=8, column=0, padx=20, pady=1)
        self.consumables_checkin_frame_Insert_Amount = customtkinter.CTkEntry(self.consumables_tab.tab("Check-In"), placeholder_text="Insert Amount")
        self.consumables_checkin_frame_Insert_Amount.grid(row=9, column=0, padx=20, pady=1)
        self.consumables_checkin_frame_Consumable_Submit = customtkinter.CTkButton(self.consumables_tab.tab("Check-In"), text="Submit", command=self.insert_consumable_data)
        self.consumables_checkin_frame_Consumable_Submit.grid(row=10, column=0, padx=20, pady=(10, 0))
        self.consumables_checkin_frame_Consumable_Print = customtkinter.CTkButton(self.consumables_tab.tab("Check-In"), text="Print", command=self.prompt_print_amount_consumables)
        self.consumables_checkin_frame_Consumable_Print.grid(row=11, column=0, padx=20, pady=(10, 0))

        #consumables checkout tab----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.consumables_checkout_title = customtkinter.CTkLabel(self.consumables_tab.tab("Check-Out"), text="Consumables Check-Out",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.consumables_checkout_title.grid(row=1, column=0, padx=20, pady=(20,5))
        self.consumables_checkout_frame_asset = customtkinter.CTkEntry(self.consumables_tab.tab("Check-Out"), placeholder_text="Asset Number")
        self.consumables_checkout_frame_asset.grid(row=2, column=0, padx=20, pady=(20, 0))
        self.consumables_checkout_frame_Volume = customtkinter.CTkEntry(self.consumables_tab.tab("Check-Out"),placeholder_text="Amount")
        self.consumables_checkout_frame_Volume.grid(row=3, column=0, padx=20, pady=1)
        self.consumables_checkout_frame_Consumable_Submit = customtkinter.CTkButton(self.consumables_tab.tab("Check-Out"), text="Submit", command=self.insert_consumable_data)
        self.consumables_checkout_frame_Consumable_Submit.grid(row=8, column=0, padx=20, pady=(10, 0))

        #consumables location tab----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.consumables_checkout_title = customtkinter.CTkLabel(self.consumables_tab.tab("Location Change"), text="Consumables Location",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.consumables_checkout_title.grid(row=1, column=0, padx=20, pady=(20,5))
        self.consumables_location_change_frame_asset = customtkinter.CTkEntry(self.consumables_tab.tab("Location Change"), placeholder_text="Asset Number")
        self.consumables_location_change_frame_asset.grid(row=2, column=0, padx=20, pady=(20, 0))
        self.consumables_location_change_input = customtkinter.CTkEntry(self.consumables_tab.tab("Location Change"),placeholder_text="Location")
        self.consumables_location_change_input.grid(row=3, column=0, padx=20, pady=1)
        self.consumables_checkout_frame_Consumable_Submit = customtkinter.CTkButton(self.consumables_tab.tab("Location Change"), text="Submit", command=self.save_new_location_consumables)
        self.consumables_checkout_frame_Consumable_Submit.grid(row=8, column=0, padx=20, pady=(10, 0))


        # create Solutions frame----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.solutions_tab = customtkinter.CTkTabview(self, width=1000)
        self.solutions_tab.grid(row=0, column=1, padx=(20, 20), pady=(0, 0), sticky="nsew")
        self.solutions_tab.add("Check-In")
        self.solutions_tab.add("Check-Out")
        self.solutions_tab.add("Location Change")
        self.solutions_tab.tab("Check-In").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.solutions_tab.tab("Check-Out").grid_columnconfigure(0, weight=1)
        self.solutions_tab.tab("Location Change").grid_columnconfigure(0, weight=1)

        self.solutions_checkin_title = customtkinter.CTkLabel(self.solutions_tab.tab("Check-In"), text="Solutions Check-In",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.solutions_checkin_title.grid(row=1, column=0, padx=20, pady=(20,5))
        self.solutions_frame_Solutions_Name = customtkinter.CTkEntry(self.solutions_tab.tab("Check-In"), placeholder_text="Name")
        self.solutions_frame_Solutions_Name.grid(row=2, column=0, padx=20, pady=(20, 0))
        self.solutions_frame_Solutions_Concentration = customtkinter.CTkEntry(self.solutions_tab.tab("Check-In"),placeholder_text="Concentration")
        self.solutions_frame_Solutions_Concentration.grid(row=3, column=0, padx=20, pady=1)
        self.solutions_frame_Solutions_DevProt = customtkinter.CTkEntry(self.solutions_tab.tab("Check-In"), placeholder_text="DevProt/Vendor")
        self.solutions_frame_Solutions_DevProt.grid(row=4, column=0, padx=20, pady=1)
        self.solutions_frame_Solutions_Prep_Date = DateEntry(self.solutions_tab.tab("Check-In"), date_pattern="yyyy/mm/dd", width=20)
        self.solutions_frame_Solutions_Prep_Date.grid(row=5, column=0, padx=20, pady=1)
        self.solutions_frame_Solutions_Exp_Date = DateEntry(self.solutions_tab.tab("Check-In"), date_pattern="yyyy/mm/dd", width=20)
        self.solutions_frame_Solutions_Exp_Date.grid(row=6, column=0, padx=20, pady=1)
        self.solutions_frame_Solutions_Volume = customtkinter.CTkEntry(self.solutions_tab.tab("Check-In"), placeholder_text="Volume")
        self.solutions_frame_Solutions_Volume.grid(row=7, column=0, padx=20, pady=1)
        self.solutions_frame_Solutions_Location = customtkinter.CTkEntry(self.solutions_tab.tab("Check-In"), placeholder_text="Location")
        self.solutions_frame_Solutions_Location.grid(row=8, column=0, padx=20, pady=1)
        self.solutions_frame_Solutions_Insert_Amount = customtkinter.CTkEntry(self.solutions_tab.tab("Check-In"), placeholder_text="Insert Amount")
        self.solutions_frame_Solutions_Insert_Amount.grid(row=9, column=0, padx=20, pady=1)
        self.solutions_frame_Solutions_Submit = customtkinter.CTkButton(self.solutions_tab.tab("Check-In"), text="Submit", command= self.insert_solution_data)
        self.solutions_frame_Solutions_Submit.grid(row=10, column=0, padx=20, pady=(10, 0))
        self.solutions_checkin_frame_solutions_Print = customtkinter.CTkButton(self.solutions_tab.tab("Check-In"), text="Print", command=self.prompt_print_amount_solutions)
        self.solutions_checkin_frame_solutions_Print.grid(row=11, column=0, padx=20, pady=(10, 0))

        #solutions checkout tab----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.solutions_checkout_volume_title = customtkinter.CTkLabel(self.solutions_tab.tab("Check-Out"), text="Solutions Check-Out",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.solutions_checkout_volume_title.grid(row=1, column=0, padx=20, pady=(20,5))
        self.solutions_checkout_volume_frame_asset = customtkinter.CTkEntry(self.solutions_tab.tab("Check-Out"), placeholder_text="Asset Number", width=160)
        self.solutions_checkout_volume_frame_asset.grid(row=2, column=0, padx=20, pady=(20, 0))
        self.solutions_checkout_frame_Volume = customtkinter.CTkEntry(self.solutions_tab.tab("Check-Out"),placeholder_text="Amount", width=160)
        self.solutions_checkout_frame_Volume.grid(row=3, column=0, padx=20, pady=1)
        self.solutions_checkout_frame_Submit = customtkinter.CTkButton(self.solutions_tab.tab("Check-Out"), text="Submit", command=self.volume_checkout_solutions)
        self.solutions_checkout_frame_Submit.grid(row=8, column=0, padx=20, pady=(10, 0))

        #solutions location tab----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.solutions_location_change_title = customtkinter.CTkLabel(self.solutions_tab.tab("Location Change"), text="Solutions Location",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.solutions_location_change_title.grid(row=1, column=0, padx=20, pady=(20,5))
        self.solutions_location_change_frame_asset = customtkinter.CTkEntry(self.solutions_tab.tab("Location Change"), placeholder_text="Asset Number",width=160)
        self.solutions_location_change_frame_asset.grid(row=2, column=0, padx=20, pady=(20, 0))
        self.solutions_location_change_input = customtkinter.CTkEntry(self.solutions_tab.tab("Location Change"),placeholder_text="Location",width=160)
        self.solutions_location_change_input.grid(row=3, column=0, padx=20, pady=1)
        self.solutions_location_change_Submit = customtkinter.CTkButton(self.solutions_tab.tab("Location Change"), text="Submit", command=self.save_new_location_solutions)
        self.solutions_location_change_Submit.grid(row=8, column=0, padx=20, pady=(10, 0))


        #create antibody frame----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.antibody_tab = customtkinter.CTkTabview(self, width=1000)
        self.antibody_tab.grid(row=0, column=1, padx=(20, 20), pady=(0, 0), sticky="nsew")
        self.antibody_tab.add("Check-In")
        self.antibody_tab.add("Check-Out")
        self.antibody_tab.add("Location Change")
        self.antibody_tab.tab("Check-In").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.antibody_tab.tab("Check-Out").grid_columnconfigure(0, weight=1)
        self.antibody_tab.tab("Location Change").grid_columnconfigure(0, weight=1)

        self.antibody_checkin_title = customtkinter.CTkLabel(self.antibody_tab.tab("Check-In"), text="Antibody Check-In",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.antibody_checkin_title.grid(row=1, column=0, padx=20, pady=(20,5))
        self.antibody_frame_Name = customtkinter.CTkEntry(self.antibody_tab.tab("Check-In"), placeholder_text="Name")
        self.antibody_frame_Name.grid(row=2, column=0, padx=20, pady=(20, 0))
        self.antibody_frame_Concentration = customtkinter.CTkEntry(self.antibody_tab.tab("Check-In"),placeholder_text="Concentration")
        self.antibody_frame_Concentration.grid(row=3, column=0, padx=20, pady=1)
        self.antibody_frame_vendor = customtkinter.CTkEntry(self.antibody_tab.tab("Check-In"), placeholder_text="DevProt/Vendor")
        self.antibody_frame_vendor.grid(row=4, column=0, padx=20, pady=1)
        self.antibody_frame_Prep_Date = DateEntry(self.antibody_tab.tab("Check-In"), date_pattern="yyyy/mm/dd", width=20)
        self.antibody_frame_Prep_Date.grid(row=5, column=0, padx=20, pady=1)
        self.antibody_frame_Exp_Date = DateEntry(self.antibody_tab.tab("Check-In"), date_pattern="yyyy/mm/dd", width=20)
        self.antibody_frame_Exp_Date.grid(row=6, column=0, padx=20, pady=1)
        self.antibody_frame_Volume = customtkinter.CTkEntry(self.antibody_tab.tab("Check-In"), placeholder_text="Volume")
        self.antibody_frame_Volume.grid(row=7, column=0, padx=20, pady=1)
        self.antibody_frame_Location = customtkinter.CTkEntry(self.antibody_tab.tab("Check-In"), placeholder_text="Location")
        self.antibody_frame_Location.grid(row=8, column=0, padx=20, pady=1)
        self.antibody_frame_Insert_Amount = customtkinter.CTkEntry(self.antibody_tab.tab("Check-In"), placeholder_text="Insert Amount")
        self.antibody_frame_Insert_Amount.grid(row=9, column=0, padx=20, pady=1)
        self.antibody_frame_Submit = customtkinter.CTkButton(self.antibody_tab.tab("Check-In"), text="Submit", command= self.insert_antibody_data)
        self.antibody_frame_Submit.grid(row=10, column=0, padx=20, pady=(10, 0))
        self.antibody_checkin_frame_antibody_Print = customtkinter.CTkButton(self.antibody_tab.tab("Check-In"), text="Print", command=self.prompt_print_amount_antibody)
        self.antibody_checkin_frame_antibody_Print.grid(row=11, column=0, padx=20, pady=(10, 0))

        #antibody checkout tab----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.antibody_checkout_title = customtkinter.CTkLabel(self.antibody_tab.tab("Check-Out"), text="Antibody Check-Out",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.antibody_checkout_title.grid(row=1, column=0, padx=20, pady=(20,5))
        self.antibody_checkout_frame_asset = customtkinter.CTkEntry(self.antibody_tab.tab("Check-Out"), placeholder_text="Asset Number",width=160)
        self.antibody_checkout_frame_asset.grid(row=2, column=0, padx=20, pady=(20, 0))
        self.antibody_checkout_frame_Volume = customtkinter.CTkEntry(self.antibody_tab.tab("Check-Out"),placeholder_text="Amount",width=160)
        self.antibody_checkout_frame_Volume.grid(row=3, column=0, padx=20, pady=1)
        self.antibody_checkout_frame_Consumable_Submit = customtkinter.CTkButton(self.antibody_tab.tab("Check-Out"), text="Submit", command=self.volume_checkout_antibody)
        self.antibody_checkout_frame_Consumable_Submit.grid(row=8, column=0, padx=20, pady=(10, 0))

        #antibody location tab----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.antibody_checkout_title = customtkinter.CTkLabel(self.antibody_tab.tab("Location Change"), text="Antibody Location",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.antibody_checkout_title.grid(row=1, column=0, padx=20, pady=(20,5))
        self.antibody_checkout_frame_location_asset = customtkinter.CTkEntry(self.antibody_tab.tab("Location Change"), placeholder_text="Asset Number",width=160)
        self.antibody_checkout_frame_location_asset.grid(row=2, column=0, padx=20, pady=(20, 0))
        self.antibody_checkout_frame_input = customtkinter.CTkEntry(self.antibody_tab.tab("Location Change"),placeholder_text="Location",width=160)
        self.antibody_checkout_frame_input.grid(row=3, column=0, padx=20, pady=1)
        self.antibody_checkout_frame_Consumable_Submit = customtkinter.CTkButton(self.antibody_tab.tab("Location Change"), text="Submit", command=self.save_new_location_antibody)
        self.antibody_checkout_frame_Consumable_Submit.grid(row=8, column=0, padx=20, pady=(10, 0))

        #create adc frame----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.adc_tab = customtkinter.CTkTabview(self, width=1000)
        self.adc_tab.grid(row=0, column=1, padx=(20, 20), pady=(0, 0), sticky="nsew")
        self.adc_tab.add("Check-In")
        self.adc_tab.add("Check-Out")
        self.adc_tab.add("Location Change")
        self.adc_tab.tab("Check-In").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.adc_tab.tab("Check-Out").grid_columnconfigure(0, weight=1)
        self.adc_tab.tab("Location Change").grid_columnconfigure(0, weight=1)

        self.adc_checkin_title = customtkinter.CTkLabel(self.adc_tab.tab("Check-In"), text="ADC Check-In",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.adc_checkin_title.grid(row=1, column=0, padx=20, pady=(20,5))
        self.adc_frame_Name = customtkinter.CTkEntry(self.adc_tab.tab("Check-In"), placeholder_text="Name")
        self.adc_frame_Name.grid(row=2, column=0, padx=20, pady=1)
        self.adc_frame_dar = customtkinter.CTkEntry(self.adc_tab.tab("Check-In"), placeholder_text="DAR")
        self.adc_frame_dar.grid(row=3, column=0, padx=20, pady=1)
        self.adc_frame_Concentration = customtkinter.CTkEntry(self.adc_tab.tab("Check-In"),placeholder_text="Concentration")
        self.adc_frame_Concentration.grid(row=4, column=0, padx=20, pady=1)
        self.adc_frame_devprot = customtkinter.CTkEntry(self.adc_tab.tab("Check-In"), placeholder_text="DevProt/Vendor")
        self.adc_frame_devprot.grid(row=5, column=0, padx=20, pady=1)
        self.adc_frame_Prep_Date = DateEntry(self.adc_tab.tab("Check-In"), date_pattern="yyyy/mm/dd", width=20)
        self.adc_frame_Prep_Date.grid(row=6, column=0, padx=20, pady=1)
        self.adc_frame_Exp_Date = DateEntry(self.adc_tab.tab("Check-In"), date_pattern="yyyy/mm/dd", width=20)
        self.adc_frame_Exp_Date.grid(row=7, column=0, padx=20, pady=1)
        self.adc_frame_Volume = customtkinter.CTkEntry(self.adc_tab.tab("Check-In"), placeholder_text="Volume")
        self.adc_frame_Volume.grid(row=8, column=0, padx=20, pady=1)
        self.adc_frame_Location = customtkinter.CTkEntry(self.adc_tab.tab("Check-In"), placeholder_text="Location")
        self.adc_frame_Location.grid(row=9, column=0, padx=20, pady=1)
        self.adc_frame_Insert_Amount = customtkinter.CTkEntry(self.adc_tab.tab("Check-In"), placeholder_text="Insert Amount")
        self.adc_frame_Insert_Amount.grid(row=10, column=0, padx=20, pady=1)
        self.adc_frame_Submit = customtkinter.CTkButton(self.adc_tab.tab("Check-In"), text="Submit", command= self.insert_adc_data)
        self.adc_frame_Submit.grid(row=11, column=0, padx=20, pady=(10, 0))
        self.adc_checkin_frame_adc_Print = customtkinter.CTkButton(self.adc_tab.tab("Check-In"), text="Print", command=self.prompt_print_amount_adc)
        self.adc_checkin_frame_adc_Print.grid(row=12, column=0, padx=20, pady=(10, 0))

        #adc checkout tab----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.adc_checkout_title = customtkinter.CTkLabel(self.adc_tab.tab("Check-Out"), text="ADC Check-Out",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.adc_checkout_title.grid(row=1, column=0, padx=20, pady=(20,5))
        self.adc_checkout_frame_asset = customtkinter.CTkEntry(self.adc_tab.tab("Check-Out"), placeholder_text="Asset Number", width=160)
        self.adc_checkout_frame_asset.grid(row=2, column=0, padx=20, pady=(20, 0))
        self.adc_checkout_frame_Volume = customtkinter.CTkEntry(self.adc_tab.tab("Check-Out"),placeholder_text="Amount",width=160)
        self.adc_checkout_frame_Volume.grid(row=3, column=0, padx=20, pady=1)
        self.adc_checkout_frame_Consumable_Submit = customtkinter.CTkButton(self.adc_tab.tab("Check-Out"), text="Submit", command=self.volume_checkout_adc)
        self.adc_checkout_frame_Consumable_Submit.grid(row=8, column=0, padx=20, pady=(10, 0))

        #adc location tab----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.adc_checkout_title = customtkinter.CTkLabel(self.adc_tab.tab("Location Change"), text="ADC Location",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.adc_checkout_title.grid(row=1, column=0, padx=20, pady=(20,5))
        self.adc_checkout_frame_location_asset = customtkinter.CTkEntry(self.adc_tab.tab("Location Change"), placeholder_text="Asset Number",width=160)
        self.adc_checkout_frame_location_asset.grid(row=2, column=0, padx=20, pady=(20, 0))
        self.adc_checkout_frame_input = customtkinter.CTkEntry(self.adc_tab.tab("Location Change"),placeholder_text="Location",width=160)
        self.adc_checkout_frame_input.grid(row=3, column=0, padx=20, pady=1)
        self.adc_checkout_frame_Consumable_Submit = customtkinter.CTkButton(self.adc_tab.tab("Location Change"), text="Submit", command=self.save_new_location_adc)
        self.adc_checkout_frame_Consumable_Submit.grid(row=8, column=0, padx=20, pady=(10, 0))

        # select default frame----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.select_frame_by_name("Search")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.consumables_button.configure(fg_color=("gray75", "gray25") if name == "Consumables" else "transparent")
        self.solutions_button.configure(fg_color=("gray75", "gray25") if name == "Solutions" else "transparent")
        self.search_button.configure(fg_color=("gray75", "gray25") if name == "Search" else "transparent")
        self.antibody_button.configure(fg_color=("gray75", "gray25") if name == "Antibody" else "transparent")        
        self.adc_button.configure(fg_color=("gray75", "gray25") if name == "ADC" else "transparent")

        # show selected frame
        if name == "Search":
            self.search_frame.grid(row=0, column=1, padx=(20, 20), sticky="nsew")
        else:
            self.search_frame.grid_forget()  

        if name == "Consumables":
            self.consumables_tab.grid(row=0, column=1, padx=(20, 20), sticky="nsew")
        else:
            self.consumables_tab.grid_forget()

        if name == "Solutions":
            self.solutions_tab.grid(row=0, column=1, padx=(20, 20), sticky="nsew")
        else:
            self.solutions_tab.grid_forget()

        if name == "Antibody":
            self.antibody_tab.grid(row=0, column=1, padx=(20, 20), sticky="nsew")
        else:
            self.antibody_tab.grid_forget()

        if name == "ADC":
            self.adc_tab.grid(row=0, column=1, sticky="nsew")
        else:
            self.adc_tab.grid_forget()          


    def Consumables_button_event(self):
        self.select_frame_by_name("Consumables")

    def Solutions_button_event(self):
        self.select_frame_by_name("Solutions")

    def Search_button_event(self):
        self.select_frame_by_name("Search")

    def Antibody_button_event(self):
        self.select_frame_by_name("Antibody")

    def adc_button_event(self):
        self.select_frame_by_name("ADC")        

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def generate_random_number(self, date_str):
        try:
            # Parse the date string into a datetime object
            date = datetime.strptime(date_str, "%Y/%m/%d")

            # Generate a random part and format the date
            random_part = str(random.randint(100000, 999999))
            formatted_date = date.strftime("%d-%b-%Y").upper()

            # Generate the asset number
            asset_number = f"AS-{formatted_date}-{random_part}"

            return asset_number
        except ValueError:
            print("Invalid date format. Please use yyyy/mm/dd.")
            return None
    
    def remove_item(self):
        if self.radiobutton_frame:
            # Get a list of all child widgets within radiobutton_frame
            children = self.radiobutton_frame.winfo_children()

            # Destroy each child widget
            for child in children:
                child.destroy()


    def retrieve_data_by_asset_number(self):
        asset_number = self.search_asset.get()

        # Call the remove_item method to clear old data
        self.remove_item()

        self.search_asset.delete(0, customtkinter.END)

        print(f"Asset Number: {asset_number}")  # Debugging print statement

        # Create a cursor
        mycursor = mydb.cursor()

        # Query to retrieve data from the "consumables" table
        consumables_query = "SELECT * FROM consumables WHERE Asset_Number = %s"

        # Query to retrieve data from the "solutions" table
        solutions_query = "SELECT * FROM solutions WHERE Asset_Number = %s"

        # Query to retrieve data from the "antibodies" table
        antibodies_query = "SELECT * FROM antibodies WHERE Asset_Number = %s"

        # Query to retrieve data from the "ADC" table
        adc_query = "SELECT * FROM adc WHERE Asset_Number = %s"
    
        # Query to retrieve location details based on Location ID
        location_query = "SELECT Location_Name FROM locations WHERE Location_ID = %s"




        # Execute the queries with the provided asset number
        mycursor.execute(consumables_query, (asset_number,))
        consumables_data = mycursor.fetchall()

        mycursor.execute(solutions_query, (asset_number,))
        solutions_data = mycursor.fetchall()

        mycursor.execute(antibodies_query, (asset_number,))
        antibodies_data = mycursor.fetchall()

        mycursor.execute(adc_query, (asset_number,))
        adc_data = mycursor.fetchall()


        self.radiobutton_frame = customtkinter.CTkFrame(self.search_frame.tab("Search by Asset Number"))
        self.radiobutton_frame.grid(row=4, column=0, padx=(20, 20), pady=(20, 0))

        # Use a flag to check if any data was found
        data_found = False

        # Display consumables data
        if consumables_data:
            data_found = True  # Data found
            print("Consumables Data:")
            for row in consumables_data:
                # Display consumables information
                consumables_name_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Name: {row[0]}", font=customtkinter.CTkFont(weight="bold"))
                consumables_name_label.grid(row=0, column=0)
                consumables_vendor_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Vendor: {row[1]}", font=customtkinter.CTkFont(weight="bold"))
                consumables_vendor_label.grid(row=1, column=0)
                consumables_catalogue_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Catalogue: {row[2]}", font=customtkinter.CTkFont(weight="bold"))
                consumables_catalogue_label.grid(row=2, column=0)
                consumables_lot_number_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Lot Number: {row[3]}", font=customtkinter.CTkFont(weight="bold"))
                consumables_lot_number_label.grid(row=3, column=0)
                consumables_prep_day_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Prepration Date: {row[4]}", font=customtkinter.CTkFont(weight="bold"))
                consumables_prep_day_label.grid(row=4, column=0)                
                consumables_exp_day_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Expiry Date: {row[5]}", font=customtkinter.CTkFont(weight="bold"))
                consumables_exp_day_label.grid(row=5, column=0)
                consumables_exp_day_location = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Location: {row[6]}", font=customtkinter.CTkFont(weight="bold"))
                consumables_exp_day_location.grid(row=6, column=0)
                consumables_asset_number_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Asset Number: {row[7]}", font=customtkinter.CTkFont(weight="bold"))
                consumables_asset_number_label.grid(row=7, column=0)

                Location_Name = row[6]  # Assuming location ID is in the 'row' variable
                # Execute the query with the provided location ID
                mycursor.execute(location_query, (Location_Name,))
                location_data = mycursor.fetchone()

                antibody_location_description_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Location Description: {location_data[0]}", font=customtkinter.CTkFont(weight="bold"))
                antibody_location_description_label.grid(row=9, column=0)

        # Display solutions data
        if solutions_data:
            data_found = True  # Data found
            print("Solutions Data:")
            for row in solutions_data:
                solutions_name_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Name: {row[0]}", font=customtkinter.CTkFont(weight="bold"))
                solutions_name_label.grid(row=0, column=0)
                solution_concentration_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Concentration (mM): {row[1]}", font=customtkinter.CTkFont(weight="bold"))
                solution_concentration_label.grid(row=1, column=0)
                solution_DevProt_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"DevProt: {row[2]}", font=customtkinter.CTkFont(weight="bold"))
                solution_DevProt_label.grid(row=2, column=0)
                solution_prep_day_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Preparation date: {row[3]}", font=customtkinter.CTkFont(weight="bold"))
                solution_prep_day_label.grid(row=3, column=0)
                solution_exp_day_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Expiry Date: {row[4]}", font=customtkinter.CTkFont(weight="bold"))
                solution_exp_day_label.grid(row=4, column=0)
                solution_volume_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Volume (µL): {row[5]}", font=customtkinter.CTkFont(weight="bold"))
                solution_volume_label.grid(row=5, column=0)
                solution_location_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Location: {row[6]}", font=customtkinter.CTkFont(weight="bold"))
                solution_location_label.grid(row=6, column=0)
                solution_asset_number_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Asset Number: {row[7]}", font=customtkinter.CTkFont(weight="bold"))
                solution_asset_number_label.grid(row=7, column=0)

                Location_Name = row[7]  # Assuming location ID is in the 'row' variable
                # Execute the query with the provided location ID
                mycursor.execute(location_query, (Location_Name,))
                location_data = mycursor.fetchone()

                antibody_location_description_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Location Description: {location_data[0]}", font=customtkinter.CTkFont(weight="bold"))
                antibody_location_description_label.grid(row=9, column=0)


                # Display antibodies data
        if antibodies_data:
            data_found = True  # Data found
            print("Antibodies Data:")
            for row in antibodies_data:
                antibody_name_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Name: {row[0]}", font=customtkinter.CTkFont(weight="bold"))
                antibody_name_label.grid(row=0, column=0)
                antibody_concentration_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Concentration (mg/mL): {row[1]}", font=customtkinter.CTkFont(weight="bold"))
                antibody_concentration_label.grid(row=1, column=0)
                antibody_DevProt_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Vendor: {row[2]}", font=customtkinter.CTkFont(weight="bold"))
                antibody_DevProt_label.grid(row=2, column=0)
                antibody_prep_day_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Preparation date: {row[3]}", font=customtkinter.CTkFont(weight="bold"))
                antibody_prep_day_label.grid(row=3, column=0)
                antibody_exp_day_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Expiry Date: {row[4]}", font=customtkinter.CTkFont(weight="bold"))
                antibody_exp_day_label.grid(row=4, column=0)
                antibody_volume_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Volume (µL): {row[5]}", font=customtkinter.CTkFont(weight="bold"))
                antibody_volume_label.grid(row=5, column=0)
                antibody_location_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Location: {row[6]}", font=customtkinter.CTkFont(weight="bold"))
                antibody_location_label.grid(row=6, column=0)
                antibody_asset_number_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Asset Number: {row[7]}", font=customtkinter.CTkFont(weight="bold"))
                antibody_asset_number_label.grid(row=7, column=0)

                Location_Name = row[6]  # Assuming location ID is in the 'row' variable

                # Execute the query with the provided location ID
                mycursor.execute(location_query, (Location_Name,))
                location_data = mycursor.fetchone()

                antibody_location_description_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Location Description: {location_data[0]}", font=customtkinter.CTkFont(weight="bold"))
                antibody_location_description_label.grid(row=9, column=0)

                # Display adc data
        if adc_data:
            data_found = True  # Data found
            print("ADC Data:")
            for row in adc_data:
                adc_name_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Name: {row[0]}", font=customtkinter.CTkFont(weight="bold"))
                adc_name_label.grid(row=0, column=0)
                adc_dar_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"DAR: {row[1]}", font=customtkinter.CTkFont(weight="bold"))
                adc_dar_label.grid(row=1, column=0)
                adc_concentration_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Concentration (mg/mL): {row[2]}", font=customtkinter.CTkFont(weight="bold"))
                adc_concentration_label.grid(row=2, column=0)
                adc_DevProt_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Vendor: {row[3]}", font=customtkinter.CTkFont(weight="bold"))
                adc_DevProt_label.grid(row=3, column=0)
                adc_prep_day_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Preparation date: {row[4]}", font=customtkinter.CTkFont(weight="bold"))
                adc_prep_day_label.grid(row=4, column=0)
                adc_exp_day_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Expiry Date: {row[5]}", font=customtkinter.CTkFont(weight="bold"))
                adc_exp_day_label.grid(row=5, column=0)
                adc_volume_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Volume (µL): {row[6]}", font=customtkinter.CTkFont(weight="bold"))
                adc_volume_label.grid(row=6, column=0)
                adc_location_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Location: {row[7]}", font=customtkinter.CTkFont(weight="bold"))
                adc_location_label.grid(row=7, column=0)
                adc_asset_number_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Asset Number: {row[8]}", font=customtkinter.CTkFont(weight="bold"))
                adc_asset_number_label.grid(row=8, column=0)

                Location_Name = row[7]  # Assuming location ID is in the 'row' variable

                # Execute the query with the provided location ID
                mycursor.execute(location_query, (Location_Name,))
                location_data = mycursor.fetchone()

                antibody_location_description_label = customtkinter.CTkLabel(self.radiobutton_frame, text=f"Location Description: {location_data[0]}", font=customtkinter.CTkFont(weight="bold"))
                antibody_location_description_label.grid(row=9, column=0)





        # If no data found, display "No Data"
        if not data_found:
            print("No Data Found")  # Debugging print statement
            no_data_label = customtkinter.CTkLabel(self.radiobutton_frame, text="No Data Found", font=customtkinter.CTkFont(weight="bold"))
            no_data_label.grid(row=0, column=0)
            

        #Insert DATE CHECK IN=-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def insert_consumable_data(self):
        # Get input from GUI elements
        name = self.consumables_checkin_frame_Consumable_Name.get()
        vendor = self.consumables_checkin_frame_Consumable_Vendor.get()
        catalogue = self.consumables_checkin_frame_Consumable_Catalogue.get()
        lot_number = self.consumables_checkin_frame_Consumable_Lot.get()
        location = self.consumables_checkin_frame_Consumable_location.get()


        # Get the date as a string from the DateEntry widget
        prep_day = self.consumables_checkin_frame_consumable_Prep_Date.get()        
        exp_day = self.consumables_checkin_frame_Consumable_Exp_Date.get()

        try:
            preparation_day = datetime.strptime(prep_day, "%Y/%m/%d")
        except ValueError:
            # Handle the case where the date string is not in the expected format
            print("Invalid date format. Please use yyyy/mm/dd.")
            return
        
        # Convert the date string to a datetime object
        try:
            expiry_date = datetime.strptime(exp_day, "%Y/%m/%d")
        except ValueError:
            # Handle the case where the date string is not in the expected format
            print("Invalid date format. Please use yyyy/mm/dd.")
            return

        # Get the "Insert Amount" value as an integer
        try:
            insert_amount = int(self.consumables_checkin_frame_Insert_Amount.get())
        except ValueError:
            print("Invalid insert amount. Please enter a valid number.")
            return

        # Check if insert_amount is a positive number
        if insert_amount <= 0:
            print("Insert amount must be a positive number.")
            return

        mycursor = mydb.cursor()

        # Insert multiple rows with unique asset numbers
        for _ in range(insert_amount):
            as_number = self.generate_random_number(prep_day)  # Generate a unique asset number
            self.asset_numbers.append(as_number)  # Store the asset number

            # SQL INSERT statement
            sql_insert = "INSERT INTO consumables (Name, Vendor, Catalogue, Lot_Number, Prep_day, Expiry_Date, Location, Asset_Number) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"

            # Data to insert
            data = (name, vendor, catalogue, lot_number, preparation_day, expiry_date, location, as_number)

            # Create a cursor

            # Execute the INSERT statement
            mycursor.execute(sql_insert, data)

            
        # Commit changes to the database
        mydb.commit()
        
        messagebox.showinfo("Success", "Added successfully.")

    def insert_solution_data(self):
        # Get input from GUI elements
        name = self.solutions_frame_Solutions_Name.get()
        concentration = self.solutions_frame_Solutions_Concentration.get()
        dev_prot = self.solutions_frame_Solutions_DevProt.get()
        preparation_day = self.solutions_frame_Solutions_Prep_Date.get()
        expiry_day = self.solutions_frame_Solutions_Exp_Date.get()
        volume = self.solutions_frame_Solutions_Volume.get()
        location = self.solutions_frame_Solutions_Location.get()

        # Get the date as a string from the DateEntry widget
        prep_day = self.solutions_frame_Solutions_Prep_Date.get()
        expiry_day = self.solutions_frame_Solutions_Exp_Date.get()

        try:
            preparation_day = datetime.strptime(prep_day, "%Y/%m/%d")
        except ValueError:
            # Handle the case where the date string is not in the expected format
            print("Invalid date format. Please use yyyy/mm/dd.")
            return
        

        # Convert the date string to a datetime object
        try:
            expiry_day = datetime.strptime(expiry_day, "%Y/%m/%d")
        except ValueError:
            # Handle the case where the date string is not in the expected format
            print("Invalid date format. Please use yyyy/mm/dd.")
            return
        

        # Get the "Insert Amount" value as an integer
        try:
            insert_amount = int(self.solutions_frame_Solutions_Insert_Amount.get())
        except ValueError:
            print("Invalid insert amount. Please enter a valid number.")
            return

        # Check if insert_amount is a positive number
        if insert_amount <= 0:
            print("Insert amount must be a positive number.")
            return


        # Insert multiple rows with unique asset numbers
        for _ in range(insert_amount):
            as_number = self.generate_random_number(prep_day)  # Generate a unique asset number
            self.asset_numbers.append(as_number)  # Store the asset number

            # SQL INSERT statement for the "solutions" table
            sql_insert = "INSERT INTO solutions (Name, Concentration, DevProt, Preparation_Day, Expiry_Day, Asset_Number, Volume, Location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

            # Data to insert
            data = (name, concentration, dev_prot, preparation_day, expiry_day, as_number, volume, location)

            # Create a cursor
            mycursor = mydb.cursor()

            # Execute the INSERT statement
            mycursor.execute(sql_insert, data)

        # Commit changes to the database
        mydb.commit()
        messagebox.showinfo("Success", "Added successfully.")

    def insert_antibody_data(self):
            # Get input from GUI elements
            name = self.antibody_frame_Name.get()
            vendor = self.antibody_frame_vendor.get()
            concentration = self.antibody_frame_Concentration.get()
            preparation_day = self.antibody_frame_Prep_Date.get()
            expiry_day = self.antibody_frame_Exp_Date.get()
            volume = self.antibody_frame_Volume.get()
            location = self.antibody_frame_Location.get()

            # Get the date as a string from the DateEntry widget
            prep_day = self.antibody_frame_Prep_Date.get()
            expiry_day = self.antibody_frame_Exp_Date.get()

            try:
                preparation_day = datetime.strptime(prep_day, "%Y/%m/%d")
            except ValueError:
                # Handle the case where the date string is not in the expected format
                print("Invalid date format. Please use yyyy/mm/dd.")
                return
            

            # Convert the date string to a datetime object
            try:
                expiry_day = datetime.strptime(expiry_day, "%Y/%m/%d")
            except ValueError:
                # Handle the case where the date string is not in the expected format
                print("Invalid date format. Please use yyyy/mm/dd.")
                return
            

            # Get the "Insert Amount" value as an integer
            try:
                insert_amount = int(self.antibody_frame_Insert_Amount.get())
            except ValueError:
                print("Invalid insert amount. Please enter a valid number.")
                return

            # Check if insert_amount is a positive number
            if insert_amount <= 0:
                print("Insert amount must be a positive number.")
                return

            # Insert multiple rows with unique asset numbers
            for _ in range(insert_amount):
                as_number = self.generate_random_number(prep_day)  # Generate a unique asset number
                self.asset_numbers.append(as_number)  # Store the asset number

                # SQL INSERT statement for the "solutions" table
                sql_insert = "INSERT INTO antibodies (Name, Vendor, Concentration, Preparation_Day, Expiry_Day, Volume, Location, Asset_Number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

                # Data to insert
                data = (name, vendor, concentration,preparation_day, expiry_day, volume, location, as_number)

                # Create a cursor
                mycursor = mydb.cursor()

                # Execute the INSERT statement
                mycursor.execute(sql_insert, data)

            # Commit changes to the database
            mydb.commit()
            messagebox.showinfo("Success", "Added successfully.")

    def insert_adc_data(self):
            # Get input from GUI elements
            name = self.adc_frame_Name.get()
            dar = self.adc_frame_dar.get()
            concentration = self.adc_frame_Concentration.get()
            devprot = self.adc_frame_devprot.get()
            preparation_day = self.adc_frame_Prep_Date.get()
            expiry_day = self.adc_frame_Exp_Date.get()
            volume = self.adc_frame_Volume.get()
            location = self.adc_frame_Location.get()

            # Get the date as a string from the DateEntry widget
            prep_day = self.adc_frame_Prep_Date.get()
            expiry_day = self.adc_frame_Exp_Date.get()

            try:
                preparation_day = datetime.strptime(prep_day, "%Y/%m/%d")
            except ValueError:
                # Handle the case where the date string is not in the expected format
                print("Invalid date format. Please use yyyy/mm/dd.")
                return
            

            # Convert the date string to a datetime object
            try:
                expiry_day = datetime.strptime(expiry_day, "%Y/%m/%d")
            except ValueError:
                # Handle the case where the date string is not in the expected format
                print("Invalid date format. Please use yyyy/mm/dd.")
                return
            

            # Get the "Insert Amount" value as an integer
            try:
                insert_amount = int(self.adc_frame_Insert_Amount.get())
            except ValueError:
                print("Invalid insert amount. Please enter a valid number.")
                return

            # Check if insert_amount is a positive number
            if insert_amount <= 0:
                print("Insert amount must be a positive number.")
                return

            # Insert multiple rows with unique asset numbers
            for _ in range(insert_amount):
                as_number = self.generate_random_number(prep_day)  # Generate a unique asset number
                self.asset_numbers.append(as_number)  # Store the asset number

                # SQL INSERT statement for the "solutions" table
                sql_insert = "INSERT INTO adc (Name, DAR, Concentration, DevProt, Preparation_Day, Expiry_Day, Volume, Location, Asset_Number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

                # Data to insert
                data = (name, dar, concentration, devprot,preparation_day, expiry_day, volume, location, as_number)

                # Create a cursor
                mycursor = mydb.cursor()

                # Execute the INSERT statement
                mycursor.execute(sql_insert, data)

            # Commit changes to the database
            mydb.commit()
            messagebox.showinfo("Success", "Added successfully.")

    #Volume checkout---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def volume_checkout_solutions(self):
        asset_number = self.solutions_checkout_volume_frame_asset.get()

        # Get the value for volume change
        volume_change_str = self.solutions_checkout_frame_Volume.get()

        # Check if volume change is provided and convert it to a float
        if volume_change_str:
            try:
                volume_change = float(volume_change_str)
            except ValueError:
                print("Invalid volume change amount. Please enter a valid number.")
                return
        else:
            print("Volume change not provided. Please enter a volume change.")
            return

        # Create a cursor
        mycursor = mydb.cursor()

        # Query to retrieve the current volume for the given asset number
        select_query = "SELECT Volume FROM solutions WHERE Asset_Number = %s"

        # Execute the query with the provided asset number
        mycursor.execute(select_query, (asset_number,))
        result = mycursor.fetchone()

        if result:
            current_volume = float(result[0])

            # Calculate the new volume
            new_volume = current_volume - volume_change

            # Update the database with the new volume
            update_query = "UPDATE solutions SET Volume = %s WHERE Asset_Number = %s"
            update_data = (new_volume, asset_number)

            print("Update Query:", update_query)
            print("Update Data:", update_data)

            mycursor.execute(update_query, update_data)
            mydb.commit()

            # Show a success message
            messagebox.showinfo("Success", "Volume updated successfully.")
        else:
            # If no data is found for the asset number, show an error message
            messagebox.showerror("Error", f"No data found for Asset Number: {asset_number}")

    def volume_checkout_antibody(self):
        asset_number = self.antibody_checkout_frame_asset.get()

        # Get the value for volume change
        volume_change_str = self.antibody_checkout_frame_Volume.get()

        # Check if volume change is provided and convert it to a float
        if volume_change_str:
            try:
                volume_change = float(volume_change_str)
            except ValueError:
                print("Invalid volume change amount. Please enter a valid number.")
                return
        else:
            print("Volume change not provided. Please enter a volume change.")
            return

        # Create a cursor
        mycursor = mydb.cursor()

        # Query to retrieve the current volume for the given asset number
        select_query = "SELECT Volume FROM antibodies WHERE Asset_Number = %s"

        # Execute the query with the provided asset number
        mycursor.execute(select_query, (asset_number,))
        result = mycursor.fetchone()

        if result:
            current_volume = float(result[0])

            # Calculate the new volume
            new_volume = current_volume - volume_change

            # Update the database with the new volume
            update_query = "UPDATE antibodies SET Volume = %s WHERE Asset_Number = %s"
            update_data = (new_volume, asset_number)

            print("Update Query:", update_query)
            print("Update Data:", update_data)

            mycursor.execute(update_query, update_data)
            mydb.commit()

            # Show a success message
            messagebox.showinfo("Success", "Volume updated successfully.")
        else:
            # If no data is found for the asset number, show an error message
            messagebox.showerror("Error", f"No data found for Asset Number: {asset_number}")

    def volume_checkout_adc(self):
        asset_number = self.adc_checkout_frame_asset.get()

        # Get the value for volume change
        volume_change_str = self.adc_checkout_frame_Volume.get()

        # Check if volume change is provided and convert it to a float
        if volume_change_str:
            try:
                volume_change = float(volume_change_str)
            except ValueError:
                print("Invalid volume change amount. Please enter a valid number.")
                return
        else:
            print("Volume change not provided. Please enter a volume change.")
            return

        # Create a cursor
        mycursor = mydb.cursor()

        # Query to retrieve the current volume for the given asset number
        select_query = "SELECT Volume FROM adc WHERE Asset_Number = %s"

        # Execute the query with the provided asset number
        mycursor.execute(select_query, (asset_number,))
        result = mycursor.fetchone()

        if result:
            current_volume = float(result[0])

            # Calculate the new volume
            new_volume = current_volume - volume_change

            # Update the database with the new volume
            update_query = "UPDATE adc SET Volume = %s WHERE Asset_Number = %s"
            update_data = (new_volume, asset_number)

            print("Update Query:", update_query)
            print("Update Data:", update_data)

            mycursor.execute(update_query, update_data)
            mydb.commit()

            # Show a success message
            messagebox.showinfo("Success", "Volume updated successfully.")
        else:
            # If no data is found for the asset number, show an error message
            messagebox.showerror("Error", f"No data found for Asset Number: {asset_number}")

    #Change location----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def save_new_location_consumables(self):
        asset_number = self.consumables_location_change_frame_asset.get()

        # Get the new location
        new_location = self.consumables_location_change_input.get()

        if not new_location:
            print("New location not provided. Please enter a new location.")
            return

        # Create a cursor
        mycursor = mydb.cursor()

        # Update the database with the new location
        update_query = "UPDATE consumables SET Location = %s WHERE Asset_Number = %s"
        update_data = (new_location, asset_number)

        print("Update Query:", update_query)
        print("Update Data:", update_data)

        mycursor.execute(update_query, update_data)
        mydb.commit()

        # Show a success message
        messagebox.showinfo("Success", "Location updated successfully.")

    def save_new_location_solutions(self):
        asset_number = self.solutions_location_change_frame_asset.get()

        # Get the new location
        new_location = self.solutions_location_change_input.get()

        if not new_location:
            print("New location not provided. Please enter a new location.")
            return

        # Create a cursor
        mycursor = mydb.cursor()

        # Update the database with the new location
        update_query = "UPDATE solutions SET Location = %s WHERE Asset_Number = %s"
        update_data = (new_location, asset_number)

        print("Update Query:", update_query)
        print("Update Data:", update_data)

        mycursor.execute(update_query, update_data)
        mydb.commit()

        # Show a success message
        messagebox.showinfo("Success", "Location updated successfully.")

    def save_new_location_antibody(self):
        asset_number = self.antibody_checkout_frame_location_asset.get()

        # Get the new location
        new_location = self.antibody_checkout_frame_input.get()

        if not new_location:
            print("New location not provided. Please enter a new location.")
            return

        # Create a cursor
        mycursor = mydb.cursor()

        # Update the database with the new location
        update_query = "UPDATE antibodies SET Location = %s WHERE Asset_Number = %s"
        update_data = (new_location, asset_number)

        print("Update Query:", update_query)
        print("Update Data:", update_data)

        mycursor.execute(update_query, update_data)
        mydb.commit()

        # Show a success message
        messagebox.showinfo("Success", "Location updated successfully.")
   
    def save_new_location_adc(self):
        asset_number = self.adc_checkout_frame_location_asset.get()

        # Get the new location
        new_location = self.adc_checkout_frame_input.get()

        if not new_location:
            print("New location not provided. Please enter a new location.")
            return

        # Create a cursor
        mycursor = mydb.cursor()

        # Update the database with the new location
        update_query = "UPDATE adc SET Location = %s WHERE Asset_Number = %s"
        update_data = (new_location, asset_number)

        print("Update Query:", update_query)
        print("Update Data:", update_data)

        mycursor.execute(update_query, update_data)
        mydb.commit()

        # Show a success message
        messagebox.showinfo("Success", "Location updated successfully.")
   

    #Search scroll bars--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def search_consumables(self):
        # Get the name entered by the user
        name = self.search_consumables_name_input.get()
        # Clear the previous search results
        self.search_consumables_name_input.delete(0, customtkinter.END)

        try:
            # Clear previous results in the scrollable frame
            for widget in self.search_slide_consumables_results.winfo_children():
                widget.destroy()

            # Create a cursor
            mycursor = mydb.cursor()

            # Query to retrieve data from the "antibodies" table with a matching name
            consumables_query = "SELECT * FROM consumables WHERE Name = %s"
            mycursor.execute(consumables_query, (name,))
            consumables_data = mycursor.fetchall()

            if consumables_data:
                # Create labels for headings
                headings = ["Name", "Vendor", "Catalogue", "Lot", "Prep_day", "Expiry Date", "Location", "Asset Number"]

                for col, heading in enumerate(headings):
                    label = customtkinter.CTkLabel(self.search_slide_consumables_results, text=heading, font=customtkinter.CTkFont(weight="bold"))
                    label.grid(row=0, column=col, padx=20, pady=(0, 20), sticky="w")

                for row_idx, row in enumerate(consumables_data, start=1):
                    for col, value in enumerate(row):
                        label = customtkinter.CTkLabel(self.search_slide_consumables_results, text=value)
                        label.grid(row=row_idx, column=col, padx=20, pady=(0, 20), sticky="w")

                    # Create a button for each row
                    location_name = row[6]  # Assuming location is in the 7th column (index 6)
                    switch = customtkinter.CTkButton(self.search_slide_consumables_results, text=f"Location Search", command=lambda name=location_name: self.search_location_by_name(name))
                    switch.grid(row=row_idx, column=len(headings), padx=10, pady=(0, 20))
                    self.scrollable_frame_switches.append(switch)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        # If no data found, display "No Data"
        if not consumables_data:
             # Debugging print statement
            no_data_label = customtkinter.CTkLabel(self.search_slide_consumables_results, text="No Data Found", font=customtkinter.CTkFont(weight="bold"))
            no_data_label.grid(row=4, column=4, padx=(610,0))

        self.bind("<Return>", lambda event: self.search_consumables())
    

    def search_solutions(self):
        # Get the name entered by the user
        name = self.search_solutions_name_input.get()
        # Clear the previous search results
        self.search_solutions_name_input.delete(0, customtkinter.END)

        try:
            # Clear previous results in the scrollable frame
            for widget in self.search_slide_solutions_results.winfo_children():
                widget.destroy()

            # Create a cursor
            mycursor = mydb.cursor()

            # Query to retrieve data from the "antibodies" table with a matching name
            solutions_query = "SELECT * FROM solutions WHERE Name = %s"
            mycursor.execute(solutions_query, (name,))
            solutions_data = mycursor.fetchall()


            if solutions_data:
                # Create labels for headings
                headings = ["Name", "Concentration (mM)", "Vendor/DevProt", "Preparation Date", "Expiry Date", "Volume (µL)", "Location", "Asset Number"]

                for col, heading in enumerate(headings):
                    label = customtkinter.CTkLabel(self.search_slide_solutions_results, text=heading, font=customtkinter.CTkFont(weight="bold"))
                    label.grid(row=0, column=col, padx=20, pady=(0, 20), sticky="w")

                for row_idx, row in enumerate(solutions_data, start=1):
                    for col, value in enumerate(row):
                        label = customtkinter.CTkLabel(self.search_slide_solutions_results, text=value)
                        label.grid(row=row_idx, column=col, padx=20, pady=(0, 20), sticky="w")

                    # Create a button for each row
                    location_name = row[6]  # Assuming location is in the 7th column (index 6)
                    switch = customtkinter.CTkButton(self.search_slide_solutions_results, text=f"Location Search", command=lambda name=location_name: self.search_location_by_name(name))
                    switch.grid(row=row_idx, column=len(headings), padx=10, pady=(0, 20))
                    self.scrollable_frame_switches.append(switch)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        # If no data found, display "No Data"
        if not solutions_data:
             # Debugging print statement
            no_data_label = customtkinter.CTkLabel(self.search_slide_solutions_results, text="No Data Found", font=customtkinter.CTkFont(weight="bold"))
            no_data_label.grid(row=4, column=4, padx=(610,0))

    def search_antibodies(self):
        # Get the name entered by the user
        name = self.search_antibodies_name_input.get()
        # Clear the previous search results
        self.search_antibodies_name_input.delete(0, customtkinter.END)

        try:
            # Clear previous results in the scrollable frame
            for widget in self.search_slide_antibodies_results.winfo_children():
                widget.destroy()

            # Create a cursor
            mycursor = mydb.cursor()

            # Query to retrieve data from the "antibodies" table with a matching name
            antibodies_query = "SELECT * FROM antibodies WHERE Name = %s"
            mycursor.execute(antibodies_query, (name,))
            antibodies_data = mycursor.fetchall()

            if antibodies_data:
                # Create labels for headings
                headings = ["Name", "Concentration (mg/mL)", "Vendor", "Preparation Date", "Expiry Date", "Volume (µL)", "Location", "Asset Number"]

                for col, heading in enumerate(headings):
                    label = customtkinter.CTkLabel(self.search_slide_antibodies_results, text=heading, font=customtkinter.CTkFont(weight="bold"))
                    label.grid(row=0, column=col, padx=20, pady=(0, 20), sticky="w")

                for row_idx, row in enumerate(antibodies_data, start=1):
                    for col, value in enumerate(row):
                        label = customtkinter.CTkLabel(self.search_slide_antibodies_results, text=value)
                        label.grid(row=row_idx, column=col, padx=20, pady=(0, 20), sticky="w")

                    # Create a button for each row
                    location_name = row[6]  # Assuming location is in the 7th column (index 6)
                    switch = customtkinter.CTkButton(self.search_slide_antibodies_results, text=f"Location Search", command=lambda name=location_name: self.search_location_by_name(name))
                    switch.grid(row=row_idx, column=len(headings), padx=10, pady=(0, 20))
                    self.scrollable_frame_switches.append(switch)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        # If no data found, display "No Data"
        if not antibodies_data:
             # Debugging print statement
            no_data_label = customtkinter.CTkLabel(self.search_slide_antibodies_results, text="No Data Found", font=customtkinter.CTkFont(weight="bold"))
            no_data_label.grid(row=4, column=4, padx=(610,0))

    def search_adc(self):
        # Get the name entered by the user
        name = self.search_adc_input.get()
        # Clear the previous search results
        self.search_adc_input.delete(0, customtkinter.END)

        try:
            # Clear previous results in the scrollable frame
            for widget in self.search_slide_adc_results.winfo_children():
                widget.destroy()

            # Create a cursor
            mycursor = mydb.cursor()

            # Query to retrieve data from the "adc" table with a matching name
            adc_query = "SELECT * FROM adc WHERE Name = %s"
            mycursor.execute(adc_query, (name,))
            adc_data = mycursor.fetchall()

            if adc_data:
                # Create labels for headings
                headings = ["Name", "DAR", "Concentration (mg/mL)", "Vendor/DevProt", "Preparation Date", "Expiry Date", "Volume (µL)", "Location", "Asset Number"]

                for col, heading in enumerate(headings):
                    label = customtkinter.CTkLabel(self.search_slide_adc_results, text=heading, font=customtkinter.CTkFont(weight="bold"))
                    label.grid(row=0, column=col, padx=20, pady=(0, 20), sticky="w")

                for row_idx, row in enumerate(adc_data, start=1):
                    for col, value in enumerate(row):
                        label = customtkinter.CTkLabel(self.search_slide_adc_results, text=value)
                        label.grid(row=row_idx, column=col, padx=20, pady=(0, 20), sticky="w")

                    # Create a button for each row
                    location_name = row[7]  # Assuming location is in the 7th column (index 6)
                    switch = customtkinter.CTkButton(self.search_slide_adc_results, text=f"Location Search", command=lambda name=location_name: self.search_location_by_name(name))
                    switch.grid(row=row_idx, column=len(headings), padx=10, pady=(0, 20))
                    self.scrollable_frame_switches.append(switch)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        # If no data found, display "No Data"
        if not adc_data:
             # Debugging print statement
            no_data_label = customtkinter.CTkLabel(self.search_slide_adc_results, text="No Data Found", font=customtkinter.CTkFont(weight="bold"))
            no_data_label.grid(row=4, column=4, padx=(610,0))
    #MISC ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def search_location_by_name(self, location_name):
        try:
            # Create a cursor
            mycursor = mydb.cursor()

            # Query to retrieve location details based on Location Name
            location_query = "SELECT Location_ID, Location_Name FROM locations WHERE Location_id = %s"

            # Execute the query with the provided location name
            mycursor.execute(location_query, (location_name,))
            location_data = mycursor.fetchone()

            if location_data:
                location_id, location_name = location_data
                # Display location details in a message box
                message = f"Location ID: {location_id}\n"
                message += f"Location Name: {location_name}\n"
                # ... (other details if needed)
                messagebox.showinfo("Location Details", message)
            else:
                messagebox.showinfo("Location Details", f"No location details found for {location_name}")

        except mysql.connector.Error as err:
            print(f"Error: {err}")


    # create buttons for slide bars
    def search_slide_results(self):
        for i in range(1000):
            switch = customtkinter.CTkButton(master=self.search_slide_consumables_results, text=f"Location Search")
            switch.grid(row=i, column=1, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)
        self.search_slide_consumables_results.grid_columnconfigure(0, weight=1)


    def generate_qr_with_text(self, text, text_lines, asset_number):
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(asset_number)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Create a blank A4-sized image with a white background
        a4_width = 21.0 * 96  # Convert from cm to pixels at 96 DPI
        a4_height = 29.7 * 96  # Convert from cm to pixels at 96 DPI
        combined_img = Image.new('RGB', (int(a4_width), int(a4_height)), 'white')

        # Calculate the position for the QR code (top-left corner)
        qr_x = 600  # Adjust this value for horizontal positioning
        qr_y = 80   # Adjust this value for vertical positioning

        # Paste the QR code onto the image at the specified position
        combined_img.paste(qr_img, (qr_x, qr_y))

        # Initialize a drawing context
        draw = ImageDraw.Draw(combined_img)

        # Specify the positions for the text lines (above and to the left of the QR code)
        text_x = qr_x - 500  # Adjust this value for horizontal positioning
        text_y = qr_y - 50   # Adjust this value for vertical positioning

        # Create a larger font
        font_size = 40
        font = ImageFont.truetype("arial.ttf", font_size)  # You can specify the path to your desired font file

        # Add each text line with the larger font and a gap between lines
        line_gap = 20  # Adjust this value to control the gap between lines
        for line in text_lines:
            draw.text((text_x, text_y), line, fill="black", font=font, weight="bold")
            text_y += font_size + line_gap  # Adjusted for vertical spacing

        return combined_img

    def print_image(self, img, num_copies=1):
        if os.name == 'nt':
            # Windows printing
            printer_name = win32print.GetDefaultPrinter()
            hprinter = win32print.OpenPrinter(printer_name)
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(printer_name)
            hdc.StartDoc('QR Code Document')
            for _ in range(num_copies):
                hdc.StartPage()
                dib = ImageWin.Dib(img)
                dib.draw(hdc.GetHandleOutput(), (0, 0, img.width, img.height))
                hdc.EndPage()
            hdc.EndDoc()
            hdc.DeleteDC()

    def prompt_print_amount_consumables(self):
        # Get the value from the entry widget
        num_copies_str = self.consumables_checkin_frame_Insert_Amount.get()

        try:
            # Convert the value to an integer
            num_copies = int(num_copies_str)

            # Ensure it's a positive integer
            if num_copies > 0:
                # Generate and print QR codes for each asset number
                name = self.consumables_checkin_frame_Consumable_Name.get()
                exp_day = self.consumables_checkin_frame_Consumable_Exp_Date.get()
                prep_day = self.consumables_checkin_frame_consumable_Prep_Date.get()


                for _ in range(num_copies):
                    if not self.asset_numbers:
                        print("No asset numbers available for printing.")
                        return
                    asset_number = self.asset_numbers.pop(0)  # Get and remove the first asset number
                    text = f"{asset_number}\n{name}\nP: {prep_day}\nE: {exp_day}"
                    text_lines = text.split("\n")

                    img = self.generate_qr_with_text(text, text_lines, asset_number)

                    # Display the final image
                    img.show()

                    # Print the image
                    self.print_image(img)

            else:
                print("Invalid input. Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    def prompt_print_amount_solutions(self):
        # Get the value from the entry widget
        num_copies_str = self.solutions_frame_Solutions_Insert_Amount.get()

        try:
            # Convert the value to an integer
            num_copies = int(num_copies_str)

            # Ensure it's a positive integer
            if num_copies > 0:
                # Generate and print QR codes for each asset number
                name = self.solutions_frame_Solutions_Name.get()
                exp_day = self.solutions_frame_Solutions_Exp_Date.get()
                prep_day = self.solutions_frame_Solutions_Prep_Date.get()
                dev_prot = self.solutions_frame_Solutions_DevProt.get()
                concentration = self.solutions_frame_Solutions_Concentration.get()


                for _ in range(num_copies):
                    if not self.asset_numbers:
                        print("No asset numbers available for printing.")
                        return
                    asset_number = self.asset_numbers.pop(0)  # Get and remove the first asset number
                    text = f"{asset_number}\n{name}\n{concentration}mM\n{dev_prot}\nP: {prep_day}\nE: {exp_day}"
                    text_lines = text.split("\n")

                    img = self.generate_qr_with_text(text, text_lines, asset_number)

                    # Display the final image
                    img.show()

                    # Print the image
                    self.print_image(img)

            else:
                print("Invalid input. Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    
    def prompt_print_amount_antibody(self):
        # Get the value from the entry widget
        num_copies_str = self.antibody_frame_Insert_Amount.get()

        try:
            # Convert the value to an integer
            num_copies = int(num_copies_str)

            # Ensure it's a positive integer
            if num_copies > 0:
                # Generate and print QR codes for each asset number
                name = self.antibody_frame_Name.get()
                exp_day = self.antibody_frame_Exp_Date.get()
                prep_day = self.antibody_frame_Prep_Date.get()
                concentration = self.antibody_frame_Concentration.get()


                for _ in range(num_copies):
                    if not self.asset_numbers:
                        print("No asset numbers available for printing.")
                        return
                    asset_number = self.asset_numbers.pop(0)  # Get and remove the first asset number
                    text = f"{asset_number}\n{name}\n{concentration}mg/mL\nP: {prep_day}\nE: {exp_day}"
                    text_lines = text.split("\n")

                    img = self.generate_qr_with_text(text, text_lines, asset_number)

                    # Display the final image
                    img.show()

                    # Print the image
                    self.print_image(img)

            else:
                print("Invalid input. Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    def prompt_print_amount_adc(self):
        # Get the value from the entry widget
        num_copies_str = self.adc_frame_Insert_Amount.get()

        try:
            # Convert the value to an integer
            num_copies = int(num_copies_str)

            # Ensure it's a positive integer
            if num_copies > 0:
                # Generate and print QR codes for each asset number
                name = self.adc_frame_Name.get()
                exp_day = self.adc_frame_Exp_Date.get()
                prep_day = self.adc_frame_Prep_Date.get()
                dar = self.adc_frame_dar.get()
                concentration = self.adc_frame_Concentration.get()


                for _ in range(num_copies):
                    if not self.asset_numbers:
                        print("No asset numbers available for printing.")
                        return
                    asset_number = self.asset_numbers.pop(0)  # Get and remove the first asset number
                    text = f"{asset_number}\n{name}\n{concentration}mg/mL DAR:{dar}\nP: {prep_day}\nE: {exp_day}"
                    text_lines = text.split("\n")

                    img = self.generate_qr_with_text(text, text_lines, asset_number)

                    # Display the final image
                    img.show()

                    # Print the image
                    self.print_image(img)

            else:
                print("Invalid input. Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")



if __name__ == "__main__":
    app = LoginApp()
    app.title("Login")
    app.mainloop()
import customtkinter as ctk
from test import TypeTest
import random

WINDOW_PADDING = 20

class Ui:
    def __init__(self, test) -> None:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.window = ctk.CTk()
        self.window.title("Typing Test")
        self.window.geometry("600x400")
        self.current_word:str = ""
        self.test:TypeTest = test
        
        
        # MENU FRAME
        self.menu_frame = ctk.CTkFrame(master=self.window)
        self.menu_frame.pack(pady=40, padx=40, fill="both", expand=True)    
        self.title_label = ctk.CTkLabel(master=self.menu_frame, text="Typing Test", font=("Roboto", 36))
        self.title_label.pack(pady=30, padx=10)
        self.start_button = ctk.CTkButton(master=self.menu_frame, text="Start Typing test", command=self.run_test)
        self.start_button.pack(pady=10, padx=20)
        self.close_button = ctk.CTkButton(master=self.menu_frame, text="Close", command=self.quit)
        self.close_button.pack(pady=10, padx=20)
        
        # GAME FRAME
        self.game_frame = ctk.CTkFrame(master=self.window)
        self.display_label = ctk.CTkLabel(master=self.game_frame, text="LONGWORD", font=("Roboto", 46))
        self.display_label.pack(pady=20, padx=20, fill="both", expand=True)
        self.text_entry = ctk.CTkEntry(master=self.game_frame, width=50, font=("Roboto", 40), justify='center')
        self.text_entry.pack(pady=20, padx=20, fill="x", expand=True)
        
        # ENDSCREEN FRAME
        self.end_game_frame = ctk.CTkFrame(master=self.window)
        self.characters_label = ctk.CTkLabel(master=self.end_game_frame, 
                                             text= "Total written characters: 100",
                                             font=("Roboto", 24))
        self.characters_label.pack(pady=20, padx=20, fill="x", expand=True)
        self.cpm_label = ctk.CTkLabel(master=self.end_game_frame, text= "CPM: 0", font=("Roboto", 24))
        self.cpm_label.pack(pady=20, padx=20, fill="x", expand=True)
        self.incor_words_label = ctk.CTkLabel(master=self.end_game_frame,
                                              text= "Incorrect words: ",
                                              font=("Roboto", 18),
                                              wraplength=300)
        self.incor_words_label.pack(pady=20, padx=20, fill="x", expand=True)
        self.return_button = ctk.CTkButton(master=self.end_game_frame,
                                           text="Return to menu",
                                           command=self.return_to_menu)
        self.return_button.pack(pady=20, padx=20, fill="x", expand=True)
        
        self.frames = [self.menu_frame, self.game_frame, self.end_game_frame]
        self.test.fetch_texts()
        self.window.bind("<KeyRelease>", self.key_listener)
        self.window.mainloop()
    
    def show_frame(self, frame):
        for f in self.frames:
            if f == frame:
                f.pack(pady=20, padx=20, fill="both", expand=True)
            else:
                f.pack_forget()
    
    def return_to_menu(self):
        self.show_frame(self.menu_frame)
        self.test.reset_test()
                 
    def run_test(self):    
        self.show_frame(self.game_frame)
        self.text_entry.focus()  
        self.next_word()
        self.test.start_timer()
        
    def key_listener(self, event):
        if(self.test.test_is_on):
            if event.keysym == "Return":
                self.check_answer()
                
    def check_answer(self):
        self.test.check_word(self.text_entry.get(), self.current_word)
        self.text_entry.delete(0, "end")
        if self.test.time_left():
            self.next_word()
        else:
            results = self.test.get_results()
            self.characters_label.configure(text=f'Total written characters: {results["characters"]}')
            self.cpm_label.configure(text=f'CPM: {results["cpm"]:.2f}')
            self.incor_words_label.configure(text=f'Incorrect words:  {results["incorrect_words"]}')
            self.show_frame(self.end_game_frame)   
    
    def next_word(self):
        self.current_word = random.choice(self.test.text_data)
        self.display_label.configure(text=self.current_word)
    
    def quit(self):
        self.window.destroy()
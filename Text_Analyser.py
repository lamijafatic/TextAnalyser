#GLavni programm
import tkinter as tk
from tkinter import messagebox
import string
from collections import Counter
import time
from PIL import Image, ImageTk
import base64
import io
import re
from langdetect import detect
from tkinter import PhotoImage
from tkinter import scrolledtext
from tkinter import filedialog 
import requests
from bs4 import BeautifulSoup
global tk_image
global results_textbox
tekst_upload = ""
enter_text_globalno = None



def introduction_screen():  #screen which is displayed for several seconds at the begining

    def resize_and_align_image(image_path, width, height): #function for changing size of text analysis icon(image)
        original_image = Image.open(image_path)
        resized_image = original_image.resize((width, height))
        tk_image = ImageTk.PhotoImage(resized_image)
        
        return tk_image
    
    screen1 = tk.Tk()  #setting first/introduction screen
    screen1.title("Text Analyzer")
    screen1.geometry("400x300")   #  components of screen
    
    title_label = tk.Label(screen1, text="Text Analyzer", font=("Helvetica", 24, "bold"))
    title_label.pack(pady=10) #.pack() for placing widget inside of anything(neccesary)
    
    welcome_label = tk.Label(screen1, text="Welcome", font=("Arial", 18))
    welcome_label.pack(pady=10)
     
    tk_image = resize_and_align_image("ikona.png",100,100)#setting image
    
    label = tk.Label(screen1, image=tk_image)#image holding label(neccesary)
    label.image = tk_image
    label.pack() 

    screen1.update()#important because of timer
    def close_screen1():#function for closing this and opening new screen
        screen1.destroy()
        home_screen()

    screen1.after(4000, close_screen1)#after 4 seconds close this screen
 
    screen1.mainloop()#crucial

def home_screen(): #screen with menu options
    global screen2
    global enter_text_globalno
    screen2 = tk.Tk()
    screen2.title("Home page")
    screen2.geometry("400x300")
    background_image = PhotoImage(file="slova.gif")#background image of screen 2
    background_label = tk.Label(screen2, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)#place to fit screen
    title_label2 = tk.Label(screen2, text="Meni", font=("Helvetica", 24, "bold"))
    title_label2.pack(pady=10)       #components and its style
    title_label2.configure(bg="white", fg="black")  

    def enter_text():
        global tekst_upload
        global unos_text
        global results_textbox
        global background_image1
        global enter_screen
        
        screen2.destroy()
        enter_screen = tk.Tk()
        enter_screen.title("Text Analysis")
        enter_screen.geometry("800x600")
        enter_screen.configure(bg="lightblue")
        background_image1 = PhotoImage(file="slova2.gif")  
        background_label1 = tk.Label(enter_screen, image=background_image1)

        background_label1.image1 = background_image1
        background_label1.place(x=0, y=0,relwidth=1, relheight=1)
        main_frame = tk.Frame(enter_screen,bg="lightyellow")
        main_frame.pack(pady=10, padx=10)#making group of more elements

        unos_label = tk.Label(main_frame, text="Type/paste your text here:", font=("Helvetica", 15, "bold"),bg="lightyellow")
        unos_label.pack(pady=3,padx=10)
        unos_text = tk.Text(main_frame, height=10, width=70, font=("Arial", 10))
        unos_text.pack(side=tk.LEFT, padx=5)#text box
      
        if tekst_upload: #if there is already uploaded text,write it in the text box, if not make it empty
            unos_text.delete("1.0", tk.END)
            unos_text.insert("1.0", tekst_upload)
        tekst_upload = ""
           

        button_frame = tk.Frame(main_frame,bg="lightyellow")
        button_frame.pack(side=tk.RIGHT)
             #setting buttons with functions
        button_analyse = tk.Button(button_frame, text="ANALYSE", bg="white", fg="black", command=analyse_tekst, width=17,font=("Arial",11,"bold"))
        button_analyse.pack(side=tk.TOP,pady=15,padx=15)
        
        button_new_unos = tk.Button(button_frame, text="New text", bg="white", fg="black", command=new_unos, width=15)
        button_new_unos.pack(side=tk.TOP, padx=15,pady=5)
        
        button_save_unos = tk.Button(button_frame, text="Save text", bg="white", fg="black", command=save_unos, width=15)
        button_save_unos.pack(side=tk.TOP, padx=15,pady=5)
        
        main_frame2 = tk.Frame(enter_screen,bg="lightyellow")
        main_frame2.pack(pady=10, padx=10)
        
        results_label = tk.Label(main_frame2, text="Analysis Results:", font=("Helvetica", 15, "bold"),bg="lightyellow")
        results_label.pack(pady=3,padx=10) #results textbox:
        
        results_textbox = scrolledtext.ScrolledText(main_frame2, height=10, width=50, wrap=tk.WORD,font=("Arial",12))
        results_textbox.pack(side=tk.LEFT,pady=3,padx=10)
      
        button_history = tk.Button(enter_screen, text="History", command=show_history,bg="white",fg="black",width=10)
        button_history.pack(side=tk.LEFT, padx=15)
        
        button_saved = tk.Button(enter_screen, text="Saved", command=show_saved_words,bg="white",fg="black",width=10)
        button_saved.pack(side=tk.LEFT, padx=15)
        
        replace_frame=tk.Frame(main_frame2)
        replace_frame.pack(side=tk.RIGHT,pady=10,padx=10)
        
        label_wordt=tk.Label(replace_frame,text="Replace words",font=("Arial",12,"bold"))
        label_wordt.pack(pady=20,padx=10)
        
        label_word = tk.Label(replace_frame, text="Replacing word:",font=("Arial",10))
        label_word.pack(pady=7)

        global entry_word #existing word
        entry_word=tk.Entry(replace_frame)
        entry_word.pack(pady=7)
            #new word
        label_new_word = tk.Label(replace_frame, text="New word:",font=("Arial",10))
        label_new_word.pack(pady=7)
        global entry_new_word
        entry_new_word=tk.Entry(replace_frame)
        entry_new_word.pack(pady=7)
        button_replace = tk.Button(replace_frame, text="REPLACE", command=replace_word,font=("Arial",10,"bold"))
        button_replace.pack(pady=7)
    enter_text_globalno = enter_text #picking this variable into global one for further use
    
    
    def replace_word(): #function for word replacing
        new_tekst=""
        tekst = unos_text.get("1.0", tk.END) #read input text
        word_for_replace = entry_word.get() #read entry word
        new_word = entry_new_word.get() #read new word
        
        if word_for_replace not in tekst: #if word does not exit in text,display error
            messagebox.showinfo("Warning", f"Word '{word_for_replace}' does not exist in text.")
            return
        
        new_tekst = tekst.replace(word_for_replace, new_word)#function for replace
        unos_text.delete("1.0", "end")
        unos_text.insert("1.0", new_tekst)
        tekst=new_tekst
  
    def exit():  #exit option
        screen2.destroy()
    
     #other buttons in program
    button_unesi_text = tk.Button(screen2, text="Enter text",bg="white", fg="black", command=enter_text,width=15)
    button_unesi_text.pack(side=tk.TOP, pady=10,)

    button_upload = tk.Button(screen2, text="Upload from file",bg="white", fg="black", command=upload_file,width=15)
    button_upload.pack(side=tk.TOP, pady=10)

    button_url = tk.Button(screen2, text="Upload from URL",bg="white", fg="black", command=url_text,width=15)
    button_url.pack(side=tk.TOP, pady=10)
   
    button_exit = tk.Button(screen2, text="Exit",bg="white", fg="black", command=exit,width=15)
    button_exit.pack(side=tk.TOP, pady=10)
    screen2.mainloop()
    
   
def analyse_tekst(): #main function for analysing text
    results_textbox.delete("1.0", tk.END)
    tekst = unos_text.get("1.0", tk.END)

    with open("uneseni_tekst.txt", "a",encoding='utf-8') as f:  #save text to history file
        f.write(tekst)
        f.write("\n\n")
    if not tekst.strip(): #if it is empty
        results_textbox.insert(tk.END,"Please enter text")
    else:
        
        slova=["a","b","c","č","ć","d","dž","đ","e","f","g","h","i","j","k","l","lj","m","n","nj","o","p","r","s","š","t","u","v","z","ž"]

        def number_words(): #number of words
            return len(tekst.split())

        def number_sentences(): #number of sentences

            if not tekst:
                return 0  
            number_sentences = 0
            u_recenici = False  #are we inside sentence
            for znak in tekst:

                 if znak in ['.', '?', '!']:
                    if not u_recenici:

                        number_sentences += 1
                    u_recenici = True
                 else:
                    u_recenici = False

            return number_sentences


        def number_letters():
            number_letters=0
            for c in tekst:
                for i in range(len(slova)):
                    if c==slova[i]:
                        number_letters+=1
                        break
            return number_letters
        
        def number_karaktera_spaces():
            return len(str(tekst))-1
            
        def number_karaktera():
            number_karaktera=0
            for i in range(len(str(tekst))):
                if tekst[i]!=" ":
                    number_karaktera+=1
            return number_karaktera-1
            
        def specijalni():
            karakteri=['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '<', '>', '?', '.', ',', ':', ';', "'", '"', '\\', '|', '[', ']', '{', '}', '~', '`']
            numberac=0
            for znak in tekst:
                if znak in karakteri:
                    numberac+=1
            return numberac
        
        def vowels():
            vowels=['a','e','i','o','u']
            numberac=0
            for letter in tekst:
                if letter in vowels:
                    numberac+=1
            return numberac

        def numbers():
            numbers=['1','2','3','4','5','6','7','8','9','0']
            numberac=0
            for letter in tekst:
                if letter in numbers:
                    numberac+=1
            return numberac
       
        def longest_word():
            words=(tekst.lower()).split()
            length=0
            longest=""
            for word in words:
                if len(word)>length:
                    longest=str(word)
                    length=len(word)
            return longest
        
        def shortest_word():
            words=(tekst.lower()).split()
            length=len(words[0])
            shortest=words[0]
            for word in words:
                if len(word)<length:
                    shortest=str(word)
                    length=len(word)
            return shortest
            
                    
                    
                
        def average_length():
            words = tekst.split()
            number_words = len(words)
            if number_words == 0:
                return 0 

            ukupna_length = sum(len(word) for word in words)
            average_length = round(ukupna_length / number_words,2)

            return average_length

    
        #language detection
        try:
            language = detect(tekst)
        except Exception as e:
            print(f"Error detecting language: {e}")
            language = "N/A"

        tekst = tekst.lower()
        words =tekst.split()
        duplikati = set(word for word in words if words.count(word) > 1) #double words
        
        dict = {}  #table with letters and repetition number

        for letter in tekst:
            if letter in slova:
                dict[letter] = tekst.count(letter)
        for letter in slova:

            if letter not in dict:
                dict[letter] = 0

        
        def most_common_word(tekst):
            most_common=""
            words = tekst.split()
            numberac_words = {}
            for word in words:
                word = word.lower()
        

                if word in numberac_words:
                    numberac_words[word] += 1
                else:
                    numberac_words[word] = 1
            
            most_common_number = 0
    
            for word, number in numberac_words.items():
                if number > most_common_number:
                    most_common = word
                    most_common_number = number
    
            return most_common
    
    
        def repetition_words():
            dict2={}
            words=tekst.split()
            
            for word in set(words):
                word=word.lower()
                dict2[word] = words.count(word)
            sortirano_dict =sorted(dict2.items(), key=lambda x: x[1], reverse=True)
            return sortirano_dict

      


        results = (
            f"number of words: {number_words()}\n",
            f"The longest word: {longest_word()}\n",
            f"The shortest word: {shortest_word()}\n",
            f"number of sentences: {number_sentences()}\n",
            f"number of letters: {number_letters()}\n",
            f"number of numbers:{numbers()}\n",
            f"Vowels: {vowels()}\n",
            f"Average word lenght:{average_length()}\n",
            f"number of special characters: {specijalni()}\n",
            f"number of characters(with spaces):{number_karaktera_spaces()}\n",
            f"number of characters(without spaces):{number_karaktera()}\n",
            "Letter repetition:"
         
        )
        for letter, number in dict.items():
            if number!=0:
                results += (f"\n{letter}: {number}",)
        results += (
            f"\nMost common word: {most_common_word(tekst)}\n ",
            f"Double words:\n {', '.join(duplikati)}\n",
            "Words repetition:"   )
        for word,number in repetition_words():
            if number>2:
                results+= (f"\n{word}:{number} times",)
            
        results+= (
            f"\nLanguage of text: {language}",
        )
        formatted_results = ' '.join(results)#tuple to string
 
       
        results_textbox.delete("1.0", tk.END)  

        results_textbox.insert(tk.END, formatted_results) #display results in the output text box
        
        
               
def upload_file():
    def continue_():
        enter_text_globalno() #enter text from file to our textbox from main screen
        screen_file.destroy()
        

    
    def upload():
        global tekst_upload

        try:

            file_path = filedialog.askopenfilename() #opening file dialog
            if file_path:
                with open(file_path, "r", encoding="utf-8") as file: #reading file
                    tekst_upload = file.read()
                    text_box.delete("1.0", "end")
                    text_box.insert("1.0", tekst_upload)
        except Exception as e:

            messagebox.showinfo("Error while reading file",f"{str(e)}")

# screen
    screen_file = tk.Tk()
    screen_file.title("Upload from file")


    text_box = tk.Text(screen_file, height=7, width=30)
    text_box.pack()


# button
    button_upload = tk.Button(screen_file, text="upload File", command=upload)
    button_upload.pack(pady=5)
    button_dalje = tk.Button(screen_file, text="Continue", command=continue_)
    button_dalje.pack(pady=5)



def new_unos():
    unos_text.delete("1.0", tk.END)
    results_textbox.delete("1.0", tk.END)  #new text

def save_unos():
    tekst = unos_text.get("1.0", tk.END)   #save text
    with open("saved.txt", "a",encoding='utf-8') as f:
        f.write(tekst)
        f.write("\n\n")
                                
def url_text():
    def nastavak(): #continue
        enter_text_globalno()
        url_screen.destroy() 
    
    def link(url):
        global tekst_upload
        try:
            response = requests.get(url)
            response.raise_for_status()  #getting url
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            tekst_upload = soup.get_text()  #reading text 
            unos_url.delete("1.0", tk.END)  
            unos_url.insert(tk.END, tekst_upload)  
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error while reading from URL",f" {str(e)}")

#screen
    url_screen = tk.Tk()
    url_screen.title("Upload from URL")

    unos_url = tk.Text(url_screen, height=10, width=40)
    unos_url.pack(pady=20)

    unos_url_box = tk.Entry(url_screen, width=40)
    unos_url_box.pack()

    def upload_sa_url():
        url = unos_url_box.get()
        link(url)

    button_upload = tk.Button(url_screen, text="Upload from URL", command=upload_sa_url)
    button_upload.pack()
    button_nastavak = tk.Button(url_screen, text="Continue", command=nastavak)
    button_nastavak.pack()


def show_history():     #history list
    
    try:
        with open("uneseni_tekst.txt", "r",encoding='utf-8') as f: #from file
            sadrzaj = f.read()
        
        new_prozor = tk.Toplevel()   #as child screen
        new_prozor.title("History of entered text")

        text_widget = scrolledtext.ScrolledText(new_prozor, wrap=tk.WORD, width=40, height=10)
        text_widget.pack(padx=10, pady=10)
        text_widget.insert(tk.END, sadrzaj)

    except FileNotFoundError:
        messagebox.showinfo("No available history.")
       
def show_saved_words():
    try:
        with open("saved.txt", "r") as f: #open from file
            tekst3 = f.read()
            
            new_prozor = tk.Toplevel(enter_screen) #new child screen
            new_prozor.title("Saved text")

            text_widget = scrolledtext.ScrolledText(new_prozor, wrap=tk.WORD, width=40, height=10)
            text_widget.pack(padx=10, pady=10)
            text_widget.insert(tk.END,tekst3)
           

    except FileNotFoundError:
        messagebox.showinfo("No saved text.")
            

introduction_screen()
home_screen()
#activating first screen &come back to home screen

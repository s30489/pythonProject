import string
from tkinter import *
import random

hangman_color = "black"

class GameState:
    def __init__(self):
        self.word = ""
        self.guessed_letters = []
        self.lives = 0
        self.letters = list(string.ascii_lowercase)
        self.paused = False
        self.started = False
        self.visible_parts = []

    def load_words(self):
        try:
            with open("HangmanWords.txt") as f:
                return f.read().split(",")
        except FileNotFoundError:
            return print("Nie znaleziono pliku")

    def start_new_game(self):
        words = self.load_words()
        self.word = random.choice(words).strip()
        self.guessed_letters = []
        self.lives = 0
        self.letters = list(string.ascii_lowercase)
        self.started = True
        self.paused = False
        self.visible_parts = []

root = Tk()
root.title("Hangman")
root.geometry("1000x550")
root.resizable(False, False)


game_state = GameState()
hangman_parts = []
current_part_index = 0
canvas = None
letter_entry = None


def menu():
    clear_window()
    frame = Frame(root, bg="black")
    frame.pack(fill="both", expand=True)

    image = PhotoImage(file="HangManBackround.png")
    frame.background_image = image

    bg_label = Label(frame, image=image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    Button(frame, text="Play", width=20, command=start_game).pack(pady=20)
    Button(frame, text="Options", width=20, command=options_menu).pack(pady=20)
    Button(frame, text="Quit", width=20, command=root.destroy).pack(pady=20)

def options_menu():
    clear_window()
    frame = Frame(root, bg="blue")
    frame.pack(fill="both", expand=True)

    Label(frame, text="Kolor ludzika:", bg="blue", fg="white", font=("Arial", 16)).pack(pady=20)
    color_var = StringVar(value="black")

    def choose_color():
        global hangman_color
        hangman_color = color_var.get()

    OptionMenu(frame, color_var, "black", "red", "blue", "green").pack(pady=10)
    Button(frame, text="Zapisz opcje", command=choose_color).pack(pady=10)
    Button(frame, text="Wróć do menu", command=menu).pack(pady=30)

def start_game():
    game_state.start_new_game()
    game()

def game():
    clear_window()
    frame = Frame(root, bg="turquoise")
    frame.pack(fill="both", expand=True)

    letters_label = Label(frame, text="", font=("Arial", 18), bg="turquoise", justify="center")
    letters_label.place(x=200, y=150)

    global canvas, hangman_parts, current_part_index, letter_entry
    current_part_index = 0
    canvas = Canvas(frame, width=400, height=400, bg="white")
    canvas.place(x=550, y=100)
    setup_hangman_canvas()
    redraw_hangman()

    def guess_letter(letter):
        if letter and letter.isalpha() and len(letter) == 1:
            letter = letter.lower()
            if letter in game_state.guessed_letters:
                return
            if letter in game_state.word:
                game_state.guessed_letters.append(letter)
            else:
                game_state.guessed_letters.append(letter)
                game_state.lives += 1
                reveal_next_part()
            update_game_screen()

    def update_game_screen():
        display = ' '.join([c if c in game_state.guessed_letters else '_' for c in game_state.word])
        word_label.config(text=display)
        if set(game_state.word).issubset(set(game_state.guessed_letters)):
            end_screen("Wygrałeś")
        elif game_state.lives >= len(hangman_parts):
            end_screen("Przegrałeś")

    def update_letters_display():
        letters_left = [letter if letter not in game_state.guessed_letters else ' ' for letter in game_state.letters]
        first_row = ' '.join(letters_left[:13])
        second_row = ' '.join(letters_left[13:])
        letters_label.config(text=f"{first_row}\n{second_row}")


    word_label = Label(frame, text="", font=("Arial", 24), bg="turquoise")
    word_label.place(x=300, y=50)
    update_game_screen()

    letter_entry = Entry(frame, font=("Arial", 16), width=5)
    letter_entry.place(x=300, y=100)
    letter_entry.focus()

    def on_enter(event):
        guess_letter(letter_entry.get())
        letter_entry.delete(0, END)
        update_letters_display()

    letter_entry.bind("<Return>", on_enter)
    update_letters_display()

    Button(frame, text="Pause", command=pause).place(x=10, y=10)

def setup_hangman_canvas():
    global hangman_parts
    hangman_parts = [
        canvas.create_line(50, 350, 100, 300, fill=hangman_color, width=3, state='hidden'),
        canvas.create_line(150, 350, 100, 300, fill=hangman_color, width=3, state='hidden'),
        canvas.create_line(100, 300, 100, 150, fill=hangman_color, width=3, state='hidden'),
        canvas.create_line(100, 150, 200, 150, fill=hangman_color, width=3, state='hidden'),
        canvas.create_line(100, 190, 140, 150, fill=hangman_color, width=3, state='hidden'),
        canvas.create_line(200, 150, 200, 180, fill=hangman_color, width=3, state='hidden'),
        canvas.create_oval(180, 180, 220, 220, outline=hangman_color, width=3, state='hidden'),
        canvas.create_line(200, 220, 200, 280, fill=hangman_color, width=3, state='hidden'),
        canvas.create_line(200, 230, 180, 270, fill=hangman_color, width=3, state='hidden'),
        canvas.create_line(200, 230, 220, 270, fill=hangman_color, width=3, state='hidden'),
        canvas.create_line(200, 280, 180, 320, fill=hangman_color, width=3, state='hidden'),
        canvas.create_line(200, 280, 220, 320, fill=hangman_color, width=3, state='hidden'),
    ]

def reveal_next_part():
    global current_part_index
    if current_part_index < len(hangman_parts):
        canvas.itemconfigure(hangman_parts[current_part_index], state='normal')
        game_state.visible_parts.append(current_part_index)
        current_part_index += 1

def redraw_hangman():
    for i in game_state.visible_parts:
        canvas.itemconfigure(hangman_parts[i], state='normal')

def pause():
    game_state.paused = True
    clear_window()
    frame = Frame(root, bg="red")
    frame.pack(fill="both", expand=True)

    Button(frame, text="Kontynuuj", command=resume_from_pause).pack(pady=20)
    Button(frame, text="Zakończ grę", command=reset_to_menu).pack(pady=20)

def resume_from_pause():
    game_state.paused = False
    game()

def reset_to_menu():
    global game_state
    game_state = GameState()
    menu()

def end_screen(result_text):
    clear_window()

    bg_color = "darkgreen" if "Wygrałeś" in result_text else "darkred"

    frame = Frame(root, bg=bg_color)
    frame.pack(fill="both", expand=True)

    Label(frame, text=result_text, font=("Arial", 32), fg="white", bg=bg_color).pack(pady=20)

    word_reveal = f"Słowo to: {game_state.word}"
    Label(frame, text=word_reveal, font=("Arial", 24), fg="white", bg=bg_color).pack(pady=10)

    Button(frame, text="Zagraj ponownie", command=start_game).pack(pady=20)
    Button(frame, text="Wróć do menu", command=reset_to_menu).pack(pady=20)


def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

root.call('wm', 'iconphoto', root._w, PhotoImage(file='HangmanIcon.png'))
menu()
root.mainloop()



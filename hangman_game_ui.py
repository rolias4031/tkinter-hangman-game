import string
import tkinter as tk
from tkinter import ttk

class WindowMain(tk.Tk):
    """
    root window that holds all other frames.
    has two funcs(), next_page() and var_refresh().
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        style = ttk.Style(self)

        self.columnconfigure(0, weight=1)
        self.geometry("400x300")
        self.frames = dict() #create a dict that we can use to cycle through FrameClass creation

        container = ttk.Frame() #container that holds all frames inside of WindowMain()
        container.grid(row=0, column=0)

        #initialize frame classes using a loop, stores them in dict()
        for FrameClass in (StartPage, SettingsPage, WordPage, GamePage):
            frame = FrameClass(container, self, style)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        self.next_page(StartPage) #raises StartPage to begin program

        print(self.frames)
        print(StartPage)
        print(self.frames[StartPage])

    def next_page(self, page, *args):
        """
        raises the next page in the game flow. takes page and finds the class in frames, then raises that frame.
        """
        if page == SettingsPage: #condition to reset all variables at each new round when SettingsPage is raised
            self.var_refresh()
        frame = self.frames[page]
        self.bind_func(page)
        frame.tkraise()

    def bind_func(self, page, *args):

        #bind update_Word_Picker
        if page == SettingsPage:
            self.bind("<Return>", lambda event, controller=self: SettingsPage.update_Word_Picker(controller, event))

        #bind WordPage_func
        elif page == WordPage:
            self.bind("<Return>", lambda event, controller=self: WordPage.WordPage_func(controller, event))

        #bind GamePage_func
        elif page == GamePage:
            self.bind("<Return>", lambda event, controller=self: GamePage.GamePage_func(controller, event))

    def var_refresh(self):
        """
        manually resets all vars for new round. I know this is probably not the most efficient way to do this.
        """
        StartPage.gameover_message_one.set("")
        StartPage.gameover_message_two.set("")
        SettingsPage.word_picker.set("")
        SettingsPage.word_guesser.set("")
        SettingsPage.error_message.set("")
        SettingsPage.enter_word_message.set("")
        WordPage.game_word.set("")
        WordPage.error_message_wordpage.set("")
        WordPage.word_blank.set("")
        WordPage.word_blank_mirror.clear()
        GamePage.letters_guessed.set("")
        GamePage.letters_guessed_mirror.clear()
        SettingsPage.guesses_left.set(5)
        GamePage.player_guess.set("")
        GamePage.error_message_gamepage.set("")
        GamePage.correct_ans.set("")

class StartPage(ttk.Frame):

    """
    StartPage does 1 thing: asks the user if they want to play a game or quit.
    Using the button calls next_page(SettingsPage) to move on to settings.
    """

    def __init__(self, container, controller, style, **kwargs):
        super().__init__(container, **kwargs)

        StartPage.gameover_message_one = tk.StringVar()
        StartPage.gameover_message_two = tk.StringVar()

        self.columnconfigure((0,1), weight=1)
        self.rowconfigure((0), minsize=60)
        self.rowconfigure((1), minsize=10)

        #styles for widgets used throughout the program
        style.configure("ButtonGeneral.TButton", font=("IBM Plex Sans", 13))
        style.configure("DisplayGeneral.TLabel", font=("IBM Plex Sans Light", 15))
        style.configure("WordBlank.TLabel", font=("IBM Plex Sans", 22))
        style.configure("LabelGeneral.TLabel", font=("IBM Plex Sans Medium", 15))
        style.configure("LabelError.TLabel", foreground="red", font=("IBM Plex Sans Condensed", 13))
        style.configure("LabelCorrect.TLabel", foreground="Green", font=("IBM Plex Sans Condensed", 13))
        style.configure("EntryGeneral.TEntry", font=("IBM Plex Sans Medium", 15))

        gameover_message_label_one = ttk.Label(self, style="LabelGeneral.TLabel", textvariable=StartPage.gameover_message_one)
        gameover_message_label_two = ttk.Label(self, style="LabelGeneral.TLabel", textvariable=StartPage.gameover_message_two)
        play_button = ttk.Button(self, text="Play Hangman", command=
                                 lambda: controller.next_page(SettingsPage))
        quit_button = ttk.Button(self, text="Quit", command=controller.destroy)

        gameover_message_label_one.grid(row=0, column=0, columnspan=2, sticky="S")
        gameover_message_label_two.grid(row=1, column=0, columnspan=2, sticky="S")
        play_button.grid(row=2, column=0, sticky="E", padx=10, pady=30)
        quit_button.grid(row=2, column=1, sticky="W", padx=10, pady=30)

        print(play_button.winfo_class())

        for button in [play_button, quit_button]:
            button["style"] = "ButtonGeneral.TButton"

class SettingsPage(ttk.Frame):

    """
    SettingsPage does 3 things:
    1. takes the names for each player (Player 1 & 2 are the default)
    2. designates which player will be choosing the word via radiobutton selection
    3. assigns the player names to a few internal variables that need to know which player is choosing and which is guessing.
    """

    def __init__(self, container, controller, style, **kwargs):
        super().__init__(container, **kwargs)

        #all SettingsPage variables as class variables.
        SettingsPage.player_one_name = tk.StringVar(value="Player 1")
        SettingsPage.player_two_name = tk.StringVar(value="Player 2")
        SettingsPage.word_picker = tk.StringVar()
        SettingsPage.word_guesser = tk.StringVar()
        SettingsPage.error_message = tk.StringVar()
        SettingsPage.enter_word_message = tk.StringVar()
        SettingsPage.guesses_left = tk.IntVar(value=5)

        self.rowconfigure((0,4), minsize=60)
        self.rowconfigure((1,2,3,5), minsize=30)
        self.columnconfigure((0,1), minsize=150)

        #creating all widgets in SettingsPage in order of appearance
        player_names_label = ttk.Label(self, text="Player Names")
        player_one_entry = ttk.Entry(self, width=15, textvariable=SettingsPage.player_one_name)
        player_two_entry = ttk.Entry(self, width=15, textvariable=SettingsPage.player_two_name)
        guesses_label = ttk.Label(self, style="LabelGeneral.TLabel", text="Guesses:")
        guesses_entry = tk.Spinbox(
            self,
            width=3,
            textvariable=SettingsPage.guesses_left,
            from_=5,
            to=15,
            wrap=True)

        select_label = ttk.Label(self, text="Word Picker")

        select_one = ttk.Radiobutton(
            self,
            text="",
            variable=SettingsPage.word_picker,
            value="Player 1")

        select_two = ttk.Radiobutton(
            self,
            text="",
            variable=SettingsPage.word_picker,
            value="Player 2")

        confirm_settings_button = ttk.Button(self, style="ButtonGeneral.TButton", text="Confirm Settings", command=lambda:
                                             SettingsPage.update_Word_Picker(controller))

        error_message_label_settings = ttk.Label(self, style="LabelError.TLabel", textvariable = SettingsPage.error_message)

        for label in [player_names_label, select_label]:
            label["style"] = "LabelGeneral.TLabel"

        for field in [player_one_entry, player_two_entry]:
            field["style"] = "EntryGeneral.TEntry"


        #grid placements for all widgets in SettingsPage
        player_names_label.grid(row=0, column=0, sticky="WS")
        player_one_entry.grid(row=1, column=0, sticky="EWS")
        player_two_entry.grid(row=2, column=0, sticky="EWS")
        select_label.grid(row=0, column=1, sticky="S")
        select_one.grid(row=1, column=1)
        select_two.grid(row=2, column=1)
        guesses_label.grid(row=3, column=0, sticky="WS")
        guesses_entry.grid(row=3, column=0, sticky="ES")
        confirm_settings_button.grid(row=4, column=0, columnspan=2, sticky="S")
        error_message_label_settings.grid(row=5, column=0, columnspan=2, sticky="S")

    def update_Word_Picker(controller, *args):
        """
        - assigns player names to their sides based on radiobutton selection, creates a message from them, then calls next page. throws an error message if a radiobutton isn't selected.
        - tied to confirm_settings_button
        """
        if SettingsPage.word_picker.get() == "Player 1":
            SettingsPage.word_picker.set(SettingsPage.player_one_name.get()) #set word_picker equal to player name selected.
            SettingsPage.word_guesser.set(SettingsPage.player_two_name.get()) #set word_guesser equal to other player
            name = SettingsPage.word_picker.get()
            message = name + ", enter your word"
            SettingsPage.enter_word_message.set(message)

            controller.next_page(WordPage)
            WordPage.enter_word_entry.focus()


        elif SettingsPage.word_picker.get() == "Player 2": #same logic, but flipped for player 2.
            SettingsPage.word_picker.set(SettingsPage.player_two_name.get())
            SettingsPage.word_guesser.set(SettingsPage.player_one_name.get())
            name = SettingsPage.word_picker.get()
            message = name + ", enter your word"
            SettingsPage.enter_word_message.set(message)

            controller.next_page(WordPage)
            WordPage.enter_word_entry.focus()

        else:
            SettingsPage.error_message.set("Select which player will pick the word")

class WordPage(ttk.Frame):

    """
    WordPage does 3 things:
    1. asks the word_picker for a game_word, checks the validity of game_word
    2. stores that word
    3. creates the word_blanks, one to be used for display on GamePage and the other for internal operations
    """

    def __init__(self, container, controller, style, **kwargs):
        super().__init__(container, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,2,3), minsize=60)
        self.rowconfigure((4), minsize=30)

        WordPage.game_word = tk.StringVar()
        WordPage.alphabet = tk.StringVar(value=string.ascii_lowercase.upper())
        WordPage.error_message_wordpage = tk.StringVar(value="x")
        WordPage.word_blank = tk.StringVar()
        WordPage.word_blank_mirror = []

        enter_word_label_one = ttk.Label(self, style="LabelGeneral.TLabel", textvariable=SettingsPage.enter_word_message)
        enter_word_label_two = ttk.Label(self, style="LabelGeneral.TLabel", text="Keep it hidden")
        WordPage.enter_word_entry = ttk.Entry(self, width=20, textvariable=WordPage.game_word)
        confirm_word_button = ttk.Button(self, width=10, style="ButtonGeneral.TButton", text="Confirm Word", command=
                                         lambda: WordPage.WordPage_func(controller))
        error_message_label_wordpage = ttk.Label(self, style="LabelError.TLabel", textvariable = WordPage.error_message_wordpage)

        enter_word_label_one.grid(row=0, column=0, sticky="S")
        enter_word_label_two.grid(row=1, column=0, sticky="S")
        WordPage.enter_word_entry.grid(row=2, column=0, sticky="S")
        confirm_word_button.grid(row=3, column=0, sticky="S")
        error_message_label_wordpage.grid(row=4, column=0, sticky="S")


    def WordPage_func(controller, *args):
        """
        - checks validity of entered word. if not valid, throws an error message to a label and does nothing. if valid, creates a word blank using create_word_blank() and raises GamePage. if player hits button without entering anything, throws another error and does nothing.
        - requires controller parameter to use next_page()
        - tied to confirm_word_button
        """
        if len(WordPage.game_word.get()) > 1:
            word = WordPage.game_word.get().upper()
            for letter in word:
                if letter not in WordPage.alphabet.get():
                    WordPage.error_message_wordpage.set("Your word can only contain letters") #error message
                    return

            WordPage.create_word_blank(word) #creates word blank for display and internal operations
            controller.next_page(GamePage) #raises GamePage
            GamePage.player_guess_entry.focus()

        else:
            WordPage.error_message_wordpage.set("Enter a word at least 2 letters long") #error message
            return

    def create_word_blank(game_word):
        """
        - creates two word blanks from the game_word, one for display and the other for game operations.
        - there are two because I couldn't find an easy way to convert StringVar() contents from a string to a list. Each time you .set() and .get() the word_blank to update it, the list characters are interpreted as a string. By using two, a word_blank and word_blank_mirror, we can do all the manipulations with the mirror and then .set(word_blank_mirror) without needing to .get() from the original.
        """
        WordPage.word_blank.set(["_" for i in range(0, len(game_word))]) #used for display
        WordPage.word_blank_mirror = ["_" for i in range(0, len(game_word))] #used for operations
        return

class GamePage(ttk.Frame):
    """
    GamePage does X things:
    1. takes a guess from the guesser and passes it to check_player_guess()
    2. check_player_guess() checks validity and if its a correct or incorrect guess
        a. if guess is invalid, throws and error message and does nothing
        b. correct guesses update the word_blank and get added to letters_guessed
        c. wrong guesses subtract 1 from guesses_left and get added to letters_guessed
    3. after each guessing round, game_over_check() checks if a player has won. This happens when guesses_left = 0 or the word_blank = game_word.
    4. two gameover_messages are created, the StartPage is recalled, and these messages are displayed there declaring the winner.
    """

    def __init__(self, container, controller, style, **kwargs):
        super().__init__(container, **kwargs)

        #variables with "_mirror" suffix are used to get around .get() complications. _mirror vars are used in program operations, and then passed to .set() for display to the UI.
        GamePage.letters_guessed = tk.StringVar()
        GamePage.letters_guessed_mirror = []
        GamePage.player_guess = tk.StringVar()
        GamePage.error_message_gamepage = tk.StringVar()
        GamePage.correct_ans = tk.StringVar()

        self.columnconfigure((0,1), minsize=150)
        self.rowconfigure((0,4), minsize=60)
        self.rowconfigure((1,2,3,5), minsize=30)

        #all widgets in the GamePage
        letters_guessed_label = ttk.Label(self, style="LabelGeneral.TLabel", text="Letters Guessed")
        letters_guessed_display = ttk.Label(self, style="DisplayGeneral.TLabel", textvariable=GamePage.letters_guessed)
        guesses_left_label = ttk.Label(self, style="LabelGeneral.TLabel", text="Guesses left")
        guesses_left_display = ttk.Label(self, style="DisplayGeneral.TLabel", textvariable=SettingsPage.guesses_left)
        player_guess_label = ttk.Label(self, style="LabelGeneral.TLabel", text="Guess a letter:")
        GamePage.player_guess_entry = ttk.Entry(self, width=2, textvariable=GamePage.player_guess)
        word_blank_display = ttk.Label(self, style="WordBlank.TLabel", textvariable=WordPage.word_blank)
        # ----- separating for visibility - has most of functionality
        player_guess_submit = ttk.Button(self, width=7, style="ButtonGeneral.TButton", text="Submit", command=
                                         lambda: GamePage.GamePage_func(controller))
        # -----
        GamePage.error_label_gamepage_one = ttk.Label(self, style="LabelError.TLabel", textvariable=GamePage.error_message_gamepage)
        GamePage.error_label_gamepage_two = ttk.Label(self, style="LabelCorrect.TLabel", textvariable=GamePage.correct_ans)

        #placement of all widgets in GamePage
        letters_guessed_label.grid(row=0, column=0, sticky="WS")
        letters_guessed_display.grid(row=1, column=0, sticky="WS")
        player_guess_label.grid(row=0, column=1, sticky="WS")
        GamePage.player_guess_entry.grid(row=1, column=1,sticky="WS")
        player_guess_submit.grid(row=1, column=1, sticky="ES")
        guesses_left_label.grid(row=2, column=0, sticky="WS")
        guesses_left_display.grid(row=3, column=0, sticky="WS")
        word_blank_display.grid(row=4, column=0, columnspan=3, sticky="S")
        GamePage.error_label_gamepage_one.grid(row=5, column=0, columnspan=3, sticky="S")
        GamePage.error_label_gamepage_two.grid(row=5, column=0, columnspan=3, sticky="S")

    def GamePage_func(controller, *args):
        """
        - parent function that calls two other functions: check_player_guess() and next_page().
        - tied to player_guess_submit button
        """
        game_end = False
        game_end = GamePage.check_player_guess() #returns True when a player wins

        if game_end == True:
            controller.next_page(StartPage) #recalls StartPage when a player wins

    def check_player_guess():

        """
        handles all core game functionality in these steps:
        1. checks if player_guess is valid (exactly 1 letter in the alphabet that hasn't been guessed before)
        2. if valid, checks if player_guess is or is not in the game_word
            a. if it is:
                1. calls mark_guess() to record that guess;
                2. calls update_word_blank() to update both word_blanks;
                3. calls gameover_check_correct() to check for a win
            b. if not:
                1. calls mark_guess();
                2. calls update_guesses_left() to subtract 1 guess;
                3. calls gameover_check_wrong to check for loss

        this process repeats until one of the gameover_check functions returns game_end = True
        """

        word = WordPage.game_word.get().upper() #get the game_word as word
        guess = GamePage.player_guess.get().upper() #get the player_guess as guess

        #initial validity check of player_guess
        if (len(guess) == 0) or (len(guess) > 1) or (guess not in WordPage.alphabet.get()) or (guess in GamePage.letters_guessed.get()):

            GamePage.error_label_gamepage_two.grid_forget()
            GamePage.error_label_gamepage_one.grid(row=5, column=0, columnspan=3, sticky="S")
            GamePage.error_message_gamepage.set("Guess failed. Must be a single letter you've yet to guess.")

        elif guess in word:
            GamePage.mark_guess(guess) #append guess to letters_guessed
            GamePage.update_word_blank(guess, word) #updates both word blanks
            GamePage.error_label_gamepage_one.grid_forget()
            GamePage.error_label_gamepage_two.grid(row=5, column=0, columnspan=3, sticky="S")
            GamePage.correct_ans.set("CORRECT") #informs users that guess was correct
            GamePage.error_message_gamepage.set("")
            GamePage.player_guess.set("") #resets player_guess_entry
            GamePage.player_guess_entry.focus() #rehighlights guess entry field
            game_end = GamePage.gameover_check_correct(word) #checks for win
            return game_end

        elif guess not in word:
            GamePage.mark_guess(guess)
            GamePage.update_guesses_left() #decrements guesses_left
            GamePage.error_label_gamepage_two.grid_forget()
            GamePage.error_label_gamepage_one.grid(row=5, column=0, columnspan=3, sticky="S")
            GamePage.error_message_gamepage.set("WRONG") #informs users of wrong guess
            GamePage.correct_ans.set("")
            GamePage.player_guess.set("")
            GamePage.player_guess_entry.focus()
            game_end = GamePage.gameover_check_wrong(word) #checks for loss
            return game_end

    def mark_guess(guess):
        """
        - called in check_player_guess()
        - takes player_guess and appends to letters_guessed_mirror, which gets .set() to letters_guessed for UI.
        """
        GamePage.letters_guessed_mirror.append(guess)
        GamePage.letters_guessed.set(GamePage.letters_guessed_mirror)

    def update_word_blank(guess, word):
        """
        - called in check_player_guess()
        - updates both word blanks. cycles through each letter in game_word by index. word_blank_mirror gets .set() to word_blank. requires both the player_guess and game_word
        """
        for i in range(0, len(word)):
            if word[i] == guess:
                WordPage.word_blank_mirror[i] = guess

        WordPage.word_blank.set(WordPage.word_blank_mirror)

    def update_guesses_left():
        """
        - called in check_player_guess()
        - decrements guesses_left by 1
        """
        num = SettingsPage.guesses_left.get()
        num = num - 1
        SettingsPage.guesses_left.set(num)

    def gameover_check_wrong(word):
        """
        - called in check_player_guess() after wrong guess is made
        - returns game_end = True if guesser runs out of guesses
        """
        if SettingsPage.guesses_left.get() == 0:
            #create gameover messages
            winner_name, loser_name = SettingsPage.word_picker.get(), SettingsPage.word_guesser.get()
            message_one = "The word was " + word
            message_two = loser_name + " is out of guesses. " + winner_name + " WINS!"

            #.sets() each message
            StartPage.gameover_message_two.set(message_two)
            StartPage.gameover_message_one.set(message_one)
            game_end = True
            return game_end #ends the game and triggers next_page()

    def gameover_check_correct(word):
        """
        called in check_player_guess() after correct guess
        - returns game_end = True if the guessers completes the word with guesses remaining
        """
        if list(word) == WordPage.word_blank_mirror:
            #create gameover messages
            winner_name, loser_name = SettingsPage.word_guesser.get(), SettingsPage.word_picker.get()
            message_one = "The word was " + word
            message_two = winner_name + " WINS!"

            #.sets() each message
            StartPage.gameover_message_two.set(message_two)
            StartPage.gameover_message_one.set(message_one)
            game_end = True
            return game_end

root = WindowMain()

root.mainloop()

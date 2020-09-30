from tkinter import *

root = Tk()
root['bg'] = "black"
root.geometry("618x422")


def start_game():
    player1label.grid(row=3, column=0)
    player2label.grid(row=3, column=1)
    player1entry.grid(row=4, column=0)
    player2entry.grid(row=4, column=1)
    confirm_start_button.grid(row=5, column=0, columnspan=2, pady=(100, 0))


def enter_game():
    import Pong
    Pong.player1name = player1entry.get()
    Pong.player2name = player2entry.get()
    Pong.main()


def make_report():
    with open("Rsults.txt", "r") as f:
        number_of_lines = len(f.readlines())


background_image = PhotoImage(file="images/Background.png")
background_label = Label(root, image=background_image)
title = Label(root, text="Pong Launcher", font="Helvetica 30 italic", fg="white", bg="black", width=27)
start_game_button = Button(root, text="Start Game", font="SegoeUI 18", fg="white", bg="black", command=start_game)
show_results_button = Button(root, text="Show results", font="SegoeUI 18", fg="white", bg="black")

player1label = Label(root, text="Enter Player 1's name:", font="SegoeUI 15", fg="white", bg="black")
player2label = Label(root, text="Enter Player 2's name:", font="SegoeUI 15", fg="white", bg="black")
player1entry = Entry(root, font="SegoeUI 14")
player2entry = Entry(root, font="SegoeUI 14")
confirm_start_button = Button(root, text="Enter Game!", font="Helvetica 30 italic", fg="white", bg="black", command=enter_game)

background_label.place(x=0, y=0, relwidth=1, relheight=1)
title.grid(row=0, column=0, columnspan=2)
start_game_button.grid(row=1, column=0, pady=(50, 10))
show_results_button.grid(row=1, column=1, pady=(50, 10))
root.mainloop()

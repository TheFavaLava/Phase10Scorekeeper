import sys
import os
import traceback

log_file = os.path.expanduser("~/phase10_launch.log")

try:
    import tkinter as tk
    from tkinter import messagebox, simpledialog

    PHASE_DESCRIPTIONS = {
        1: "2 sets of 3",
        2: "1 set of 3 + 1 run of 4",
        3: "1 set of 4 + 1 run of 4",
        4: "1 run of 7",
        5: "1 run of 8",
        6: "1 run of 9",
        7: "2 sets of 4",
        8: "7 cards of one color",
        9: "1 set of 5 + 1 set of 2",
        10: "1 set of 5 + 1 set of 3",
    }

    class Player:
        def __init__(self, name):
            self.name = name
            self.phase = 1
            self.total_score = 0

        def display_phase(self):
            return "Finished!" if self.phase > 10 else f"Phase {self.phase}"

    class Phase10App:
        def __init__(self, root):
            self.root = root
            self.root.title("Phase 10 Scorekeeper")
            self.players = []
            self.current_round = 1
            self.dealer_index = 0
            self.bg_color = "#222222"

            self.setup_intro_screen()

        def setup_intro_screen(self):
            self.intro_frame = tk.Frame(self.root, bg=self.bg_color)
            self.intro_frame.pack(expand=True, fill="both")

            container = tk.Frame(self.intro_frame, bg=self.bg_color)
            container.place(relx=0.5, rely=0.5, anchor="center")

            tk.Label(container, text="Enter player names (comma-separated):",
                     font=("Segoe UI", 16), bg=self.bg_color, fg="white").pack(pady=(0, 10))

            self.name_entry = tk.Entry(container, width=40, font=("Segoe UI", 14),
                                       bg="white", fg="black", justify="center")
            self.name_entry.pack(pady=5)

            start_button = tk.Button(container, text="Start Game", font=("Segoe UI", 16, "bold"),
                                     bg="#0066cc", fg="black", relief="flat",
                                     activebackground="#004a99", activeforeground="black",
                                     command=self.start_game)
            start_button.pack(pady=(10, 0))

            self.root.bind('<Return>', lambda event: self.start_game())

        def start_game(self):
            names = self.name_entry.get().split(",")
            self.players = [Player(name.strip()) for name in names if name.strip()]
            if not self.players:
                messagebox.showerror("Input Error", "Please enter at least one player name.")
                return

            self.intro_frame.destroy()
            self.setup_game_screen()

        def setup_game_screen(self):
            self.menu = tk.Menu(self.root)
            self.root.config(menu=self.menu)
            player_menu = tk.Menu(self.menu, tearoff=0)
            player_menu.add_command(label="Edit Player Names", command=self.edit_player_names)
            self.menu.add_cascade(label="Options", menu=player_menu)

            self.game_frame = tk.Frame(self.root, bg=self.bg_color)
            self.game_frame.pack(padx=10, pady=10, fill="both", expand=True)

            tk.Label(self.game_frame, text="Phase 10 Scorekeeper",
                     font=("Segoe UI", 20, "bold"), bg=self.bg_color, fg="white").grid(row=0, column=0, columnspan=6, pady=(0,10))

            self.round_label = tk.Label(self.game_frame, text=f"Round {self.current_round}",
                                        font=("Segoe UI", 18), bg=self.bg_color, fg="white")
            self.round_label.grid(row=1, column=0, columnspan=6, pady=(0,20))

            headers = ["Player", "Score", "Phase Completed", "Current Phase", "Dealer"]
            for col, header in enumerate(headers):
                tk.Label(self.game_frame, text=header, font=("Segoe UI", 14, "bold"),
                         bg=self.bg_color, fg="white", padx=5, pady=5).grid(row=2, column=col, sticky="nsew", padx=1, pady=1)

            self.entries = []
            for idx, player in enumerate(self.players):
                row = idx + 3

                name_label = tk.Label(self.game_frame, text=player.name, font=("Segoe UI", 14),
                                      bg=self.bg_color, fg="white")
                name_label.grid(row=row, column=0, sticky="nsew", padx=5, pady=5)

                score_entry = tk.Entry(self.game_frame, font=("Segoe UI", 14),
                                       bg="white", fg="black", justify="center")
                score_entry.grid(row=row, column=1, sticky="nsew", padx=5)

                check_var = tk.IntVar()
                check_frame = tk.Frame(self.game_frame, bg=self.bg_color)
                check_frame.grid(row=row, column=2, sticky="nsew")
                check = tk.Checkbutton(check_frame, variable=check_var, bg=self.bg_color)
                check.pack(expand=True)

                phase_lbl = tk.Label(self.game_frame, text=player.display_phase(),
                                     font=("Segoe UI", 14), bg=self.bg_color, fg="white")
                phase_lbl.grid(row=row, column=3, sticky="nsew", padx=5)

                dealer_lbl = tk.Label(self.game_frame, text="", font=("Segoe UI", 14, "bold"),
                                      bg=self.bg_color, fg="yellow")
                dealer_lbl.grid(row=row, column=4, sticky="nsew", padx=5)

                self.entries.append((player, score_entry, check_var, phase_lbl, dealer_lbl, name_label))

            self.update_dealer_display()

            btn_frame = tk.Frame(self.game_frame, bg=self.bg_color)
            btn_frame.grid(row=len(self.players)+3, column=0, columnspan=6, sticky="ew", pady=(30,0))
            for i in range(6):
                btn_frame.grid_columnconfigure(i, weight=1)

            self.next_round_button = tk.Button(btn_frame, text="Next Round",
                                               font=("Segoe UI", 18, "bold"),
                                               bg="#0066cc", fg="black", relief="flat",
                                               activebackground="#004a99", activeforeground="black",
                                               command=self.next_round)
            self.next_round_button.grid(row=0, column=0, sticky="ew", padx=(0,10), ipadx=20, ipady=12)

            self.rules_button = tk.Button(btn_frame, text="Rules",
                                          font=("Segoe UI", 18, "bold"),
                                          bg="#cccccc", fg="black", relief="flat",
                                          activebackground="#bbbbbb", activeforeground="black",
                                          command=self.show_rules)
            self.rules_button.grid(row=0, column=1, sticky="ew", ipadx=20, ipady=12)

            self.all_finish_button = tk.Button(btn_frame, text="All Finish Phase",
                                               font=("Segoe UI", 18, "bold"),
                                               bg="#28a745", fg="black", relief="flat",
                                               activebackground="#1e7e34", activeforeground="black",
                                               command=self.all_finish_phase)
            self.all_finish_button.grid(row=0, column=2, sticky="ew", padx=(10,0), ipadx=20, ipady=12)

            self.calc_scores_button = tk.Button(btn_frame, text="Calculate Scores",
                                                font=("Segoe UI", 18, "bold"),
                                                bg="#ffaa00", fg="black", relief="flat",
                                                activebackground="#cc8800", activeforeground="black",
                                                command=self.open_score_calculator)
            self.calc_scores_button.grid(row=0, column=3, sticky="ew", padx=(10,0), ipadx=20, ipady=12)

            self.score_display = tk.Text(self.game_frame, height=8, font=("Segoe UI", 30),
                                         bg="#1c1c1c", fg="white", relief="flat")
            self.score_display.grid(row=len(self.players)+4, column=0, columnspan=6, sticky="nsew", pady=(15,0))
            self.score_display.config(state=tk.DISABLED)

            self.game_frame.grid_rowconfigure(len(self.players)+4, weight=1)
            for col in range(6):
                self.game_frame.grid_columnconfigure(col, weight=1)

            self.update_score_display()
            self.root.bind('<Return>', lambda event: self.next_round())

        def update_dealer_display(self):
            for idx, (_, _, _, _, dealer_lbl, _) in enumerate(self.entries):
                dealer_lbl.config(text="✅" if idx == self.dealer_index else "")

        def next_round(self):
            someone_finished = False

            for player, score_entry, check_var, phase_label, _, _ in self.entries:
                score_text = score_entry.get().strip()
                try:
                    score = int(score_text) if score_text else 0
                except ValueError:
                    messagebox.showerror("Invalid Input", f"Enter a valid score for {player.name}")
                    return

                player.total_score += score
                if check_var.get():
                    player.phase += 1
                    if player.phase > 10:
                        someone_finished = True

                score_entry.delete(0, tk.END)
                check_var.set(0)
                phase_label.config(text=player.display_phase())

            self.current_round += 1
            self.round_label.config(text=f"Round {self.current_round}")

            self.dealer_index = (self.dealer_index + 1) % len(self.players)
            self.update_dealer_display()
            self.update_score_display()

            if someone_finished:
                self.end_game()

        def all_finish_phase(self):
            someone_finished = False
            for player, score_entry, check_var, phase_label, _, _ in self.entries:
                score_text = score_entry.get().strip()
                try:
                    score = int(score_text) if score_text else 0
                except ValueError:
                    messagebox.showerror("Invalid Input", f"Enter a valid score for {player.name}")
                    return  # Stop processing if invalid input

                player.total_score += score
                if player.phase <= 10:
                    player.phase += 1
                    if player.phase > 10:
                        someone_finished = True
                    phase_label.config(text=player.display_phase())

                score_entry.delete(0, tk.END)
                check_var.set(0)

            self.current_round += 1
            self.round_label.config(text=f"Round {self.current_round}")

            self.dealer_index = (self.dealer_index + 1) % len(self.players)
            self.update_dealer_display()
            self.update_score_display()

            if someone_finished:
                self.end_game()

        def open_score_calculator(self):
            calc_win = tk.Toplevel(self.root)
            calc_win.title("Score Calculator")
            calc_win.geometry("400x400")
            calc_win.configure(bg=self.bg_color)

            tk.Label(calc_win, text="Enter each player's cards left separated by spaces or commas:",
                     font=("Segoe UI", 12), bg=self.bg_color, fg="white").pack(pady=(10,5))

            entries = []
            for player, _, _, _, _, _ in self.entries:
                frame = tk.Frame(calc_win, bg=self.bg_color)
                frame.pack(fill="x", padx=10, pady=5)

                tk.Label(frame, text=player.name, font=("Segoe UI", 12, "bold"), bg=self.bg_color, fg="white", width=15, anchor="w").pack(side="left")

                entry = tk.Entry(frame, font=("Segoe UI", 12), width=25)
                entry.pack(side="left", fill="x", expand=True)
                entries.append((player, entry))

            def calculate_and_fill():
                for player, entry in entries:
                    cards_text = entry.get().strip()
                    if not cards_text:
                        score = 0
                    else:
                        cards = [c.strip().lower() for c in cards_text.replace(",", " ").split()]
                        score = 0
                        for card in cards:
                            if card in ("skip", "s"):
                                score += 15
                            elif card in ("wild", "w"):
                                score += 25
                            else:
                                try:
                                    num = int(card)
                                    if 1 <= num <= 9:
                                        score += 5
                                    elif 10 <= num <= 12:
                                        score += 10
                                    else:
                                        messagebox.showerror("Invalid Card", f"Invalid card value '{card}' for player {player.name}")
                                        return
                                except ValueError:
                                    messagebox.showerror("Invalid Card", f"Invalid card '{card}' for player {player.name}")
                                    return

                    # Update the player's score entry box with the calculated score
                    for p, score_entry, _, _, _, _ in self.entries:
                        if p == player:
                            score_entry.delete(0, tk.END)
                            score_entry.insert(0, str(score))
                            break

                calc_win.destroy()

            btn_calc = tk.Button(calc_win, text="Calculate Scores",
                                 font=("Segoe UI", 14, "bold"),
                                 bg="#0066cc", fg="black", relief="flat",
                                 activebackground="#004a99", activeforeground="black",
                                 command=calculate_and_fill)
            btn_calc.pack(pady=15, ipadx=10, ipady=6)

        def update_score_display(self):
            self.score_display.config(state=tk.NORMAL)
            self.score_display.delete(1.0, tk.END)
            for player in self.players:
                phase_text = "Finished!" if player.phase > 10 else PHASE_DESCRIPTIONS.get(player.phase, "")
                self.score_display.insert(
                    tk.END, f"{player.name} -- {phase_text} -- Score: {player.total_score}\n"
                )
            self.score_display.config(state=tk.DISABLED)

        def end_game(self):
            self.next_round_button.config(state=tk.DISABLED)
            self.rules_button.config(state=tk.DISABLED)
            self.all_finish_button.config(state=tk.DISABLED)
            self.calc_scores_button.config(state=tk.DISABLED)

            winner = min(self.players, key=lambda p: p.total_score)
            messagebox.showinfo("Game Over", f"🎉 Winner: {winner.name} with {winner.total_score} points!")

            self.new_game_button = tk.Button(
                self.game_frame,
                text="New Game",
                font=("Segoe UI", 18, "bold"),
                bg="#28a745",
                fg="black",
                relief="flat",
                activebackground="#1e7e34",
                activeforeground="black",
                command=self.prompt_new_game
            )
            self.new_game_button.grid(row=len(self.players)+5, column=0, columnspan=6, sticky="ew", pady=(20, 0))

        def prompt_new_game(self):
            choice = messagebox.askquestion(
                "Start New Game",
                "Do you want to use the same players?",
                icon='question'
            )
            if choice == 'yes':
                self.reset_game()
            else:
                self.game_frame.destroy()
                self.setup_intro_screen()

            self.new_game_button.destroy()

        def reset_game(self):
            self.current_round = 1
            self.round_label.config(text=f"Round {self.current_round}")
            self.dealer_index = 0

            for player, score_entry, check_var, phase_label, dealer_lbl, name_label in self.entries:
                player.phase = 1
                player.total_score = 0
                score_entry.delete(0, tk.END)
                check_var.set(0)
                phase_label.config(text=player.display_phase())
                dealer_lbl.config(text="")
            
            self.update_dealer_display()
            self.update_score_display()

            self.next_round_button.config(state=tk.NORMAL)
            self.rules_button.config(state=tk.NORMAL)
            self.all_finish_button.config(state=tk.NORMAL)
            self.calc_scores_button.config(state=tk.NORMAL)

        def show_rules(self):
            rules_text = (
                "Phase 10 Rules:\n\n"
                "Players work to complete 10 phases in order.\n"
                "Each phase requires collecting sets or runs of cards as follows:\n\n"
            )
            for phase, desc in PHASE_DESCRIPTIONS.items():
                rules_text += f"Phase {phase}: {desc}\n"
            rules_text += (
                "\nRound Scoring Rules:\n"
                "At the end of each round, players score points based on the cards left in their hands:\n"
                " - Number cards (1-9): 5 points\n"
                " - Number cards (10-12): 10 points\n"
                " - Skip cards: 15 points\n"
                " - Wild cards: 25 points\n"
            )    
            rules_text += (
                "\nWinning Requirements:\n"
                "The first player to complete all 10 phases wins the game.\n"
                "If multiple players finish Phase 10 in the same round, the player with the lowest score wins.\n\n"
                )

            rules_win = tk.Toplevel(self.root)
            rules_win.title("Phase 10 Rules")
            rules_win.configure(bg="white")
            rules_win.geometry("400x525")

            txt = tk.Text(rules_win, wrap="word", font=("Segoe UI", 12), bg="white", fg="black")
            txt.insert("1.0", rules_text)
            txt.config(state=tk.DISABLED)
            txt.pack(padx=10, pady=10, fill="both", expand=True)

            btn_close = tk.Button(rules_win, text="Close", font=("Segoe UI", 12, "bold"),
                                  bg="#0066cc", fg="black", relief="flat",
                                  command=rules_win.destroy)
            btn_close.pack(pady=(0,10), ipadx=10, ipady=6)

        def edit_player_names(self):
            for idx, (player, _, _, _, _, name_label) in enumerate(self.entries):
                new_name = simpledialog.askstring("Edit Player Name",
                                                  f"Edit name for player #{idx+1} (current: {player.name}):",
                                                  initialvalue=player.name,
                                                  parent=self.root)
                if new_name is not None and new_name.strip():
                    player.name = new_name.strip()
                    name_label.config(text=player.name)
            self.update_score_display()

    if __name__ == "__main__":
        with open(log_file, "w") as f:
            f.write("App starting...\n")

        root = tk.Tk()
        root.geometry("800x600")
        app = Phase10App(root)
        root.mainloop()

except Exception:
    with open(log_file, "a") as f:
        f.write("Exception during launch:\n")
        traceback.print_exc(file=f)
    sys.exit(1)

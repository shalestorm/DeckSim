import random
import requests
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from io import BytesIO
from typing import List
from typing import Optional
from collections import Counter


# --- CARD CLASS ---
class Card:
    # the magic cards themselves

    def __init__(
        self, name: str, type_line: str = "Unknown", image_url: Optional[str] = None
    ):
        self.name = name
        self.type_line = type_line.lower()
        self.image_url = image_url  # Store image link

    def is_land(self) -> bool:
        # checks if the card is a land type Useful as in game you can only play 1 a turn
        # and later we can actually have a counter for lands in hand
        # and in future give reccomendations to keep the hand based on the land value
        # also just good practice for some of the more complex card types and values
        # we can grab from the scryfall api
        return "land" in self.type_line

    def __repr__(self):
        return self.name


# --- DECK CLASS ---
class Deck:
    # builds the deck from decklist text file, and handles shuffling

    def __init__(self, decklist: List[str]):
        self.cards = self.build_deck(decklist)
        # store the original deck list for reference
        self.original_deck = self.cards.copy()

    def build_deck(self, decklist: List[str]) -> List[Card]:
        # builds the deck considering the number of copies per card
        cards = []
        for line in decklist:
            count, card_name = line.split(" ", 1)
            count = int(count)
            for _ in range(count):
                cards.append(self.fetch_card_data(card_name))
        return cards

    def fetch_card_data(self, card_name: str) -> Card:
        # grabs the scryfall info, image, and link for the cards
        url = f"https://api.scryfall.com/cards/named?exact={card_name}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return Card(
                name=data["name"],
                type_line=data.get("type_line", "Unknown"),
                image_url=(
                    data["image_uris"]["normal"] if "image_uris" in data else None
                ),
            )
        else:
            print(f"Warning: Could not fetch {card_name}, using default type.")
            return Card(name=card_name)

    def shuffle(self):
        # shuffles the deck using random's shuffle method
        random.shuffle(self.cards)

    def draw_hand(self, hand_size: int = 7) -> List[Card]:
        # draws the hand
        return (
            [self.cards.pop(0) for _ in range(hand_size)]
            if len(self.cards) >= hand_size
            else self.cards
        )


class DeckSimulatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MTG Deck Simulator")
        self.root.configure(bg="#3C4347")

        self.deck = None
        # stores the unshuffled deck list
        self.original_deck = []
        # stores the drawn hand
        self.previous_hand = []

        # UI Elements
        self.canvas = tk.Canvas(root, width=1400, height=450)
        self.canvas.pack()
        self.canvas.configure(bg="#79929D")
        self.canvas.configure(bd=5)
        self.canvas.configure(highlightthickness=5)
        self.canvas.configure(highlightbackground="#15654E")
        # upload decklist button, which will call the load deck method from our class
        self.upload_button = tk.Button(
            root, text="Upload Decklist", command=self.load_deck
        )
        # pack the button to the root window
        self.upload_button.pack(pady=5)
        # shuffle button, which will call the draw hand method from our class
        self.shuffle_button = tk.Button(
            root, text="Shuffle & Draw", command=self.draw_hand, state=tk.DISABLED
        )
        # pack the button to the root window
        self.shuffle_button.pack(pady=5)
        # label to display the number of lands in the hand
        self.land_count_label = tk.Label(
            root, text="Lands in Hand: 0", font=("Arial", 14)
        )
        self.land_count_label.pack()
        # button to view the full decklist
        self.view_deck_button = tk.Button(
            root,
            text="View Full Decklist",
            command=self.view_full_decklist,
            state=tk.DISABLED,
        )
        self.view_deck_button.pack(pady=5)
        # store image references
        self.card_images = []
        # store the images for full decklist
        self.full_deck_images = []

    def load_deck(self):
        # load and shuffle the deck
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        # open the file and read the decklist
        # if the file is empty, we return
        # but we could add an error message here
        # to tell the user that the file is empty
        if not file_path:
            return  # return if no file selected

        # here we are using open, to read the file
        # and then we are using a list comprehension to strip
        # the whitespace from the file
        # and then we are checking if the line is empty
        # if the line is empty, we skip it
        with open(file_path, "r") as file:
            decklist = [line.strip() for line in file if line.strip()]
        # store original, unshuffled deck
        self.original_deck = decklist.copy()
        self.deck = Deck(decklist)
        # shuffle the deck
        self.deck.shuffle()

        self.shuffle_button.config(state=tk.NORMAL)
        self.view_deck_button.config(state=tk.NORMAL)

        self.draw_hand()

    def draw_hand(self):
        # shuffle and draw hand
        if not self.deck:
            return
        # we check whether they had a previous hand here, because we want to add it back to the deck
        # to simulate a "mulligan" system where the hand is shuffled back in the deck
        # and a new hand is drawn
        if self.previous_hand:
            self.deck.cards.extend(self.previous_hand)

        self.deck.shuffle()
        hand = self.deck.draw_hand()
        self.previous_hand = hand

        # reset the canvas and images
        self.canvas.delete("all")
        self.card_images.clear()

        # count lands
        # we do this as a sort of future proof method
        # we could later because we check for lands in hand
        # give reccomendations on whether to keep said hand
        # based on hitting a specific land threshold, etc
        land_count = sum(1 for card in hand if card.is_land())
        if land_count == 0:
            self.land_count_label.config(text="No Lander hander!")
        else:
            self.land_count_label.config(text=f"Lands in Hand: {land_count}")

        # display the hand on the canvas
        for i, card in enumerate(hand):
            if card.image_url:
                try:
                    response = requests.get(card.image_url)
                    img_data = Image.open(BytesIO(response.content))
                    img_data = img_data.resize((200, 280))
                    img = ImageTk.PhotoImage(img_data)

                    self.card_images.append(img)
                    x_position = 200 * i + 110
                    self.canvas.create_image(x_position, 200, image=img)
                    self.canvas.create_text(
                        x_position,
                        380,
                        text=card.name,
                        font=("Arial", 12, "bold"),
                        width=100,
                        anchor="center",
                        justify="center",
                    )
                # we use this previous try and except block
                # to catch any errors that may occur when loading the image
                # and then we print the error to the console
                # future iterations will include a popup message to the user as well
                except Exception as e:
                    print(f"Error loading image for {card.name}: {e}")

        self.root.update()

    def view_full_decklist(self):
        if not self.deck or not self.deck.cards:
            return

        # Create a window for full decklist view
        deck_window = tk.Toplevel(self.root)
        deck_window.title("Full Decklist")
        deck_window.geometry("1000x600")
        deck_window.configure(bg="#3C4347")

        def on_close():
            canvas.unbind_all("<MouseWheel>")
            deck_window.destroy()

        deck_window.protocol("WM_DELETE_WINDOW", on_close)
        # Bind close event to custom function
        # this way we dont accidentally add a scroll bar
        # to the main window

        max_width = 1000
        total_height = 600

        # Create the canvas and scrollbar
        canvas = tk.Canvas(deck_window, bg="#79929D", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(deck_window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create the frame inside the canvas to hold the cards
        deck_frame = tk.Frame(canvas, bg="#79929D")
        canvas.create_window((0, 0), window=deck_frame, anchor="nw")

        # Count occurrences of each card in the self.deck.cards (shuffled deck)
        card_count = Counter(card.name for card in self.deck.cards)

        # Include the cards from the hand in the count
        # because our deck is a fluid item, that gets updated with the hand
        # removing from it, we add back the hand to the card count
        # such that view full deck doesnt exclude the hand cards
        hand_count = Counter(card.name for card in self.previous_hand)
        card_count.update(hand_count)

        # Layout settings for consistent card spacing
        card_width = 200
        card_height = 280
        card_spacing_x = card_width + 12
        card_spacing_y = card_height + 12
        left_padding = 150
        top_padding = 150
        max_columns = 4

        # Track total count of cards to ensure correct positioning
        card_index = 0
        # count each individual card, including dupes
        # we do this because decklist text are formatted like
        # 4 card1
        # 3 card2
        # 4 card1
        # and so on

        # stores images from our previous fetch
        self.full_deck_images.clear()

        # Add the images of the cards to the deck view
        for card_name, count in card_count.items():
            # Find the first card instance that matches the card name
            card = next((c for c in self.deck.cards if c.name == card_name), None)

            if card and card.image_url:
                try:
                    response = requests.get(card.image_url)
                    if response.status_code == 200:
                        img_data = Image.open(BytesIO(response.content))
                        img_data = img_data.resize(
                            (card_width, card_height)
                        )  # resize image such that it matches the hand card size
                        img = ImageTk.PhotoImage(img_data)

                        # Add card images to the deck list displaying each copy as a separate entry
                        for _ in range(
                            count
                        ):  # Place each copy as if it's a separate card
                            # this helps prevent the same card from being placed in the same spot
                            # Determine row number
                            row = card_index // max_columns
                            # Determine column number
                            column = card_index % max_columns

                            x_position = left_padding + (
                                card_spacing_x * column
                            )  # Adjust x position for column
                            y_position = top_padding + (
                                card_spacing_y * row
                            )  # Adjust y position for row

                            # Place the card at the calculated position
                            canvas.create_image(x_position, y_position, image=img)
                            self.full_deck_images.append(
                                img
                            )  # Store image reference to prevent garbage collection

                            # Increment card index for proper placement of next card
                            card_index += 1

                        # Track the maximum width and total height for scrolling
                        max_width = max(max_width, x_position + card_width)  # type: ignore
                        total_height = max(total_height, y_position + card_height)  # type: ignore

                    else:
                        print(f"Failed to load image for {card.name}")

                except Exception as e:
                    print(f"Error loading image for {card.name}: {e}")

        # Update the scroll region to include all cards
        deck_frame.update_idletasks()
        if not card_index:
            max_width = 1000
            total_height = 600
        canvas.config(scrollregion=canvas.bbox("all"))

        def on_mousewheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        # Bind scrolling to the mouse wheel and scrollbar
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

        # readd the scrollbar, post resizing to fit the canvas
        scrollbar.config(command=canvas.yview)

        # Force canvas update
        canvas.update()


# run program
if __name__ == "__main__":
    root = tk.Tk()
    app = DeckSimulatorUI(root)
    root.mainloop()

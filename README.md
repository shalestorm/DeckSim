# Magic the Gathering Deck Sim

This is a small-scale simulator for Magic: The Gathering deck shuffling.  
The primary goal of this program was to learn and understand Object-Oriented Programming (OOP).  
I made this program during Week 2 of my Hack Reactor bootcamp, using things I have learned —  
as well as personal research into file reading and API usage.

## Goals
The foundational goal was to get a grasp on understanding classes in Python,  
as well as using my interest in one hobby as a catalyst to want to learn more in a profession.

## Contents
- **Folder containing a few sample decklists**
- **The Python program itself**
- **This README file**

## Highlights
Some highlights of the program I feel are:
- The image fetching and card-type fetching using Scryfall's API
- The usage of the `open()` function in Python to read from a text file
- The basic understanding of making a GUI using Tkinter
- The usage of Python modules like `random`, `Pillow`, and `requests`
- The concepts of future-proofing by adding expandable features,  
  such as adding clauses into API fetches to grab card data as well as images (e.g., card type).  
  The example in the program being Lands (which can be a strong indicator of whether to keep or mull).
- The storage methods for information regarding images, namely reuse by storing them in lists,  
  so they are easier to call on again when reshuffling and drawing new hands.
- Ensuring that on deck load and hand shuffles, we check if we previously had information there,  
  such that we can add it back into the deck rather than discard the information.  
  The same logic applies for loading new text files.
- Keeping in mind fail states, in the event the API handler is unavailable or an incorrect input is made in the text files/format.
- Handling the view full deck via storing information in a separate unshuffled list  
  and denoting when we read through the decklist text file to make note of how decks are commonly formatted,  
  such that we append to our deck list (e.g., 4x Lightning Bolt) instead of looking up "4 Lightning Bolt,"  
  and adding the image we find once, four times.

## How-To-Use

1. First, download the program, as well as prepare your decklists.  
   I have attached some example decklist text files inside the repo.  
   **NOTE:** Decklist text files should be formatted as:  
   `*3 card1*`  
   `*4 card2*`  
   `*4 card3*`  
   `*1 card4*`  
   `*20 card5*`
   
2. Once you have your formatted decklist text file and the program downloaded, run the `DeckSim.py` file.

3. You should now be met with your Tkinter GUI interface, featuring a display area for your hand, as well as buttons below.

4. Start by clicking the **Upload Decklist** button at the top, then use your file explorer to select your formatted text file.

5. Wait for a moment while the card images are fetched via the Scryfall API, and you should soon be met with a hand of 7 cards drawn from your deck,  
   as well as a lands-in-hand counter. This can be a good indicator of whether or not you want to keep your hand. You may then, if desired,  
   shuffle your hand back into the deck and draw a new hand of 7 cards if the current one wasn't a keeper.

6. At the bottom, you also have a **View Full Decklist** button, which should open a new window with a scrollbar to accommodate the deck size.  
   The cards should all be sorted so that duplicates are kept next to one another, adhering to a 4-cards-per-row limit.

7. Optionally, rather than restarting the program whenever you want to load a new decklist into the sim viewer,  
   you can simply click the **Upload Decklist** button again without needing to close the program.

## Future Plans

In the future, I would like to expand on the functions of the view deck, namely to include a separate area to receive the sideboard.  
Often, decklists will feature a 15-card "sideboard" that players are allowed to access between games in a best-of-3 match against another player.  
I would like to implement functionality where, when opening the text file, all cards after a line reading `*sideboard*` are omitted from the main decklist and added to a list named "sideboard."  
This way, when I select **View Full Decklist**, I can have a separate label at the bottom of the window stating "Sideboard,"  
acting as the header for a visual representation of those card images.

I would also like to add functionality for Commander decks.  
A Commander deck is a 100-card deck where the single card placed in the sideboard acts as your commander —  
a card that is in a special zone, unaffected by spells or effects, and that you may cast (at any time you could legally cast the card had it been in your hand).  
Because of its special nature, I would like the commander card to be displayed inside the primary hand-view window, though smaller and off to the bottom left or right-hand side.  
Perhaps I could implement logic such that if the program detects exactly 100 lines of text (or 101, given the "sideboard" header),  
then the last line of the text file will be appended to its own separate list named "commander."

**Blackjack (Pygame Implementation)**
=====================================

**Overview**
------------

This is a **Blackjack game** built using **Pygame**, where you can play in either **single-player mode** or **multi-player mode** against two AI-controlled opponents.

**Installation Requirements**
-----------------------------

To run this game, you need **Python** installed on your system, along with the required dependencies. The project was developed using the following Python packages in a virtual environment:

### **Required Packages:**

*   pygame==2.6.1 _(for graphical interface and animations)_
    
*   pytest==8.3.4 _(for running unit tests)_
    

Other dependencies included in the virtual environment:

*   exceptiongroup==1.2.2
    
*   iniconfig==2.0.0
    
*   packaging==24.2
    
*   pip==22.0.2
    
*   pluggy==1.5.0
    
*   setuptools==59.6.0
    
*   tomli==2.2.1
    


**How to Run the Game**
-----------------------

To start the Blackjack game, run:

`blackjack.py`

A terminal prompt will appear, asking you to choose:

*   **Enter 1** for **Single Player Mode** (play against the dealer).
    
*   **Enter 3** for **Multi-Player Mode** (play against two AI opponents).
    

Once selected, a **Pygame window** will open where the game will run.

**How to Run Unit Tests**
-------------------------

This project includes unit tests to validate game functionality.To run the tests, use:

`python -m unittest test.test_deck`

This ensures the **Deck class** and related components work correctly.


**Game Rules**
--------------

*   Each player starts with **two cards**.
    
*   Players can **Hit** (draw a card) or **Stand** (keep their current hand).
    
*   If a player's hand value exceeds **21**, they **bust** and lose.
    
*   If multiple players have the same highest score, it's a **tie**.
    
*   The AI follows probability-based decisions when hitting or standing.
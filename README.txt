MIDNIGHT BLACKJACK — LOCAL STREAMLIT APP

Requirements:
- Python 3.10 or newer recommended
- Internet connection for first package install (Google Fonts are optional styling)

MAC / LINUX:
1. Open Terminal and change into this folder:
   cd path/to/virtual_blackjack_casino
2. Create a virtual environment:
   python3 -m venv .venv
3. Activate it:
   source .venv/bin/activate
4. Install dependencies:
   python -m pip install -r requirements.txt
5. Run the app:
   python -m streamlit run app.py
6. Streamlit will show a local URL, usually http://localhost:8501. Open it in your browser.

WINDOWS:
1. Open PowerShell in this folder.
2. Create a virtual environment:
   py -m venv .venv
3. Activate:
   .\.venv\Scripts\Activate.ps1
4. Install:
   py -m pip install -r requirements.txt
5. Run:
   py -m streamlit run app.py

NOTES:
- The app uses Streamlit session state. Each browser session has its own temporary balance.
- This is a local demo. Other people cannot play from their own devices unless you deploy it.
- For an online multi-user casino, add authentication, persistent database balances, server-side game logic, and appropriate security controls.
- All chips are fictional and have no cash value.

FEATURE: The sidebar includes Monte Carlo estimates for win/push/loss probabilities if the player stands on the current hand. These are educational estimates, not guaranteed results.
FEATURE: The sidebar also provides a simplified basic-strategy suggestion (Hit or Stand) with an explanation based on the player's hand and dealer upcard. It is educational guidance, not a guarantee.

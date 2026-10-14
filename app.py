import random
import streamlit as st

st.set_page_config(
    page_title="Midnight Blackjack",
    page_icon="♠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.stApp {
    background:
      radial-gradient(ellipse at 50% 0%, rgba(20, 108, 75, .22), transparent 44%),
      linear-gradient(145deg, #07110f 0%, #0b1714 55%, #101410 100%);
    color: #f4f1e8;
    font-family: 'DM Sans', sans-serif;
}
.block-container { padding-top: 1.7rem; max-width: 1250px; }
h1, h2, h3 { font-family: 'Playfair Display', Georgia, serif !important; }
.hero {
    border: 1px solid rgba(219, 180, 95, .28);
    border-radius: 22px;
    padding: 26px 30px;
    background: linear-gradient(120deg, rgba(15, 48, 38, .96), rgba(10, 25, 21, .96));
    box-shadow: 0 16px 45px rgba(0,0,0,.24);
    margin-bottom: 20px;
}
.eyebrow { color: #d8b66a; text-transform: uppercase; letter-spacing: .19em; font-size: .74rem; font-weight: 700; }
.hero-title { font-size: clamp(2.1rem, 4vw, 3.5rem); line-height: 1.08; margin: 7px 0 10px; font-family: 'Playfair Display', Georgia, serif; }
.subtle { color: #aebbb3; }
.metric {
    border: 1px solid rgba(255,255,255,.09); background: rgba(255,255,255,.035);
    padding: 16px 18px; border-radius: 16px; min-height: 95px;
}
.metric-label { color: #aebbb3; font-size: .78rem; text-transform: uppercase; letter-spacing: .09em; }
.metric-value { color: #f0d28a; font-size: 1.65rem; font-weight: 700; margin-top: 3px; }
.table-wrap {
    border: 1px solid rgba(216,182,106,.35);
    background: radial-gradient(ellipse at center, #126344 0%, #0c4b37 55%, #083426 100%);
    border-radius: 28px; padding: 26px; box-shadow: inset 0 0 0 7px rgba(4,24,18,.23), 0 18px 45px rgba(0,0,0,.22);
}
.table-label { text-align:center; color:rgba(255,255,255,.62); font-size:.73rem; letter-spacing:.22em; text-transform:uppercase; margin-bottom: 8px; }
.hand-total { text-align:center; color:#fff5d8; font-size:1rem; margin: 7px 0 20px; }
.cards { display:flex; justify-content:center; flex-wrap:wrap; gap:10px; min-height:115px; }
.playing-card {
    width:72px; height:102px; background:#fffdf7; color:#17211c; border-radius:9px;
    box-shadow:0 7px 14px rgba(0,0,0,.25); padding:8px 7px; display:flex; flex-direction:column;
    justify-content:space-between; font-weight:700; font-size:1.05rem; border:1px solid #dedbd1;
}
.playing-card.red { color:#bd3038; }
.card-center { font-size:2rem; text-align:center; line-height:1; }
.card-bottom { align-self:flex-end; transform:rotate(180deg); }
.card-back {
    width:72px; height:102px; border-radius:9px; background:repeating-linear-gradient(45deg,#142e55,#142e55 5px,#1b416d 5px,#1b416d 10px);
    border:4px solid #f1e6c8; box-shadow:0 7px 14px rgba(0,0,0,.25); display:flex; align-items:center; justify-content:center;
    color:#f1e6c8; font-size:1.7rem;
}
.result {
    text-align:center; border:1px solid rgba(216,182,106,.35); border-radius:15px;
    background:rgba(7,19,15,.55); padding:15px; margin-top:20px;
}
.result-title { color:#f0d28a; font-family:'Playfair Display', Georgia, serif; font-size:1.5rem; }
div.stButton > button {
    border-radius: 12px; border:1px solid rgba(240,210,138,.45); min-height: 45px;
    font-weight:700; transition:all .15s ease;
}
div.stButton > button[kind="primary"] {
    background:linear-gradient(135deg,#e7c875,#c69b42); color:#172018; border:0;
}
div.stButton > button:hover { border-color:#f0d28a; transform:translateY(-1px); }
[data-testid="stSidebar"] { background:#08110f; border-right:1px solid rgba(255,255,255,.08); }
div[data-testid="stNumberInput"] input { background:#101d18; color:#f4f1e8; }
hr { border-color:rgba(255,255,255,.1); }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ---------- Game logic ----------
SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
RED_SUITS = {"♥", "♦"}

def new_deck():
    deck = [(rank, suit) for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    return deck

def card_value(card):
    rank, _ = card
    if rank in ("J", "Q", "K"):
        return 10
    if rank == "A":
        return 11
    return int(rank)

def hand_value(hand):
    total = sum(card_value(c) for c in hand)
    aces = sum(1 for rank, _ in hand if rank == "A")
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def is_blackjack(hand):
    return len(hand) == 2 and hand_value(hand) == 21

def draw_card():
    if not st.session_state.deck:
        st.session_state.deck = new_deck()
    return st.session_state.deck.pop()

def start_round():
    if st.session_state.balance < st.session_state.bet:
        st.session_state.message = "Your balance is too low for that bet. Lower your bet or reset your chips."
        return
    st.session_state.balance -= st.session_state.bet
    st.session_state.player_hand = [draw_card(), draw_card()]
    st.session_state.dealer_hand = [draw_card(), draw_card()]
    st.session_state.round_active = True
    st.session_state.round_over = False
    st.session_state.message = ""
    st.session_state.result = ""
    st.session_state.payout = 0
    # Resolve natural blackjacks immediately.
    p_bj = is_blackjack(st.session_state.player_hand)
    d_bj = is_blackjack(st.session_state.dealer_hand)
    if p_bj or d_bj:
        finish_round("blackjack_check")

def finish_round(reason="stand"):
    s = st.session_state
    p_total = hand_value(s.player_hand)
    d_total = hand_value(s.dealer_hand)

    if reason == "blackjack_check":
        if is_blackjack(s.player_hand) and is_blackjack(s.dealer_hand):
            title, payout, message = "Push — both have blackjack", s.bet, "Your original bet is returned."
        elif is_blackjack(s.player_hand):
            title, payout, message = "Blackjack!", int(s.bet * 2.5), "Natural blackjack pays 3:2, including your returned bet."
        else:
            title, payout, message = "Dealer blackjack", 0, "The dealer has a natural 21."
    elif p_total > 21:
        title, payout, message = "Bust!", 0, "You went over 21."
    else:
        while hand_value(s.dealer_hand) < 17:
            s.dealer_hand.append(draw_card())
        d_total = hand_value(s.dealer_hand)
        if d_total > 21 or p_total > d_total:
            title, payout, message = "You win!", s.bet * 2, "Your bet is returned with winnings equal to your bet."
        elif p_total == d_total:
            title, payout, message = "Push — tie game", s.bet, "Your original bet is returned."
        else:
            title, payout, message = "Dealer wins", 0, "Better luck on the next hand."

    s.balance += payout
    s.payout = payout
    s.result = title
    s.message = message
    s.round_active = False
    s.round_over = True

def record_completed_hand():
    """Update session statistics once a round has reached a final result."""
    s = st.session_state
    s.hands_played += 1
    if s.result in ("You win!", "Blackjack!"):
        s.hands_won += 1
    elif "push" in s.result.lower():
        s.hands_pushed += 1
    else:
        s.hands_lost += 1

def card_html(card, hidden=False):
    if hidden:
        return '<div class="card-back">♠</div>'
    rank, suit = card
    color = " red" if suit in RED_SUITS else ""
    return f'<div class="playing-card{color}"><div>{rank}<br>{suit}</div><div class="card-center">{suit}</div><div class="card-bottom">{rank}<br>{suit}</div></div>'

def render_cards(cards, hide_second=False):
    rendered = "".join(card_html(c, hidden=(hide_second and i == 1)) for i, c in enumerate(cards))
    st.markdown(f'<div class="cards">{rendered}</div>', unsafe_allow_html=True)


def estimate_stand_odds(player_hand, dealer_upcard, unseen_cards, simulations=4000):
    """
    Monte Carlo estimate of win/push/loss probabilities if the player stands now.
    The dealer's hidden card is treated as unknown and sampled from unseen_cards.
    """
    wins = pushes = losses = 0

    if hand_value(player_hand) > 21:
        return {"win": 0.0, "push": 0.0, "loss": 1.0, "trials": simulations}

    for _ in range(simulations):
        shoe = unseen_cards.copy()
        random.shuffle(shoe)

        dealer_hand = [dealer_upcard, shoe.pop()]
        # A natural blackjack is only possible with the dealer's first two cards.
        dealer_natural = is_blackjack(dealer_hand)
        player_natural = is_blackjack(player_hand)

        if player_natural or dealer_natural:
            if player_natural and dealer_natural:
                pushes += 1
            elif player_natural:
                wins += 1
            else:
                losses += 1
            continue

        while hand_value(dealer_hand) < 17 and shoe:
            dealer_hand.append(shoe.pop())

        player_total = hand_value(player_hand)
        dealer_total = hand_value(dealer_hand)

        if dealer_total > 21 or player_total > dealer_total:
            wins += 1
        elif player_total == dealer_total:
            pushes += 1
        else:
            losses += 1

    return {
        "win": wins / simulations,
        "push": pushes / simulations,
        "loss": losses / simulations,
        "trials": simulations,
    }



def dealer_upcard_value(card):
    rank, _ = card
    if rank == "A":
        return 11
    if rank in ("J", "Q", "K"):
        return 10
    return int(rank)


def basic_strategy_advice(player_hand, dealer_upcard):
    """
    Beginner-friendly basic-strategy guidance for a common blackjack ruleset.
    This is a simplified educational chart: no surrender, double-after-split,
    or pair-splitting advice is included.
    """
    total = hand_value(player_hand)
    up = dealer_upcard_value(dealer_upcard)
    soft = any(rank == "A" for rank, _ in player_hand) and sum(
        card_value(card) for card in player_hand
    ) == total and total <= 21 and any(
        rank == "A" for rank, _ in player_hand
    ) and (sum(card_value(card) for card in player_hand) != total or total <= 11)

    # Reliable soft-hand check: at least one ace can currently count as 11.
    raw_total = sum(card_value(card) for card in player_hand)
    has_usable_ace = any(rank == "A" for rank, _ in player_hand) and raw_total <= 21

    if total > 21:
        return ("No action — bust", "Your total is over 21, so the hand has already lost.")
    if is_blackjack(player_hand):
        return ("Stand", "You have a natural blackjack. Taking another card is unnecessary, and the hand is already at 21.")

    # Soft totals: an ace is still being counted as 11.
    if has_usable_ace and total <= 21 and raw_total == total:
        if total >= 19:
            return ("Stand", f"Your soft {total} is already strong. Standing avoids risking a weaker total, and the dealer must still beat you.")
        if total == 18:
            if 2 <= up <= 8:
                return ("Stand", f"Soft 18 is strong against a dealer {up}. Standing is a reasonable basic-strategy choice here.")
            return ("Hit", f"Soft 18 is vulnerable against a dealer {up}. Taking a card can improve your hand, and the ace can flex to count as 1.")
        return ("Hit", f"Your soft {total} is relatively low. Hit to improve it; the ace can count as 1 if needed.")

    # Hard totals.
    if total >= 17:
        return ("Stand", f"With a hard {total}, hitting has a substantial bust risk. Let the dealer try to beat your total.")
    if total >= 13:
        if up <= 6:
            return ("Stand", f"Your hard {total} is a reasonable stopping point against a dealer {up}. The dealer is more likely to bust with a weak upcard.")
        return ("Hit", f"A dealer {up} is a strong upcard. A hard {total} is often not enough, so basic strategy says to try to improve it.")
    if total == 12:
        if 4 <= up <= 6:
            return ("Stand", f"With 12 against dealer {up}, standing lets the dealer take the risk of busting. Against stronger upcards, you generally need to improve.")
        return ("Hit", f"12 is usually too weak to stand on against dealer {up}. Hit to improve, while remembering that a 10-value card would bust you.")
    if total == 11:
        return ("Hit", "11 is a strong starting point for improvement. In many rule sets, doubling is preferred, but this version only offers Hit or Stand.")
    if total == 10:
        return ("Hit", f"10 can often improve to a strong total with one card. Doubling may be preferred against weaker dealer cards, but this version only offers Hit or Stand.")
    return ("Hit", f"Your total of {total} is low, so taking another card is the standard basic-strategy move.")


def render_probability_bar(label, probability, color, description):
    pct = probability * 100
    st.markdown(
        f"""
        <div style="margin: 11px 0 5px; display:flex; justify-content:space-between; gap:8px;">
          <span style="color:#e9eee9;font-weight:600;">{label}</span>
          <span style="color:{color};font-weight:700;">{pct:.1f}%</span>
        </div>
        <div style="height:9px;background:#1b2923;border-radius:99px;overflow:hidden;">
          <div style="width:{pct:.2f}%;height:100%;background:{color};border-radius:99px;"></div>
        </div>
        <div style="font-size:.75rem;color:#9eafa5;margin-top:4px;">{description}</div>
        """,
        unsafe_allow_html=True,
    )


# ---------- Session state ----------
defaults = {
    "balance": 1000,
    "bet": 25,
    "deck": new_deck(),
    "player_hand": [],
    "dealer_hand": [],
    "round_active": False,
    "round_over": False,
    "message": "",
    "result": "",
    "payout": 0,
    "hands_played": 0,
    "hands_won": 0,
    "hands_lost": 0,
    "hands_pushed": 0,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## ♠ Midnight")
    st.caption("BLACKJACK CLUB")
    st.divider()
    st.markdown("### Your wallet")
    st.markdown(f"<div class='metric'><div class='metric-label'>Available chips</div><div class='metric-value'>🪙 {st.session_state.balance:,}</div></div>", unsafe_allow_html=True)
    st.markdown("")
    st.markdown("### Table settings")
    max_bet = max(1, st.session_state.balance)
    st.session_state.bet = st.number_input(
        "Your bet (chips)", min_value=1, max_value=max_bet,
        value=min(int(st.session_state.bet), max_bet), step=5,
        disabled=st.session_state.round_active,
        help="Your bet is deducted when a new hand begins."
    )
    st.caption("Minimum bet: 1 chip")
    if st.button("↻ Reset balance", use_container_width=True):
        st.session_state.balance = 1000
        st.session_state.bet = 25
        st.session_state.player_hand = []
        st.session_state.dealer_hand = []
        st.session_state.round_active = False
        st.session_state.round_over = False
        st.session_state.message = "Your balance has been reset to 1,000 chips."
        st.session_state.result = ""
        st.session_state.payout = 0
        st.session_state.hands_played = 0
        st.session_state.hands_won = 0
        st.session_state.hands_lost = 0
        st.session_state.hands_pushed = 0
        st.rerun()
    st.divider()
    st.markdown("### How to play")
    st.markdown("""
- Get closer to **21** than the dealer.
- Number cards count as shown; J, Q and K count as 10.
- Aces count as 1 or 11.
- Dealer stands on 17.
- Blackjack pays **3:2**.
- A tie returns your bet.
""")
    st.caption("For entertainment only. Chips have no cash value.")

    st.divider()
    st.markdown("### 📊 Hand odds")
    st.caption("Probability lesson · Monte Carlo estimate")

    if st.session_state.round_active and st.session_state.player_hand and st.session_state.dealer_hand:
        # Only remove cards the player can see. The dealer's hidden card stays
        # in the unseen pool because its identity is unknown to the player.
        unseen = new_deck()
        visible_cards = st.session_state.player_hand + [st.session_state.dealer_hand[0]]
        for visible_card in visible_cards:
            if visible_card in unseen:
                unseen.remove(visible_card)

        odds = estimate_stand_odds(
            st.session_state.player_hand,
            st.session_state.dealer_hand[0],
            unseen,
            simulations=4000,
        )
        player_total = hand_value(st.session_state.player_hand)
        dealer_up = st.session_state.dealer_hand[0]
        st.markdown(
            f"<div style='border:1px solid rgba(216,182,106,.28);background:rgba(255,255,255,.035);padding:12px;border-radius:13px;margin:8px 0 12px;'>"
            f"<div style='color:#9eafa5;font-size:.73rem;text-transform:uppercase;letter-spacing:.08em;'>If you stand now</div>"
            f"<div style='font-size:1.25rem;font-weight:700;color:#f0d28a;margin-top:3px;'>Your {player_total} vs dealer {dealer_up[0]}{dealer_up[1]}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
        render_probability_bar("Win", odds["win"], "#67d6a1", "You finish with the better hand, or dealer busts.")
        render_probability_bar("Push", odds["push"], "#e7c875", "The final totals tie; your bet is returned.")
        render_probability_bar("Loss", odds["loss"], "#f08b83", "Dealer finishes with the better hand.")
        st.markdown(
            f"<div style='font-size:.72rem;color:#91a39a;margin-top:12px;'>Based on {odds['trials']:,} simulated rounds. Estimates can vary slightly each refresh.</div>",
            unsafe_allow_html=True,
        )

        advice, reason = basic_strategy_advice(
            st.session_state.player_hand,
            st.session_state.dealer_hand[0],
        )
        advice_color = "#67d6a1" if advice == "Stand" else "#e7c875"
        st.markdown(
            f"""
            <div style="margin-top:18px;border:1px solid rgba(216,182,106,.35);
                        background:linear-gradient(135deg,rgba(19,55,40,.75),rgba(13,28,22,.9));
                        border-radius:15px;padding:14px;">
              <div style="font-size:.72rem;color:#9eafa5;text-transform:uppercase;letter-spacing:.1em;">Suggested move</div>
              <div style="font-size:1.35rem;font-weight:700;color:{advice_color};margin:5px 0 8px;">{advice}</div>
              <div style="font-size:.86rem;line-height:1.5;color:#e0e8e2;">{reason}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("Why this suggestion?"):
            st.markdown(
                """
                The suggestion uses a simplified **basic-strategy chart**: a set of commonly recommended moves based on your total and the dealer's visible card.

                - **Hit:** try to improve your total.
                - **Stand:** keep your current total and let the dealer play.
                - The recommendation is educational guidance, not a guarantee.
                - This demo only offers Hit and Stand. Some real blackjack rulesets allow doubling, splitting, or surrender, which can change the best action.
                """
            )

        with st.expander("How are the odds estimated?"):
            st.markdown(
                """
                1. The program removes your visible cards and the dealer's visible upcard from a standard 52-card deck.
                2. It randomly samples the dealer's hidden card and any cards the dealer draws.
                3. The dealer follows the rule of drawing below 17 and standing on 17 or higher.
                4. It repeats this thousands of times and reports the share of wins, pushes, and losses.

                **Important:** These are estimates of the result *if you stand now*, not the best possible strategy. They are not guaranteed outcomes.
                """
            )
    elif st.session_state.round_over and st.session_state.player_hand and st.session_state.dealer_hand:
        st.info("This hand is finished. Deal the next hand to see live odds.")
    else:
        st.markdown(
            "<div style='padding:14px;border:1px dashed rgba(216,182,106,.3);border-radius:13px;color:#aebbb3;font-size:.88rem;'>"
            "Deal a hand to see estimated win, push, and loss probabilities here."
            "</div>",
            unsafe_allow_html=True,
        )

# ---------- Main page ----------
st.markdown("""
<div class="hero">
  <div class="eyebrow">The private table · Since tonight</div>
  <div class="hero-title">Midnight <span style="color:#e4c575">Blackjack</span></div>
  <div class="subtle">Take a seat, place your chips, and play your hand.</div>
</div>
""", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f"<div class='metric'><div class='metric-label'>Your chips</div><div class='metric-value'>🪙 {st.session_state.balance:,}</div></div>", unsafe_allow_html=True)
with m2:
    st.markdown(f"<div class='metric'><div class='metric-label'>Hands played</div><div class='metric-value'>{st.session_state.hands_played}</div></div>", unsafe_allow_html=True)
with m3:
    win_rate = (st.session_state.hands_won / st.session_state.hands_played * 100) if st.session_state.hands_played else 0
    st.markdown(f"<div class='metric'><div class='metric-label'>Win rate</div><div class='metric-value'>{win_rate:.0f}%</div></div>", unsafe_allow_html=True)

st.markdown("")
st.markdown("<div class='table-wrap'>", unsafe_allow_html=True)
st.markdown("<div class='table-label'>Dealer</div>", unsafe_allow_html=True)

if st.session_state.player_hand:
    hide_dealer = st.session_state.round_active
    render_cards(st.session_state.dealer_hand, hide_second=hide_dealer)
    dealer_score = "?" if hide_dealer else str(hand_value(st.session_state.dealer_hand))
    st.markdown(f"<div class='hand-total'>Dealer total: <b>{dealer_score}</b></div>", unsafe_allow_html=True)
else:
    render_cards([("?", "♠"), ("?", "♠")], hide_second=True)
    st.markdown("<div class='hand-total'>Waiting for the next hand</div>", unsafe_allow_html=True)

st.markdown("<hr style='border-color:rgba(255,255,255,.2); margin:20px 0;'>", unsafe_allow_html=True)
st.markdown("<div class='table-label'>Your hand</div>", unsafe_allow_html=True)

if st.session_state.player_hand:
    render_cards(st.session_state.player_hand)
    st.markdown(f"<div class='hand-total'>Your total: <b>{hand_value(st.session_state.player_hand)}</b></div>", unsafe_allow_html=True)
else:
    render_cards([("?", "♠"), ("?", "♠")], hide_second=True)
    st.markdown("<div class='hand-total'>Your cards will appear here</div>", unsafe_allow_html=True)

if st.session_state.round_over and st.session_state.result:
    st.markdown(f"""
    <div class="result">
      <div class="result-title">{st.session_state.result}</div>
      <div class="subtle">{st.session_state.message}</div>
      <div style="margin-top:8px;color:#f0d28a;font-weight:700;">Payout: {st.session_state.payout:,} chips</div>
    </div>
    """, unsafe_allow_html=True)
elif st.session_state.message:
    st.info(st.session_state.message)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("")

# ---------- Controls ----------
if not st.session_state.round_active:
    if st.session_state.balance <= 0:
        st.warning("You're out of chips. Reset your balance to keep playing.")
    start_col, info_col = st.columns([1, 2])
    with start_col:
        if st.button("♠  Deal new hand", type="primary", use_container_width=True, disabled=st.session_state.balance < st.session_state.bet):
            start_round()
            if st.session_state.round_over:
                record_completed_hand()
            st.rerun()
    with info_col:
        st.markdown(f"<p class='subtle' style='padding-top:8px'>Betting <b style='color:#f0d28a'>{st.session_state.bet:,} chips</b> · No real money, no purchases.</p>", unsafe_allow_html=True)
else:
    hit_col, stand_col, tip_col = st.columns([1, 1, 2])
    with hit_col:
        if st.button("＋ Hit", type="primary", use_container_width=True):
            st.session_state.player_hand.append(draw_card())
            if hand_value(st.session_state.player_hand) > 21:
                finish_round("hit")
                record_completed_hand()
            st.rerun()
    with stand_col:
        if st.button("Ⅱ Stand", use_container_width=True):
            finish_round("stand")
            record_completed_hand()
            st.rerun()
    with tip_col:
        st.markdown("<p class='subtle' style='padding-top:8px'>Choose <b>Hit</b> to take another card or <b>Stand</b> to let the dealer play.</p>", unsafe_allow_html=True)

st.markdown("")
with st.expander("Game rules & payout details"):
    st.markdown("""
    - **Regular win:** pays 1:1. Your bet is returned plus winnings equal to your bet.
    - **Natural blackjack:** an ace plus a 10-value card in the first two cards; pays 3:2.
    - **Push:** you and the dealer tie; your bet is returned.
    - **Bust:** a hand over 21 loses.
    - **Dealer rule:** dealer draws on 16 or less and stands on 17 or more.
    - This demo uses a shuffled single deck and replaces it when exhausted. It is a casual game, not a certified gambling system.
    """)

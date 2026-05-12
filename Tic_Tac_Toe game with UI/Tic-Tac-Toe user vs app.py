import streamlit as st
import time

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Unbeatable AI Tic Tac Toe",
    page_icon="🔥",
    layout="centered"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background-color: #050816;
    color: white;
}

/* HIDE STREAMLIT UI */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* TITLE */
.title {

    text-align: center;

    font-size: 55px;

    font-weight: bold;

    color: #38bdf8;

    margin-bottom: 20px;
}

/* ATTEMPT BOX */
.attempt-box {

    background: #1e2a5a;

    border: 2px solid #38bdf8;

    border-radius: 20px;

    padding: 16px;

    text-align: center;

    font-size: 28px;

    font-weight: bold;

    margin-bottom: 30px;

    color: white;
}

/* GAME BOARD */
.board-container {

    display: flex;

    justify-content: center;

    align-items: center;

    margin-top: 10px;
}

/* GAME CELL BUTTONS ONLY */
.board-cell button {

    width: 95px !important;

    height: 95px !important;

    border-radius: 18px !important;

    border: 3px solid #38bdf8 !important;

    background: #0f172a !important;

    color: white !important;

    font-size: 48px !important;

    font-weight: bold !important;

    box-shadow:
        0px 0px 15px rgba(56,189,248,0.3),
        inset 0px 0px 8px rgba(255,255,255,0.05);

    transition: 0.2s ease;
}

/* HOVER */
.board-cell button:hover {

    transform: scale(1.05);

    border-color: cyan !important;

    box-shadow:
        0px 0px 25px cyan,
        inset 0px 0px 10px rgba(255,255,255,0.08);
}

/* WINNER CELLS */
.winner button {

    border: 4px solid red !important;

    box-shadow:
        0px 0px 25px red !important;
}

/* SMALL RESTART BUTTON */
.restart-btn button {

    width: auto !important;

    height: auto !important;

    padding: 10px 18px !important;

    font-size: 15px !important;

    border-radius: 12px !important;

    background: #111827 !important;

    border: 2px solid #38bdf8 !important;

    margin-top: 20px;
}

/* WINNER LINE */
.win-line {

    height: 6px;

    background: red;

    border-radius: 20px;

    margin: auto;

    margin-top: -165px;

    margin-bottom: 160px;

    width: 300px;

    box-shadow: 0px 0px 20px red;
}

/* FOOTER */
.footer {

    text-align: center;

    color: gray;

    margin-top: 40px;
}

/* MOBILE */
@media (max-width: 768px) {

    .title {

        font-size: 38px;
    }

    .attempt-box {

        font-size: 20px;
    }

    .board-cell button {

        width: 80px !important;

        height: 80px !important;

        font-size: 38px !important;
    }

    .win-line {

        width: 250px;

        margin-top: -140px;

        margin-bottom: 140px;
    }
}

</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================
if "board" not in st.session_state:
    st.session_state.board = [""] * 9

if "gameover" not in st.session_state:
    st.session_state.gameover = False

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "winner_cells" not in st.session_state:
    st.session_state.winner_cells = []

board = st.session_state.board

# ================= CHECK WINNER =================
def checkwinner(board, player):

    wins = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6]
    ]

    for win in wins:

        if (
            board[win[0]] ==
            board[win[1]] ==
            board[win[2]] == player
        ):

            st.session_state.winner_cells = win

            return True

    return False

# ================= MINIMAX =================
def minimax(board, depth, isMaximizing):

    if checkwinner(board, "O"):
        return 10 - depth

    if checkwinner(board, "X"):
        return depth - 10

    if "" not in board:
        return 0

    if isMaximizing:

        bestscore = -100

        for i in range(9):

            if board[i] == "":

                board[i] = "O"

                score = minimax(board, depth + 1, False)

                board[i] = ""

                bestscore = max(score, bestscore)

        return bestscore

    else:

        bestscore = 100

        for i in range(9):

            if board[i] == "":

                board[i] = "X"

                score = minimax(board, depth + 1, True)

                board[i] = ""

                bestscore = min(score, bestscore)

        return bestscore

# ================= AI MOVE =================
def computer_move():

    bestscore = -100
    bestmove = 0

    for i in range(9):

        if board[i] == "":

            board[i] = "O"

            score = minimax(board, 0, False)

            board[i] = ""

            if score > bestscore:

                bestscore = score
                bestmove = i

    board[bestmove] = "O"

# ================= PLAYER MOVE =================
def player_move(index):

    if board[index] == "" and not st.session_state.gameover:

        board[index] = "X"

        st.session_state.attempts += 1

        # PLAYER WIN
        if checkwinner(board, "X"):

            st.session_state.gameover = True
            return

        # TIE
        if "" not in board:

            st.session_state.gameover = True
            return

        # AI THINKING
        with st.spinner("AI is thinking..."):
            time.sleep(0.3)

        # AI MOVE
        computer_move()

        # AI WIN
        if checkwinner(board, "O"):

            st.session_state.gameover = True
            return

        # TIE
        if "" not in board:

            st.session_state.gameover = True

# ================= TITLE =================
st.markdown("""
<div class='title'>
🔥 Unbeatable AI Tic Tac Toe
</div>
""", unsafe_allow_html=True)

# ================= ATTEMPTS =================
st.markdown(f"""
<div class='attempt-box'>
🎯 Attempts Taken: {st.session_state.attempts}
</div>
""", unsafe_allow_html=True)

# ================= GAME BOARD =================

for row in range(3):

    cols = st.columns(3)

    for col in range(3):

        index = row * 3 + col

        symbol = board[index]

        # SYMBOLS
        if symbol == "X":

            display_symbol = "✖"

        elif symbol == "O":

            display_symbol = "◉"

        else:

            display_symbol = ""

        with cols[col]:

            st.markdown(
                "<div class='board-cell'>",
                unsafe_allow_html=True
            )

            # WINNER CELLS
            if index in st.session_state.winner_cells:

                st.markdown(
                    "<div class='winner'>",
                    unsafe_allow_html=True
                )

            st.button(
                display_symbol,
                key=index,
                on_click=player_move,
                args=(index,)
            )

            if index in st.session_state.winner_cells:

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

# ================= WIN LINE =================
if len(st.session_state.winner_cells) == 3:

    st.markdown("""
    <div class='win-line'></div>
    """, unsafe_allow_html=True)

# ================= RESULT =================
if checkwinner(board, "X"):

    st.success(
        f"🎉 You Won in {st.session_state.attempts} attempts!"
    )

elif checkwinner(board, "O"):

    st.error(
        f"😈 AI Won in {st.session_state.attempts} attempts!"
    )

elif "" not in board:

    st.warning(
        f"🤝 Match Tie in {st.session_state.attempts} attempts!"
    )

# ================= RESTART =================
st.markdown("<div class='restart-btn'>", unsafe_allow_html=True)

if st.button("🔄 Restart Game"):

    st.session_state.board = [""] * 9
    st.session_state.gameover = False
    st.session_state.attempts = 0
    st.session_state.winner_cells = []

    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# ================= EXTRA CONTENT =================
st.markdown("---")

st.markdown("""
<h2 style='text-align:center; color:cyan;'>
"Beat me if you can 😈"
</h2>
""", unsafe_allow_html=True)

st.markdown("---")

st.subheader("🎮 How To Play")

st.write("""
- You are **X**
- AI is **O**
- Click any box to place your move
- Try to survive against the unbeatable AI 😈
""")

st.markdown("---")

st.subheader("💭 About The AI")

st.write("""
This AI uses the **Minimax Algorithm** to predict all possible future moves.

That means:
- It never makes mistakes
- It never loses
- Best possible result against it is a tie 😈
""")

st.markdown("---")

st.subheader("🔗 Connect With Me")

st.write("""
- GitHub: https://github.com/yourname
- LinkedIn: https://linkedin.com/in/yourname
""")

st.markdown("""
<div class='footer'>
⚡ Built by Sutakar using Python + Streamlit
<br><br>
Made with ❤️ by Sutakar
</div>
""", unsafe_allow_html=True)

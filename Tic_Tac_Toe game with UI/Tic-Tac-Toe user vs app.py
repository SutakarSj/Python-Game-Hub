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

.main {
    background-color: #020617;
    color: white;
}

/* TITLE */
.title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    color: #38bdf8;
    margin-bottom: 25px;
}

/* ATTEMPTS BOX */
.attempt-box {
    background: #172554;
    padding: 14px;
    border-radius: 15px;
    text-align: center;
    font-size: 24px;
    margin-bottom: 30px;
    border: 2px solid #38bdf8;
    color: white;
}

/* GAME BUTTONS */
.stButton > button {

    width: 100%;
    aspect-ratio: 1 / 1;

    font-size: 55px !important;
    font-weight: bold;

    border-radius: 20px;
    border: 3px solid #38bdf8;

    background-color: #0f172a;
    color: white;

    transition: 0.25s ease-in-out;

    margin-bottom: 10px;
}

/* HOVER EFFECT */
.stButton > button:hover {

    border-color: cyan;
    transform: scale(1.04);

    box-shadow: 0px 0px 20px cyan;
}

/* WINNING CELLS */
.winner button {

    background-color: #7f1d1d !important;

    border: 4px solid red !important;

    color: white !important;

    box-shadow: 0px 0px 20px red !important;
}

/* MOBILE RESPONSIVE */
@media (max-width: 768px) {

    .title {
        font-size: 34px;
    }

    .stButton > button {

        font-size: 38px !important;

        border-radius: 15px;
    }

    .attempt-box {
        font-size: 18px;
    }
}

/* FOOTER */
.footer {
    text-align: center;
    color: gray;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================
if "board" not in st.session_state:
    st.session_state.board = ["-"] * 9

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
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
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


# ================= MINIMAX AI =================
def minimax(board, depth, isMaximizing):

    if checkwinner(board, "O"):
        return 10 - depth

    if checkwinner(board, "X"):
        return depth - 10

    if "-" not in board:
        return 0

    # AI TURN
    if isMaximizing:

        bestscore = -100

        for i in range(9):

            if board[i] == "-":

                board[i] = "O"

                score = minimax(board, depth + 1, False)

                board[i] = "-"

                bestscore = max(score, bestscore)

        return bestscore

    # PLAYER TURN
    else:

        bestscore = 100

        for i in range(9):

            if board[i] == "-":

                board[i] = "X"

                score = minimax(board, depth + 1, True)

                board[i] = "-"

                bestscore = min(score, bestscore)

        return bestscore


# ================= COMPUTER MOVE =================
def computer_move():

    bestscore = -100
    bestmove = 0

    for i in range(9):

        if board[i] == "-":

            board[i] = "O"

            score = minimax(board, 0, False)

            board[i] = "-"

            if score > bestscore:

                bestscore = score
                bestmove = i

    board[bestmove] = "O"


# ================= PLAYER MOVE =================
def player_move(index):

    if board[index] == "-" and not st.session_state.gameover:

        board[index] = "X"

        st.session_state.attempts += 1

        # PLAYER WIN
        if checkwinner(board, "X"):

            st.session_state.gameover = True
            return

        # TIE
        if "-" not in board:

            st.session_state.gameover = True
            return

        # AI THINKING EFFECT
        with st.spinner("AI is thinking..."):
            time.sleep(0.3)

        # AI MOVE
        computer_move()

        # AI WIN
        if checkwinner(board, "O"):

            st.session_state.gameover = True
            return

        # TIE
        if "-" not in board:

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
🎯 Attempts Taken: <b>{st.session_state.attempts}</b>
</div>
""", unsafe_allow_html=True)

# ================= GAME BOARD =================
for row in range(3):

    cols = st.columns(3)

    for col in range(3):

        index = row * 3 + col

        symbol = board[index]

        if symbol == "-":
            symbol = ""

        # WINNER CELL
        if index in st.session_state.winner_cells:

            cols[col].markdown(
                "<div class='winner'>",
                unsafe_allow_html=True
            )

        cols[col].button(
            symbol,
            key=index,
            on_click=player_move,
            args=(index,)
        )

        if index in st.session_state.winner_cells:

            cols[col].markdown(
                "</div>",
                unsafe_allow_html=True
            )

# ================= RESULT =================
if checkwinner(board, "X"):

    st.success(
        f"🎉 You Won in {st.session_state.attempts} attempts!"
    )

elif checkwinner(board, "O"):

    st.error(
        f"😈 AI Won! You survived {st.session_state.attempts} attempts."
    )

elif "-" not in board:

    st.warning(
        f"🤝 Tie Match in {st.session_state.attempts} attempts."
    )

# ================= RESTART =================
if st.button("🔄 Restart Game"):

    st.session_state.board = ["-"] * 9
    st.session_state.gameover = False
    st.session_state.attempts = 0
    st.session_state.winner_cells = []

    st.rerun()

# ================= EXTRA CONTENT =================
st.markdown("---")

st.markdown("""
<h3 style='text-align:center; color:cyan;'>
"Beat me if you can 😈"
</h3>
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

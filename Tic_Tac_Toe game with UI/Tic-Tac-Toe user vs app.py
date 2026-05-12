import streamlit as st

# Initialize board
if "board" not in st.session_state:
    st.session_state.board = ["-"] * 9

if "gameover" not in st.session_state:
    st.session_state.gameover = False

board = st.session_state.board


# CHECK WINNER
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
            return True

    return False


# MINIMAX AI
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


# COMPUTER MOVE
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


# PLAYER MOVE
def player_move(index):

    if board[index] == "-" and not st.session_state.gameover:

        board[index] = "X"

        # PLAYER WIN
        if checkwinner(board, "X"):
            st.session_state.gameover = True
            return

        # TIE
        if "-" not in board:
            st.session_state.gameover = True
            return

        # AI MOVE
        computer_move()

        # AI WIN
        if checkwinner(board, "O"):
            st.session_state.gameover = True
            return

        # TIE
        if "-" not in board:
            st.session_state.gameover = True


# ================= UI =================

st.title("🔥 Unbeatable AI Tic Tac Toe")

# GAME BOARD
for row in range(3):

    cols = st.columns(3)

    for col in range(3):

        index = row * 3 + col

        cols[col].button(
            board[index],
            key=index,
            on_click=player_move,
            args=(index,)
        )


# RESULT
if checkwinner(board, "X"):

    st.success("🎉 You Win")

elif checkwinner(board, "O"):

    st.error("😈 AI Wins")

elif "-" not in board:

    st.warning("🤝 It's a Tie")


# RESTART BUTTON
if st.button("Restart Game"):

    st.session_state.board = ["-"] * 9
    st.session_state.gameover = False

    st.rerun()


# ================= EXTRA CONTENT =================

st.markdown("""
<h3 style='color:cyan;'>
"Beat me if you can 😈"
</h3>
""", unsafe_allow_html=True)

st.markdown("---")

st.subheader("🎮 How To Play")

st.write("""
- You are X
- AI is O
- Click any box to place your move
- Try to survive against the unbeatable AI 😈
""")

st.markdown("""
### 🔗 Connect With Me

- GitHub: https://github.com/yourname
- LinkedIn: https://linkedin.com/in/yourname
""")

st.markdown("---")

st.subheader("💭 About The AI")

st.write("""
This AI uses the Minimax Algorithm to predict all possible future moves.

That means:
- It never makes mistakes
- It never loses
- Best possible result against it is a tie 😈
""")

st.markdown("---")

st.caption("⚡ Built by Sutakar using Python + Streamlit")

st.markdown("---")

st.caption("Made with ❤️ by Sutakar")

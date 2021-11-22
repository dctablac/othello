const body = document.querySelector('body');
const gameSettingForm = document.querySelector('#game-setting-form');

let game_board;
let game_info;

gameSettingForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    try {
        // Submit board size to endpoint to generate board and game info
        await setGame(gameSettingForm['board-size'].value);
        // Fade out settings
        fadeOutSettings();
        // Fade in game
        fadeGameIn();
    } catch(err) {
        console.error(err);
    }
});

async function setGame(size) {
    const headers = { 'Content-type': 'application/json' }
    const res = await fetch('/game/new_game', { method: 'POST', body: JSON.stringify({ boardSize: size }), headers: headers });
    const data = await res.json();
    game_board = data.board;
    game_info = data.game_info;
}

function fadeOutSettings() {
    const gameSetup = document.querySelector('#game-setup');
    body.removeChild(gameSetup);
}

function fadeGameIn() {
    addGameInfoDisplay();
    addGameBoardDisplay();
}

function addGameInfoDisplay() {
    /*
        <section id="game-info-area" class="game-info-area">
            <h1 class="game-title">Othello</h1>
            <div class="player-scores">
                <p>B: <span id="score-black">2</span></p>
                <p>W: <span id="score-white">2</span></p>
            </div>
            <p class="player-turn">Turn: <span id="player-turn"></span></p>
            <div class="move-log">
                <ul id="move-log-list"></ul>
            </div>
        </section>
    */
   // Create game info area section
   const gameInfoDisplay = document.createElement('section');
   gameInfoDisplay.id = 'game-info-area';
   gameInfoDisplay.className = 'game-info-area';
   // Game title
   const gameTitle = document.createElement('h1');
   gameTitle.className = 'game-title';
   gameTitle.innerText = 'Othello';
   gameInfoDisplay.appendChild(gameTitle);
   // Player scores
   const playerScores = document.createElement('div');
   playerScores.className = 'player-scores';
   const playerScoreLabels = {
       B: 'score-black',
       W: 'score-white'
   }
   for (let player of Object.keys(playerScoreLabels)) {
       let score = document.createElement('p');
       score.innerText = `${player}: `;
       let scoreNum = document.createElement('span');
       scoreNum.id = playerScoreLabels.player;
       scoreNum.innerText = '2';
       score.appendChild(scoreNum);
       playerScores.appendChild(score);
   }
   gameInfoDisplay.appendChild(playerScores);
   // Turn display
   const turnDisplay = document.createElement('p');
   turnDisplay.className = 'turn-display'
   turnDisplay.innerText = 'Turn: '
   const turnDisplayNum = document.createElement('span');
   turnDisplayNum.id = 'player-turn-data';
   turnDisplayNum.innerText = 'B';
   turnDisplay.appendChild(turnDisplayNum);
   gameInfoDisplay.appendChild(turnDisplay);
   // Move Log
   const moveLogDisplay = document.createElement('div');
   moveLogDisplay.className = 'move-log';
   const moveLogList = document.createElement('ul');
   moveLogDisplay.appendChild(moveLogList);
   gameInfoDisplay.appendChild(moveLogDisplay);

   body.appendChild(gameInfoDisplay);
}

function addGameBoardDisplay() {
    const boardElement = document.createElement('section');
    boardElement.className = 'game-board';
    boardElement.style.gridTemplateColumns = `repeat(${game_board.length}, 1fr)`;
    for (let row of game_board) {
        for (let col of row) {
            let cell = document.createElement('div');
            cell.className = 'board-cell'
            switch(col) {
                case '-':
                    break;
                case 'B':
                    cell.appendChild(createGamePiece('black'));
                    break;
                case 'W':
                    cell.appendChild(createGamePiece('white'));
                    break;
                default:
                    break;
            }
            boardElement.appendChild(cell);
        }
    }
    body.appendChild(boardElement);
}

function createGamePiece(color) {
    let piece = document.createElement('div');
    piece.className = 'game-piece';
    piece.style.backgroundColor = color;
    return piece;
}
import { handleMove, createGamePiece } from './game.js';

const body = document.querySelector('body');
const gameSettingForm = document.querySelector('#game-setting-form');

export let game_board;
export let game_info;

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
    const res = await fetch('/game/new_game', { 
        method: 'POST', 
        body: JSON.stringify({ 
            boardSize: size 
        }), 
        headers: headers 
    });
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
    // Game info top half
    const gameStats = document.createElement('div');
    gameStats.className = 'game-stats'
    // Create game info area section
    const gameInfoDisplay = document.createElement('section');
    gameInfoDisplay.id = 'game-info';
    gameInfoDisplay.className = 'game-info';
    // Game title
    const gameTitle = document.createElement('h1');
    gameTitle.className = 'game-title';
    gameTitle.innerText = 'Othello';
    gameStats.appendChild(gameTitle);
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
        scoreNum.id = playerScoreLabels[player];
        scoreNum.innerText = '2';
        score.appendChild(scoreNum);
        playerScores.appendChild(score);
    }
    gameStats.appendChild(playerScores);
    // Turn display
    const turnDisplay = document.createElement('p');
    turnDisplay.className = 'turn-display';
    turnDisplay.innerText = 'Turn: ';
    const turnDisplayNum = document.createElement('span');
    turnDisplayNum.id = 'player-turn-data';
    turnDisplayNum.innerText = ' B';
    turnDisplay.appendChild(turnDisplayNum);
    gameStats.appendChild(turnDisplay);

    gameInfoDisplay.appendChild(gameStats);

    // Move Log
    const moveLogDisplay = document.createElement('div');
    moveLogDisplay.className = 'move-log';
    const moveLogList = document.createElement('ul');
    moveLogList.id = 'move-log-list';
    moveLogDisplay.appendChild(moveLogList);
    gameInfoDisplay.appendChild(moveLogDisplay);

    body.appendChild(gameInfoDisplay);
}

function addGameBoardDisplay() {
    const boardElement = document.createElement('section');
    boardElement.className = 'game-board';
    boardElement.style.gridTemplateColumns = `repeat(${game_board.length}, 1fr)`;
    for (let row = 0; row < game_board.length; row++) {
        for (let col = 0; col < game_board.length; col++) {
            let cell = document.createElement('div');
            cell.className = 'board-cell';
            // Track cell position in board
            cell.setAttribute('position', `${row},${col}`);
            // Handles game move on click
            cell.addEventListener('click', handlePiecePlacement);
            switch(game_board[row][col]) {
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

async function handlePiecePlacement(e) {
    const log = document.createElement('li');
    const move = await handleMove(e);
    const newGameInfo = move.game_info;
    // console.log(updatedGame);
    if (move.status !== 500) {
        refreshInfo(move.game_info);
        refreshBoard(move.board);
        // Log move to move log
        log.innerText = `Player ${newGameInfo[6]} makes move at ${newGameInfo[5][0]}, ${newGameInfo[5][1]}.`;
    } else {
        log.innerText = 'Invalid move.'
    }
    document.querySelector('#move-log-list').appendChild(log);
}

function refreshBoard(newBoard) {
    // For now, just loop through all spots, and compare to new board
    game_board = newBoard
    const currentBoard = document.querySelector('.game-board');
    let piece, position, row, column;
    for (let child of currentBoard.children) {
        position = child.getAttribute('position').split(',');
        row = parseInt(position[0]);
        column = parseInt(position[1]);
        piece = newBoard[row][column];
        child.innerHTML = ""
        switch(piece) {
            case '-':
                break;
            case 'B':
                child.appendChild(createGamePiece('black'));
                break;
            case 'W':
                child.appendChild(createGamePiece('white'));
                break;
            default:
                break;
        }
    }
}

function refreshInfo(newInfo) {
    // Set new game info
    game_info = newInfo;
    // Black count
    document.querySelector('#score-black').innerText = newInfo[0];
    // White count
    document.querySelector('#score-white').innerText = newInfo[1];
    // Turn
    document.querySelector('#player-turn-data').innerText = newInfo[2];
}

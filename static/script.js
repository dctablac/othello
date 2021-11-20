const pageContent = document.querySelector('#content');
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
    pageContent.innerHTML = "";
}

function fadeGameIn() {
    const boardElement = document.createElement('div');
    boardElement.className = 'game-board';
    boardElement.style.gridTemplateColumns = `repeat(${game_board.length}, 1fr)`;
    for (let row of game_board) {
        for (let col of row) {
            let cell = document.createElement('div');
            cell.className = 'board-cell'
            let icon = document.createElement('p');
            icon.className = 'cell-icon'
            switch(col) {
                case '-':
                    icon.innerText = '';
                    break;
                case 'B':
                    icon.innerText = 'B';
                    break;
                case 'W':
                    icon.innerText = 'W';
                    break;
                default:
                    break;
            }
            cell.appendChild(icon);
            boardElement.appendChild(cell);
        }
    }
    pageContent.appendChild(boardElement);
}

function game_piece(color) {

}
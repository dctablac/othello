// Functions to handle game processing from backend
import { game_board, game_info } from './script.js';

export async function handleMove(e) {
    try {
        const pos = e.target.getAttribute('position').split(','); // [row,col]
        const headers = { 'Content-type': 'application/json' }
        const res = await fetch('/game/request_move', {
            method: 'POST',
            body: JSON.stringify({
                board: game_board,
                game_info: game_info,
                move_row: pos[0],
                move_column: pos[1]
            }),
            headers: headers
        });
        const data = await res.json();
        return data
    } catch(err) {
        console.error(err);
    }
}

export function createGamePiece(color) {
    // Piece container
    let piece = document.createElement('div');
    // Class
    piece.className = 'game-piece';
    // Background color according to player
    piece.style.backgroundColor = color;
    return piece;
}
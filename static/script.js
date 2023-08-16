document.addEventListener('DOMContentLoaded', function () {

    const startChoiceDropdown = document.getElementById('startChoice');
    const symbolChoiceContainer = document.getElementById('symbolChoiceContainer');

    // Initially set visibility based on the dropdown's default value
    toggleSymbolChoice(startChoiceDropdown.value);

    startChoiceDropdown.addEventListener('change', function() {
        toggleSymbolChoice(startChoiceDropdown.value);
    });

    function toggleSymbolChoice(value) {
        if (value === 'computer') {
            symbolChoiceContainer.style.display = 'none';
        } else {
            symbolChoiceContainer.style.display = 'block';
        }
    }

    const cells = document.querySelectorAll('.cell');
    let currentGameId = null;

    cells.forEach(cell => {
        cell.addEventListener('click', function (e) {
            if (!e.target.textContent) {
                makeMove(e.target.dataset.index);
                console.log('Clicked on cell:', e.target.dataset.index);
            }
        });
    });

    function makeMove(index) {
        if (!currentGameId) {
            // If there's no game yet, start a new one
            startNewGame(index);
            console.log('Started a new game');
        } else {
            // If there's an ongoing game, make a move
            updateGame(index);
            console.log('Updated the game');
        }
    }

    function startNewGame(index) {
        let board = '---------';
        board = setMoveOnBoard(board, index, 'x'); // Assuming player is always 'x' for the first move
        console.log('Starting a new game with board:', board);
        fetch('/api/v1/games', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ board: board })
        })
        .then(response => response.json())
        .then(data => {
            currentGameId = data.id;
            console.log('New game created with id:', currentGameId);
            renderBoard(data.board);
            console.log('Rendered the board');
        })
        .catch(error => console.error('Error starting a new game:', error));
    }

function updateGame(index) {
    console.log('Initiating updateGame for index:', index);

    fetch(`/api/v1/games/${currentGameId}`)
    .then(response => {
        console.log('Initial fetch response:', response);
        return response.json();
    })
    .then(data => {
        console.log('Received game data:', data);

        let board = data.board;
        console.log('Current board:', board);

        board = setMoveOnBoard(board, index, 'x'); // Assuming player is always 'x' for the first move
        console.log('Updated board:', board);

        return fetch(`/api/v1/games/${currentGameId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ board: board })
        });
    })
    .then(response => {
        console.log('PUT response:', response);
        return response.json();
    })
    .then(data => {
        console.log('Received data after PUT request:', data);

        if (data.board) {
            renderBoard(data.board);
            console.log('Rendered the board');
        } else {
            console.error('No board data received after PUT request:', data);
        }
    })
    .catch(error => {
        console.error('Error encountered during updateGame:', error);
    });
}


    function setMoveOnBoard(board, index, move) {
        let boardArray = Array.from(board);
        boardArray[index] = move;
    
        let newBoard = boardArray.join('');
        console.log('New board:', newBoard);
        return newBoard;
    }
    
    function renderBoard(board) {
        cells.forEach((cell, index) => {
            cell.textContent = board[index] === '-' ? '' : board[index];
        });
    }
});

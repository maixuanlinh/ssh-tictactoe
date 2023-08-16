// The entire script waits for the DOM content to be loaded before executing.
document.addEventListener("DOMContentLoaded", function () {

    // Getting references to startChoiceDropdown.
    const startChoiceDropdown = document.getElementById("startChoice");
  
    // Reset button functionality: Refreshes the page.
    const resetButton = document.getElementById("reset");
    resetButton.addEventListener("click", function () {
      location.reload();
    });
  
    // Handle initial dropdown's default value.
    computerStartFirstHandler(startChoiceDropdown.value);
  
    // Attach event listener to dropdown for game start choice.
    startChoiceDropdown.addEventListener("change", function () {
      computerStartFirstHandler(startChoiceDropdown.value);
    });
  
    // Determines action the computer starts first.
    function computerStartFirstHandler(value) {
      if (value === "computer") {
        // If 'computer' is selected, start a new game with the computer playing first.
        startNewGame(-1);
      }
    }
  
    // Reference to all cells in the tic-tac-toe board.
    const cells = document.querySelectorAll(".cell");
    let currentGameId = null;
  
    // Attach click event listeners to each cell.
    cells.forEach((cell) => {
      cell.addEventListener("click", function (e) {
        // Only proceed if cell is empty.
        if (!e.target.textContent) {
          makeMove(e.target.dataset.index);
        }
      });
    });
  
    // Handles a move on the board, either starting a new game or updating an existing one.
    function makeMove(index) {
      if (!currentGameId) {
        startNewGame(index);
      } else {
        updateGame(index);
      }
    }
  
    // Starts a new game, handing two senarios if computer or player plays first.
    function startNewGame(index) {
      let board = "---------";
  
      // Set the first move if not initiated by computer (if initiated by computer, index will be -1).
      if (index !== -1) {
        mark = startChoiceDropdown.value === "computer" ? "o" : "x";
        board = setMoveOnBoard(board, index, mark);
      }
  
      // API call to start a new game.
      fetch("/api/v1/games", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ board: board }),
      })
        .then((response) => response.json())
        .then((data) => {
          currentGameId = data.id; // Storing the game's ID for future reference.
          // Render the board UI and show game result message.
          renderBoard(data.board);
        })
        .catch((error) => console.error("Error starting a new game:", error));
    }
  
    // Updates the game state after a move.
    function updateGame(index) {
      // Fetch current game state.
      fetch(`/api/v1/games/${currentGameId}`)
        .then((response) => response.json())
        .then((data) => {
          let board = data.board;
  
          // Determine the mark ('x' or 'o') for the player.
          mark = startChoiceDropdown.value === "computer" ? "o" : "x";
          // then set the move on the board with the player's mark (o or x)
          board = setMoveOnBoard(board, index, mark);
  
          // Update game state with the new board.
          return fetch(`/api/v1/games/${currentGameId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ board: board }),
          });
        })
        .then((response) => response.json())
        .then((data) => {
          // Render updated board and show game result message.
          if (data.board) {
            renderBoard(data.board);
            updateGameResultMessage(data.status);
          } else {
            console.error("No board data received after PUT request:", data);
          }
        })
        .catch((error) => {
          console.error("Error encountered during updateGame:", error);
        });
    }
  
    // Updates the displayed game result based on the game's status.
    function updateGameResultMessage(status) {
      let resultMessage = document.getElementById("resultMessage");
      if (status !== "RUNNING") {
        let displayedMessage = "";
        switch (status) {
          case "X_WON":
            displayedMessage = "X WON!";
            break;
          case "O_WON":
            displayedMessage = "O WON!";
            break;
          case "DRAW":
            displayedMessage = "IT'S A DRAW!";
            break;
        }
        resultMessage.innerHTML = displayedMessage;
      } else {
        resultMessage.innerHTML = " ";
      }
    }
  
    // Helper function to set a move on a given board state.
    function setMoveOnBoard(board, index, move) {
        
        //convert board string to array for easier manipulation. I have tried with slice() method but seems a bit problematic. This one works fine.
      let boardArray = Array.from(board);
      boardArray[index] = move;
      return boardArray.join("");
    }
  
    // Renders the board based on a given board state.
    function renderBoard(board) {
      cells.forEach((cell, index) => {
        cell.textContent = board[index] === "-" ? "" : board[index];
        // Set colors for each type of mark.
        if (cell.textContent === "x") {
          cell.style.color = "red";
        } else {
          cell.style.color = "green";
        }
      });
    }
  });
  
class BoggleGame {
    constructor(boardId, seconds = 60) {
        this.board = $("#" + boardId);
        this.words = new Set();
        this.score = 0;
        this.seconds = seconds;
        this.showTimer();
        this.timer = setInterval(this.tick.bind(this), 1000);

        // Bind event listener
        $(".add-word").on("submit", this.handleSubmit.bind(this));
    }

    // Handle word submission
    async handleSubmit(event) {
        event.preventDefault();
        const word = $(".word").val().trim();

        if (!word) return;

        if (this.words.has(word)) {
            this.showMessage(`Already found "${word}"`, "warning");
            return;
        }

        // Make AJAX request to check if the word is valid
        let response;
        try {
            response = await axios.post("/submit_guess", { guess: word });
        } catch (error) {
            this.showMessage("Error submitting word, please try again.", "error");
            console.error("Error:", error);
            return;
        }

        // Process the response from the server
        if (response.data.result === "ok") {
            this.words.add(word);
            this.updateScore(word.length);
            this.showMessage(`Added "${word}"`, "success");
            this.showWords(word);
        } else if (response.data.result === "not-on-board") {
            this.showMessage(`"${word}" is not on the board`, "error");
        } else if (response.data.result === "not-word") {
            this.showMessage(`"${word}" is not a valid word`, "error");
        }

        $(".word").val(""); // Clear input
    }

    // Display submitted words in the word list
    showWords(word) {
        $(".words").append($("<li>").text(word));
    }

    // Update the displayed score
    updateScore(points) {
        this.score += points;
        $(".score").text(this.score);
    }

    // Show messages to the player
    showMessage(msg, cls) {
        $(".msg").text(msg).removeClass().addClass(`msg ${cls}`);
    }

    // Show the countdown timer
    showTimer() {
        $(".timer").text(this.seconds);
    }

    // Tick down the timer
    async tick() {
        this.seconds -= 1;
        this.showTimer();

        if (this.seconds === 0) {
            clearInterval(this.timer);
            await this.endGame();
        }
    }

    // End the game and send final score to the server if needed
    async endGame() {
        $(".add-word").hide();
        this.showMessage(`Game over! Final score: ${this.score}`, "info");

        let response;
        try {
            response = await axios.post("/end_game", { score: this.score });
            $("#highscore").text(response.data.highscore);
            $("#nplays").text(response.data.nplays);
        } catch (error) {
            console.error("Error ending game:", error);
        }
    }
}

// Initialize game on document ready
$(document).ready(function () {
    const game = new BoggleGame("boggle", 60);
});
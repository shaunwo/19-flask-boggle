class BoggleGame {
  /* Create a new game board at this DOM id */
  constructor(boardId, secs = 60) {
    this.secs = secs;
    this.showTimer();

    this.score = 0;
    this.words = new Set();
    this.board = $('#' + boardId);

    // counting down on the timer
    this.timer = setInterval(this.tick.bind(this), 1000);

    // checking the word submitted
    $('.add-word', this.board).on('submit', this.handleSubmit.bind(this));
  }

  /* add to list of words on screen */
  showWord(word) {
    $('.words', this.board).append($('<li>', { text: word }));
  }

  /* display the current score on the screen */
  showScore() {
    $('.score', this.board).text(this.score);
  }

  /* displaying a status message */
  showMessage(msg, cls) {
    $('.msg', this.board).text(msg).removeClass().addClass(`msg ${cls}`);
  }

  /* handling word submission of word- if it's unique and valid, increase score & show on screen */
  async handleSubmit(evt) {
    evt.preventDefault();
    const $word = $('.word', this.board);

    let word = $word.val();
    if (!word) return;

    // checking that the work entered hasn't already been submitted
    if (this.words.has(word)) {
      this.showMessage(`Already found ${word}`, 'err');
      return;
    }

    // check server for validity if the word
    const resp = await axios.get('/check-word', { params: { word: word } });
    if (resp.data.result === 'not-word') {
      this.showMessage(`${word} is not a valid English word`, 'error');
    } else if (resp.data.result === 'not-on-board') {
      this.showMessage(`${word} is not a valid word on this board`, 'error');
    } else {
      this.showWord(word);
      this.score += word.length;
      this.showScore();
      this.words.add(word);
      this.showMessage(`Added: ${word}`, 'success');
    }

    // putting the cursor back in the form field for the next word guess
    $word.val('').focus();
  }

  /* showing the timer on the screen */
  showTimer() {
    ('.timer', this.board).text(this.secs);
  }

  /* decerementing the counter */
  async tick() {
    this.secs -= 1;
    this.showTimer();

    if (this.secs === 0) {
      clearInterval(this.timer);
      await this.scoreGame();
    }
  }

  /* handling the end of the game, disabling any further play and displaying score / new record on screen */
  async scoreGame() {
    $('.add-word', this.board).hide();
    const resp = await axios.post('/post-score', { score: this.score });
    if (resp.data.brokeRecord) {
      this.showMessage(`New record: ${this.score}`, 'success');
    } else {
      this.showMessage(`Final score: ${this.score}`, 'success');
    }
  }
}

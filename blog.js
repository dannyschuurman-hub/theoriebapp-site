document.querySelectorAll('.quiz').forEach(quiz => {
  const feedback = quiz.querySelector('.feedback');
  quiz.querySelectorAll('.answer').forEach(button => {
    button.addEventListener('click', () => {
      quiz.querySelectorAll('.answer').forEach(option => {
        option.classList.remove('is-correct', 'is-wrong');
        option.setAttribute('aria-pressed', String(option === button));
      });
      const correct = button.dataset.correct === 'true';
      button.classList.add(correct ? 'is-correct' : 'is-wrong');
      if (!correct) quiz.querySelector('[data-correct="true"]').classList.add('is-correct');
      feedback.hidden = false;
      feedback.classList.toggle('wrong', !correct);
      feedback.querySelector('.verdict').textContent = correct ? (quiz.dataset.goed || 'Goed gezien.') : (quiz.dataset.fout || 'Nog niet goed. Dit is de regel:');
    });
  });
});

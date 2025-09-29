// Faz os alertas sumirem automaticamente
setTimeout(() => {
  document.querySelectorAll('.alert-fixed').forEach(e => e.remove());
}, 3000);

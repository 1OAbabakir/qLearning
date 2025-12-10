(function(){
    const key = 'study_note_card_{{ card.id }}';
    const area = document.getElementById('study-note');
    if (!area) return;
    try {
      const saved = localStorage.getItem(key);
      if (saved !== null) area.value = saved;
    } catch(e) {}
    area.addEventListener('input', function(){
      try { localStorage.setItem(key, area.value); } catch(e) {}
    });
  })();
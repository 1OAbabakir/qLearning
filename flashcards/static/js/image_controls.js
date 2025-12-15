document.addEventListener('DOMContentLoaded', function(){
  const img = document.getElementById('card-image');
  if(!img) return;
  let rotate = 0;
  let width = 600;

  function update(){
    const params = new URLSearchParams();
    if(rotate) params.set('rotate', rotate);
    if(width) params.set('w', width);
    img.src = `/card/${img.getAttribute('data-card-id') || img.src.split('/card/')[1].split('/')[0]}/image/?${params.toString()}&t=${Date.now()}`;
  }

  document.getElementById('rotate-left').addEventListener('click', function(e){ e.preventDefault(); rotate = (rotate - 90) % 360; update(); });
  document.getElementById('rotate-right').addEventListener('click', function(e){ e.preventDefault(); rotate = (rotate + 90) % 360; update(); });
  document.getElementById('zoom-in').addEventListener('click', function(e){ e.preventDefault(); width = Math.min(2000, Math.round(width * 1.25)); update(); });
  document.getElementById('zoom-out').addEventListener('click', function(e){ e.preventDefault(); width = Math.max(50, Math.round(width * 0.8)); update(); });
  document.getElementById('thumb').addEventListener('click', function(e){ e.preventDefault(); const params = new URLSearchParams(); params.set('thumb','1'); img.src = `/card/${img.getAttribute('data-card-id') || img.src.split('/card/')[1].split('/')[0]}/image/?${params.toString()}&t=${Date.now()}`; });

});

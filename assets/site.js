
(function(){
  var root=document.documentElement;
  root.classList.add('js');
  /* header turns solid after the opening */
  var hd=document.querySelector('header');var isHome=!!document.getElementById('op-bg');
  function onScroll(){
    var y=window.scrollY||0;
    if(isHome)hd.classList.toggle('solid',y>window.innerHeight*0.6);
    var bg=document.getElementById('op-bg');
    if(bg&&y<window.innerHeight*1.2&&!window.matchMedia('(prefers-reduced-motion: reduce)').matches) bg.style.transform='translate3d(0,'+(y*0.35)+'px,0)';
  }
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();
  /* reveal */
  var rvs=document.querySelectorAll('.rv,.rv-img');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});
    rvs.forEach(function(el){io.observe(el)});
  } else rvs.forEach(function(el){el.classList.add('in')});
  /* lightbox */
  var lb=document.getElementById('lb'),lbImg=document.getElementById('lb-img'),lbCap=document.getElementById('lb-cap'),lbTitle=document.getElementById('lb-title'),lbCount=document.getElementById('lb-count');
  var group=[],idx=0;
  function capOf(img){var f=img.closest('figure');var c=f&&f.querySelector('figcaption');if(c){var sp=c.querySelector('[lang="'+root.lang+'"]');return (sp||c).textContent.trim()}return img.alt||''}
  function titleOf(img){var pv=img.closest('.pv-panel');if(pv)return 'Pavilion '+pv.querySelector('.pv-name').textContent.trim();var it=img.closest('.item');if(it){var n=it.querySelector('.name');if(n)return n.textContent.trim()}var sec=img.closest('section');var h=sec&&sec.querySelector('h2');return h?h.textContent.trim():'Bonomelli Estate'}
  function show(i){idx=(i+group.length)%group.length;var im=group[idx];lbImg.src=im.currentSrc||im.src;lbImg.alt=im.alt;lbImg.style.animation='none';void lbImg.offsetWidth;lbImg.style.animation='';lbCap.textContent=capOf(im);lbTitle.textContent=titleOf(im);lbCount.textContent=group.length>1?(idx+1)+' / '+group.length:'';document.getElementById('lb-prev').hidden=document.getElementById('lb-next').hidden=group.length<2}
  function open(img){var scope=img.closest('.pv-panel,.fbody,#serra .plates,.aepanel,[data-gallery]')||img.parentNode;if(img.closest('.aepanel'))scope=img.closest('.aepanel');group=Array.prototype.slice.call(scope.querySelectorAll('figure img'));show(group.indexOf(img));lb.hidden=false;document.body.style.overflow='hidden';document.getElementById('lb-close').focus()}
  function close(){lb.hidden=true;document.body.style.overflow=''}
  document.querySelector('main').addEventListener('click',function(e){var im=e.target.closest('figure img');if(im&&!im.closest('.opening')&&!im.closest('a'))open(im)});
  document.getElementById('lb-close').addEventListener('click',close);
  document.getElementById('lb-prev').addEventListener('click',function(){show(idx-1)});
  document.getElementById('lb-next').addEventListener('click',function(){show(idx+1)});
  lb.addEventListener('click',function(e){if(e.target===lb||e.target.id==='lb-stage')close()});
  document.addEventListener('keydown',function(e){if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(idx-1);if(e.key==='ArrowRight')show(idx+1)});
  var sx=null;var st=document.getElementById('lb-stage');
  st.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});
  st.addEventListener('touchend',function(e){if(sx===null)return;var dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>45)show(idx+(dx<0?1:-1));sx=null});

  function setLang(l){
    root.setAttribute('lang',l);
    document.querySelectorAll('.lang button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.l===l?'true':'false')});
    try{localStorage.setItem('be-lang',l)}catch(e){}
  }
  var saved=null;try{saved=localStorage.getItem('be-lang')}catch(e){}
  setLang(saved==='en'?'en':'it');
  document.querySelectorAll('.lang button').forEach(function(b){b.addEventListener('click',function(){setLang(b.dataset.l)})});

  document.addEventListener('contextmenu',function(e){if(e.target.closest('img,video'))e.preventDefault()});
  document.addEventListener('dragstart',function(e){if(e.target.closest('img,video'))e.preventDefault()});
  document.querySelectorAll('video').forEach(function(v){v.setAttribute('controlsList','nodownload');v.setAttribute('disablePictureInPicture','')});

  document.querySelectorAll('.snd').forEach(function(b){
    var v=b.parentNode.querySelector('video');
    b.addEventListener('click',function(){
      var on=v.muted;
      document.querySelectorAll('.snd').forEach(function(o){var ov=o.parentNode.querySelector('video');if(o!==b){ov.muted=true;o.setAttribute('aria-pressed','false')}});
      v.muted=!on;b.setAttribute('aria-pressed',on?'true':'false');
      if(on){try{v.currentTime=0;var p=v.play();if(p&&p.catch)p.catch(function(){})}catch(e){}}
    });
  });


  /* enquiry form -> Supabase */
  var SB='https://klxcmojwmjilklfoqzhp.supabase.co',KEY='sb_publishable_ft-DNpTfQMfHfw08NEvsPg_nIsqkiHR';
  /* mobile menu */
  var mb=document.getElementById('menu-btn');
  if(mb){mb.addEventListener('click',function(){var o=root.classList.toggle('nav-open');mb.setAttribute('aria-expanded',o?'true':'false');document.body.style.overflow=o?'hidden':''});
    document.querySelectorAll('#nav a').forEach(function(a){a.addEventListener('click',function(){root.classList.remove('nav-open');document.body.style.overflow=''})});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&root.classList.contains('nav-open')){root.classList.remove('nav-open');mb.setAttribute('aria-expanded','false');document.body.style.overflow=''}});}
  var form=document.getElementById('enq'),st=document.getElementById('f-status'),btn=document.getElementById('f-send');
  if(form){
  function T(it,en){return root.lang==='en'?en:it}
  function relabel(){document.querySelectorAll('option[data-it]').forEach(function(o){o.textContent=root.lang==='en'?o.dataset.en:o.dataset.it})}
  relabel();document.querySelectorAll('.lang button').forEach(function(b){b.addEventListener('click',relabel)});
  form.addEventListener('submit',function(e){
    e.preventDefault();st.className='f-msg';st.textContent='';
    var v=function(id){return document.getElementById(id).value.trim()};
    var bad=[];
    [['f-nome',v('f-nome').length>=2],['f-email',/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v('f-email'))],['f-tipo',!!v('f-tipo')],['f-privacy',document.getElementById('f-privacy').checked]].forEach(function(c){document.getElementById(c[0]).setAttribute('aria-invalid',c[1]?'false':'true');if(!c[1])bad.push(c[0])});
    if(bad.length){st.classList.add('err');st.textContent=T('Completi i campi segnati: nome, email valida, tipo di richiesta e consenso privacy.','Please complete the marked fields: name, a valid email, request type and privacy consent.');document.getElementById(bad[0]).focus();return}
    if(v('f-web')){st.classList.add('ok');st.textContent=T('Grazie.','Thank you.');return}
    var data={nome:v('f-nome'),email:v('f-email'),telefono:v('f-tel')||null,paese:v('f-paese')||null,tipo:v('f-tipo'),profilo:v('f-profilo')||null,progetto:v('f-progetto')||null,canale_preferito:v('f-canale')||null,fonte:v('f-fonte')||null,messaggio:v('f-msg')||null,lingua:root.lang==='en'?'en':'it',consenso_privacy:true};
    btn.disabled=true;st.textContent=T('Invio in corso…','Sending…');
    fetch(SB+'/rest/v1/richieste',{method:'POST',headers:{'apikey':KEY,'Content-Type':'application/json','Prefer':'return=minimal'},body:JSON.stringify(data)})
    .then(function(r){if(!r.ok)throw new Error(r.status);form.reset();relabel();st.classList.add('ok');st.textContent=T('Grazie. La sua richiesta è arrivata allo studio: le risponderemo personalmente.','Thank you. Your enquiry has reached the studio: we will reply to you personally.')})
    .catch(function(){st.classList.add('err');st.textContent=T('Non è stato possibile inviare la richiesta. Scriva a studio@bonomelliestate.it o su WhatsApp al +39 351 657 5517.','Your enquiry could not be sent. Please write to studio@bonomelliestate.it or on WhatsApp at +39 351 657 5517.')})
    .finally(function(){btn.disabled=false});
  });
  var PJ={bonomelli:'Pavilion Bonomelli',caelo:'Pavilion Caelo',magnolia:'Pavilion Magnolia',rome:'Pavilion Rome',dhier:'Pavilion D\u2019Hier',forestier:'Pavilion Forestier',airfrais:'Pavilion Air Frais',serra:'Serra dei Sogni'};
  var hm=(location.hash||'').match(/^#(dossier|consulenza)(?:-([a-z]+))?$/);
  if(hm){document.getElementById('f-tipo').value=hm[1];if(hm[2]&&PJ[hm[2]])document.getElementById('f-progetto').value=PJ[hm[2]];setTimeout(function(){form.scrollIntoView({block:'start'})},50)}
  }
  var pvt=document.querySelectorAll('[data-pv][role="tab"]');
  pvt.forEach(function(t){t.addEventListener('click',function(){
    pvt.forEach(function(x){x.setAttribute('aria-selected',x===t?'true':'false')});
    document.querySelectorAll('.pv-panel').forEach(function(p){p.hidden=p.dataset.pv!==t.dataset.pv;if(!p.hidden)p.querySelectorAll('.rv-img').forEach(function(f){f.classList.add('in')})});
  })});
  var aet=document.querySelectorAll('[data-ae][role="tab"]');
  aet.forEach(function(t){t.addEventListener('click',function(){
    aet.forEach(function(x){x.setAttribute('aria-selected',x===t?'true':'false')});
    document.querySelectorAll('.aepanel').forEach(function(p){p.hidden=p.dataset.ae!==t.dataset.ae});
  })});


  /* COROLLA: tre versioni, stesse due viste */
  var ct=document.querySelectorAll('[data-c][role="tab"]');
  var cnote={base:['La seduta poggia su un anello di pietra, come un fiore sul suo vaso.','The seat rests on a stone ring, like a flower on its vase.'],guscio:['La pietra avvolge la seduta come un calice; i petali dello schienale sono arrotondati.','Stone wraps the seat like a chalice; the back petals are rounded.'],affilato:['Lo stesso guscio di pietra, con i petali dello schienale più slanciati e appuntiti.','The same stone shell, with slimmer, pointed back petals.']};
  ct.forEach(function(t){t.addEventListener('click',function(){
    ct.forEach(function(x){x.setAttribute('aria-selected',x===t?'true':'false')});
    var v=t.dataset.c;document.getElementById('c1').src='img/corolla-'+v+'-1.webp';document.getElementById('c2').src='img/corolla-'+v+'-2.webp';
    var n=document.getElementById('c-note');n.children[0].textContent=cnote[v][0];n.children[1].textContent=cnote[v][1];
  })});
  var tabs=document.querySelectorAll('#serra .variants button');
  var p=[document.getElementById('p1'),document.getElementById('p2'),document.getElementById('p3')];
  var parts=['galleria','alto','dettaglio'];
  tabs.forEach(function(t){t.addEventListener('click',function(){
    tabs.forEach(function(x){x.setAttribute('aria-selected',x===t?'true':'false')});
    p.forEach(function(img,i){img.src='img/'+t.dataset.v+'-'+parts[i]+'.webp'});
  })});
})();

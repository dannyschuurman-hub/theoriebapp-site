(() => {
 'use strict';
 const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
 const english = document.documentElement.lang === 'en';
 const passedText = english ? '44 pass mark reached.' : 'Grens van 44 gehaald.';
 const progressText = english ? 'On the way to 44.' : 'Op weg naar 44.';
 const preference = matchMedia('(prefers-reduced-motion: reduce)');
 const clamp = x => Math.max(0,Math.min(1,x));
 const range = (x,a,b) => clamp((x-a)/(b-a));
 const ease = x => 1-Math.pow(1-x,3);
 const sections = ['hero','exam','result','pan','language'];
 let bounds = {}, vh = innerHeight, panDistance = 0, pending = false, previousQuestion = -1, previousAnswer = null, previousCount = -1, manualLanguage = false, language = english ? 'en' : 'nl';
 const hero=$('.hero'),scene=$('.scene'),title=$('.hero-title'),far=$('.far'),near=$('.hero .near'),heroPhone=$('.hero-phone'),flash=$('.flash'),examPhone=$('.exam-phone'),landing=$('.landing-flash'),captions=$$('.captions article'),questions=$$('.exam-phone .question'),dots=$$('.result-dot'),score=$('#score-count'),threshold=$('#threshold'),scoreCard=$('.score-card'),track=$('.topic-track');
 function setLanguage(lang) {
  language=lang;
  $$('.language-phone .question').forEach(el=>{const hidden=!el.classList.contains('language-'+lang);el.inert=hidden;el.setAttribute('aria-hidden',String(hidden));});
  $('.language-phone').classList.toggle('is-en',lang==='en');
  $$('.language-switch button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.lang===lang)));
 }
 $$('.language-switch button').forEach(b=>b.addEventListener('click',()=>{manualLanguage=true;setLanguage(b.dataset.lang);}));
 function measureCopy() {
  const box=$('.captions');
  box.style.minHeight='0px';
  box.style.minHeight=Math.ceil(Math.max(...captions.map(el=>el.getBoundingClientRect().height)))+'px';
  $('.exam-stage').style.setProperty('--exam-copy-height',Math.ceil($('.exam-copy').getBoundingClientRect().height)+'px');
  $('.language-stage').style.setProperty('--language-copy-height',Math.ceil($('.language-stage>div:first-child').getBoundingClientRect().height)+'px');
 }
 function measure() {
  measureCopy();
  vh=innerHeight;
  sections.forEach(name=>{const e=$('.'+name);bounds[name]={top:e.offsetTop,length:Math.max(1,e.offsetHeight-vh)};});
  panDistance=Math.max(0,track.scrollWidth-innerWidth);
  queue();
 }
 function progress(name){return clamp((scrollY-bounds[name].top)/bounds[name].length);}
 function draw() {
  pending=false;
  if(preference.matches)return;
  const h=progress('hero'), p=progress('exam'), r=progress('result');
  if(scrollY<bounds.exam.top+vh) {
   title.style.transform=`translateY(${h*vh*.42}px)`;
   far.style.transform=`translateY(${-h*vh*.06}px) scale(${1+h*.05})`;
   near.style.transform=`translateY(${h*vh*.09}px) scale(${1+h*.15})`; $('.green-foreground img').style.transform=near.style.transform;
   scene.style.transform=`scale(${1+ease(range(h,.53,1))*1.4})`;
   $('.hero-caption').style.opacity=1-range(h,.1,.35);$('.hero-note').style.opacity=1-range(h,.1,.35);
   heroPhone.style.opacity=range(h,.35,.5);
   heroPhone.style.transform=`translateY(${(1-ease(range(h,.35,.65)))*180}px) rotate(${-12*(1-range(h,.5,.8))}deg) scale(${1+range(h,.68,1)*18})`;
   flash.style.opacity=range(h,.85,.98);
   $('.green-foreground').style.opacity=1-range(h,.05,.22);
  }
  if(scrollY>bounds.exam.top-vh&&scrollY<bounds.exam.top+bounds.exam.length+vh) {
   const land=ease(range(p,0,.055));
   examPhone.style.transform=`scale(${1+(1-land)*5})`;
   landing.style.opacity=1-range(p,0,.025);
   const q=Math.min(2,Math.floor(range(p,.065,1)*3));
   const local=(range(p,.065,1)*3)-q;
   if(q!==previousQuestion){questions.forEach((e,i)=>{e.style.opacity=i===q?1:0;e.setAttribute('aria-hidden',String(i!==q));e.inert=i!==q;});captions.forEach((e,i)=>{e.style.opacity=i===q?1:0;e.setAttribute('aria-hidden',String(i!==q));});previousQuestion=q;previousAnswer=null;measureCopy();}
   const answer=local>.28;
   if(answer!==previousAnswer){questions[q].classList.toggle('answered',answer);previousAnswer=answer;}
   const explanation=range(local,.47,.62),el=questions[q].querySelector('.explanation');el.style.opacity=explanation;el.style.transform=`translateY(${(1-explanation)*14}px)`;
  }
  const count=Math.round(range(r,.04,.88)*50);
  if(count!==previousCount){dots.forEach((d,i)=>d.classList.toggle('filled',i<count));const correct=Math.min(49,count);score.textContent=correct;scoreCard.classList.toggle('passed',correct>=44);threshold.textContent=correct>=44?passedText:progressText;previousCount=count;}
  track.style.transform=`translateX(${-progress('pan')*panDistance}px)`;
  if(!manualLanguage){const target=progress('language')>.45?(english?'nl':'en'):(english?'en':'nl');if(target!==language)setLanguage(target);}
 }
 function queue(){if(!pending){pending=true;requestAnimationFrame(draw);}}
 function setup(){
  setLanguage(language);
  document.documentElement.classList.toggle('motion',!preference.matches);
  if(preference.matches){score.textContent='49';threshold.textContent=passedText;scoreCard.classList.add('passed');return;}
  measure();
 }
 addEventListener('scroll',queue,{passive:true});addEventListener('resize',measure,{passive:true});addEventListener('load',measure);preference.addEventListener('change',()=>location.reload());
 setup();if(document.fonts)document.fonts.ready.then(measure);
})();

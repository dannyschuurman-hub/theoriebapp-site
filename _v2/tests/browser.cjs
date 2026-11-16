const {chromium}=require('/Users/dannyschuurman/Developer/gratisadvocaat/node_modules/playwright-core');
const fs=require('fs');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 const report=[];
 for(const [w,h,reduced] of [[390,844,false],[1440,900,false],[360,800,false],[5120,1440,false],[390,844,true],[1440,900,true]]){
  const page=await browser.newPage({viewport:{width:w,height:h},reducedMotion:reduced?'reduce':'no-preference'}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error') errors.push(m.text())});
  await page.goto('http://127.0.0.1:8765/_v2/',{waitUntil:'networkidle'});
  const shots=[];let overflow=false;
  for(const [section,progresses] of [['hero',[0,.45,.8]],['exam',[.12,.3,.47,.62,.8,.95]],['result',[.1,.77,.9]],['pan',[0,.5,1]],['language',[0,.7]],['blogs',[0]],['download',[0]]]){
   for(const p of progresses){await page.evaluate(({section,p})=>{const el=document.querySelector('.'+section);scrollTo(0,el.offsetTop+Math.max(0,el.offsetHeight-innerHeight)*p)},{section,p});await page.waitForTimeout(90);
    overflow ||= await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
    if([390,1440].includes(w)&&!reduced){const path=`_v2/tests/${w}-${section}-${p}.jpg`;await page.screenshot({path,quality:68});shots.push(path);}
   }
  }
  await page.locator('[data-lang="en"]').click();const english=await page.locator('.language-phone').evaluate(el=>el.classList.contains('is-en'));
  await page.locator('[data-lang="nl"]').click();const dutch=await page.locator('[data-lang="nl"]').getAttribute('aria-pressed');
  const broken=await page.locator('img').evaluateAll(imgs=>imgs.filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src));
  report.push({w,h,reduced,overflow,errors,broken,english,dutch,shots});await page.close();
 }
 fs.writeFileSync('_v2/tests/browser-report.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report.map(({shots,...r})=>r),null,2));await browser.close();
})();

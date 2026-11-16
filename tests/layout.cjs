// Real browser geometry: each question, both translations, responsive and reduced motion.
const {chromium}=require('/Users/dannyschuurman/Developer/gratisadvocaat/node_modules/playwright-core');
const assert=require('node:assert/strict'),fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 const report=[];
 try {
 for(const [w,h] of [[1440,900],[375,812]]) for(const lang of ['nl','en']) for(const reduced of [false,true]) {
  const page=await browser.newPage({viewport:{width:w,height:h},reducedMotion:reduced?'reduce':'no-preference'}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
  await page.goto('http://127.0.0.1:8765/'+(lang==='en'?'en/':''),{waitUntil:'networkidle'});
  await page.evaluate(()=>document.fonts.ready);
  const measurements=[];
  for(const p of [.12,.3,.4,.6,.72,.94]) {
   await page.evaluate(p=>{document.documentElement.style.scrollBehavior='auto';const e=document.querySelector('.exam');scrollTo(0,e.offsetTop+(e.offsetHeight-innerHeight)*p)},p);
   await page.waitForTimeout(100);
   const m=await page.evaluate(()=>{
    const r=e=>{const b=e.getBoundingClientRect();return {top:b.top,bottom:b.bottom,left:b.left,right:b.right,height:b.height}};
    const articles=[...document.querySelectorAll('.captions article')].filter(e=>getComputedStyle(e).opacity==='1');
    const label=r(document.querySelector('.demo-label'));
    const captions=articles.map(e=>({head:r(e.querySelector('h2')),paragraph:r(e.querySelector('p'))}));
    const phones=[...document.querySelectorAll('.exam-phone .question')].filter(e=>getComputedStyle(e).opacity==='1').map(e=>({content:r(e.querySelector('.question-content')),footer:r(e.querySelector('.app-bottom'))}));
    return {captions,label,phones,overflow:document.documentElement.scrollWidth>innerWidth};
   });
   assert(!m.overflow,'Horizontal overflow');
   for(const c of m.captions){assert(c.head.bottom<=c.paragraph.top+1,'Heading overlaps paragraph');assert(c.paragraph.bottom<=m.label.top+1,'Paragraph overlaps caption');}
   for(const q of m.phones)assert(q.content.bottom<=q.footer.top+1,'Question overlaps footer');
   measurements.push(m);
  }
  for(const selected of ['nl','en']) {
   await page.locator(`[data-lang="${selected}"]`).click();
   const fit=await page.locator('.language-'+selected).evaluate(e=>{
    const c=e.querySelector('.question-content'),f=e.querySelector('.app-bottom');
    c.scrollTop=c.scrollHeight;
    const x=e.querySelector('.explanation').getBoundingClientRect();
    return {bottom:c.getBoundingClientRect().bottom,footer:f.getBoundingClientRect().top,explanation:x.bottom,clip:getComputedStyle(c).overflowY};
   });
   assert(fit.bottom<=fit.footer+1,'Language content overlaps bottom bar');
   assert(fit.explanation<=fit.bottom+1,'Explanation cannot be scrolled into view');
  }
  // Trigger lazy images, then collect broken files and JavaScript/CSP failures.
  await page.locator('.home-magazine').scrollIntoViewIfNeeded();await page.waitForTimeout(200);
  const broken=await page.locator('img').evaluateAll(xs=>xs.filter(x=>x.complete&&!x.naturalWidth).map(x=>x.src));
  assert.deepEqual(broken,[]);assert.deepEqual(errors,[]);
  await page.screenshot({path:`/tmp/theorieb-${lang}-${w}-${reduced}.png`,fullPage:false});
  report.push({w,h,lang,reduced,measurements});await page.close();
 }
 fs.writeFileSync('_v2/tests/layout-report.json',JSON.stringify(report,null,2));
 console.log('PASS: all question transitions, NL/EN phone clipping, desktop/mobile, reduced motion, assets and console');
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});

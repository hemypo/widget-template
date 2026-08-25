const { chromium } = require('playwright');
const fs=require('fs'), path=require('path');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
 const dir='/home/claude/tenet-widget/build/_preview';
 for(const f of fs.readdirSync(dir).filter(x=>x.endsWith('.html'))){
   const mobile=f.includes('mobile');
   const p=await b.newPage({viewport:{width:mobile?454:964,height:900},deviceScaleFactor:2});
   await p.goto('file://'+path.join(dir,f));
   await p.waitForTimeout(250);
   await p.screenshot({path:path.join(dir,f.replace('.html','.png')),fullPage:true});
   await p.close();
 }
 await b.close();
})();

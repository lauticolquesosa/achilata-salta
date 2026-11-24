import puppeteer from "puppeteer-core";
const b = await puppeteer.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true });
let f=0; const ok=(c,m)=>{console.log((c?"OK    ":"FALLA ")+m); if(!c)f++;};
// hora de Salta -> ms UTC
const salta=(iso)=>Date.parse(iso+"-03:00");
async function abrir(iso, vp={width:1280,height:900}){
  const p=await (await b.createBrowserContext()).newPage(); await p.setViewport(vp);
  const err=[]; p.on("pageerror",e=>err.push(e.message)); p.on("console",m=>{if(m.type()==="error")err.push(m.text())});
  await p.evaluateOnNewDocument((ms)=>{sessionStorage.setItem("achilata_visto","1");localStorage.setItem("achilata_privacidad",JSON.stringify({v:1,necesarias:true,medicion:false,fecha:Date.now()}));window.__ahoraSalta=ms;window.__ab=[];window.open=(u)=>{window.__ab.push(u);return {}};}, salta(iso));
  await p.goto("http://127.0.0.1:8765/pedir.html",{waitUntil:"load"}); p.err=err; return p;
}
const turnos=(p)=>p.$$eval("#pd-turnos input",l=>l.map(i=>i.value));
const dia0=(p)=>p.$eval("#pd-dia option",o=>o.textContent);
// jueves 26/11 a las 12:00: tarde y noche
let p=await abrir("2026-11-26T12:00:00");
ok((await dia0(p)).startsWith("Hoy"),"Jueves 12:00 el primer día es hoy → "+await dia0(p));
ok((await turnos(p)).join()==="tarde,noche","Jueves 12:00: tarde y noche → "+await turnos(p));
ok((await p.$$eval("#pd-dia option",o=>o.length))===7,"Siete días para elegir");
ok(p.err.length===0,"Sin errores "+p.err.join(" | "));
// jueves 14:00: solo noche
p=await abrir("2026-11-26T14:00:00"); ok((await turnos(p)).join()==="noche","Jueves 14:00: solo noche → "+await turnos(p));
// jueves 18:30: hoy no aparece, mañana viernes
p=await abrir("2026-11-26T18:30:00"); ok((await dia0(p)).startsWith("Mañana, viernes"),"Jueves 18:30 arranca mañana → "+await dia0(p));
// domingo 9:00: mediodía, tarde y noche
p=await abrir("2026-11-29T09:00:00"); ok((await turnos(p)).join()==="mediodia,tarde,noche","Domingo 9:00 → "+await turnos(p));
// lunes 10:00: único
p=await abrir("2026-11-30T10:00:00"); ok((await turnos(p)).join()==="unico","Lunes → "+await turnos(p));
// mínimo y envío
p=await abrir("2026-11-26T12:00:00");
await p.click('[data-mas="kg1"][data-paso="-1"]');
await p.type("#pd-nombre","Ana"); await p.type("#pd-direccion","Los Ceibos 123");
await p.click('button[type="submit"]');
ok((await p.$eval("#error-pedir",e=>e.textContent)).includes("al menos un pote"),"Sin potes pide sumar uno");
ok((await p.evaluate(()=>window.__ab.length))===0,"No abre WhatsApp sin potes");
await p.click('[data-mas="kg1"][data-paso="1"]');
await p.click('[data-mas="kg05"][data-paso="1"]');
ok((await p.$eval("#pd-total",e=>e.textContent))==="$20.000","1 kg y medio = $20.000");
await p.click('input[name="pago"][value="efectivo"]');
ok(!(await p.$eval("#pd-con-caja",e=>e.hidden)),"Efectivo muestra con cuánto pagás");
await p.type("#pd-con","25000");
await p.click('input[name="turno"][value="noche"]');
await p.click('button[type="submit"]');
const u=await p.evaluate(()=>window.__ab[0]||""); const msg=decodeURIComponent(new URL(u).searchParams.get("text")||"");
console.log(msg);
ok((await p.evaluate(()=>window.__ab.length))===1,"Abre WhatsApp una sola vez");
ok(msg.includes("Para cuándo: hoy a la noche, de 19:30 a 21:30"),"Mensaje con día y turno");
ok(msg.includes("Pago: efectivo, pago con $25.000"),"Mensaje con pago en efectivo");
ok(msg.includes("Dirección: Grand Bourg, Los Ceibos 123")&&msg.includes("Cantidad: 1 kg y medio kilo")&&msg.includes("Total: $20.000 más envío"),"Mensaje con barrio, dirección, potes y total");
// celular sin desborde
p=await abrir("2026-11-26T12:00:00",{width:375,height:800});
ok((await p.evaluate(()=>document.documentElement.scrollWidth))<=375,"Sin desborde en celular");
await p.screenshot({path:process.argv[2]+"/pedir_cel.png",fullPage:true});
await b.close(); console.log(f?`${f} fallas`:"Todo bien"); process.exit(f?1:0);

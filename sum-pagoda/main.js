'use strict';
const {app,BrowserWindow,session}=require('electron');
const path=require('node:path');
app.commandLine.appendSwitch('disable-features','Translate');
app.whenReady().then(()=>{
 session.defaultSession.webRequest.onBeforeRequest({urls:['http://*/*','https://*/*']},(_d,cb)=>cb({cancel:true}));
 const win=new BrowserWindow({width:1280,height:800,minWidth:900,minHeight:620,backgroundColor:'#1d1409',title:'Sum Pagoda',autoHideMenuBar:true,webPreferences:{nodeIntegration:false,contextIsolation:true,sandbox:true,webSecurity:true,devTools:false}});
 win.webContents.setWindowOpenHandler(()=>({action:'deny'}));
 win.webContents.on('will-navigate',(e,url)=>{if(!url.startsWith('file:'))e.preventDefault()});
 win.webContents.on('before-input-event',(e,i)=>{if(i.type==='keyDown'&&i.key==='Escape')app.quit()});
 win.loadFile(path.join(__dirname,'SumPagoda.html'));
});
app.on('window-all-closed',()=>app.quit());

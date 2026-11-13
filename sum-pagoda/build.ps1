$ErrorActionPreference='Stop'
$ProgressPreference='SilentlyContinue'
$here=Split-Path -Parent $MyInvocation.MyCommand.Path
$root=Join-Path $here 'dist'
$release=Join-Path $root 'SumPagoda-win32-x64'
$appDir=Join-Path $release 'resources\app'
New-Item -ItemType Directory -Force -Path $root,$release,$appDir | Out-Null
function Fetch($url,$path){
 for($n=1;$n -le 3;$n++){
  try {
   Write-Host "Downloading $url (attempt $n)"
   Invoke-WebRequest -Uri $url -OutFile $path -MaximumRedirection 10 -TimeoutSec 600 -UseBasicParsing
   if((Get-Item $path).Length -lt 1000){throw 'Download too small'}
   return
  } catch {
   Write-Warning $_
   if($n -eq 3){throw}
   Start-Sleep -Seconds (5*$n)
  }
 }
}
$gamePath=Join-Path $appDir 'SumPagoda.html'
Fetch 'https://magnificent-tortellini.pages.dev/files/sum-pagoda-v8.html' $gamePath
$game=[System.IO.File]::ReadAllText($gamePath)
if(!$game.Contains('<title>Sum Pagoda</title>') -or !$game.Contains('requestAnimationFrame(loop)') -or ([regex]::Matches($game,'data:image/')).Count -lt 20){throw 'Source integrity check failed'}
$o='viewRotated=wh>ww;'
$t='if(viewRotated)ctx.setTransform(0,viewDPR*viewScale,-viewDPR*viewScale,0,viewDPR*viewRX,viewDPR*viewRY);'
if($game.Contains($o) -and $game.Contains($t)) {
 $game=$game.Replace($o,'viewRotated=false;').Replace($t,'if(false)ctx.setTransform(0,viewDPR*viewScale,-viewDPR*viewScale,0,viewDPR*viewRX,viewDPR*viewRY);')
} elseif (!$game.Contains('viewRotated=false;')) {throw 'Unexpected orientation code'}
[System.IO.File]::WriteAllText($gamePath,$game,[System.Text.UTF8Encoding]::new($false))
Copy-Item (Join-Path $here 'main.js') (Join-Path $appDir 'main.js')
Copy-Item (Join-Path $here 'package.json') (Join-Path $appDir 'package.json')
$electronZip=Join-Path $root 'electron-v45.3.2-win32-x64.zip'
Fetch 'https://github.com/electron/electron/releases/download/v45.3.2/electron-v45.3.2-win32-x64.zip' $electronZip
$actual=(Get-FileHash $electronZip -Algorithm SHA256).Hash.ToLowerInvariant()
$expected='cd1ab0d49c2f76838c0c9ff75afefb4d9d85ca59036691932bf35be8eceba98b'
if($actual -ne $expected){throw "Electron SHA mismatch: $actual"}
Expand-Archive -LiteralPath $electronZip -DestinationPath $release -Force
Rename-Item (Join-Path $release 'electron.exe') 'SumPagoda.exe'
foreach($item in @('SumPagoda.exe','resources\app\SumPagoda.html','resources\app\main.js','resources\app\package.json')){
 if(!(Test-Path (Join-Path $release $item))){throw "Missing game item $item"}
}
$exe=Join-Path $release 'SumPagoda.exe'
Write-Host 'Windows executable launch smoke test'
$p=Start-Process -FilePath $exe -PassThru
Start-Sleep -Seconds 8
$p.Refresh()
if($p.HasExited){throw "Game exited unexpectedly (code $($p.ExitCode))"}
Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
$readme='Sum Pagoda Windows Steam Build. Run SumPagoda.exe to play-test. Upload the ENTIRE folder contents to the Steam Windows depot. Launch target: SumPagoda.exe. Game sourced from magnificent-tortellini.pages.dev. Windows process launch tested; gameplay and Steam installation NOT verified.'
Set-Content (Join-Path $release 'README-FIRST.txt') $readme
$zip=Join-Path $root 'SumPagoda-Steam-Windows.zip'
Compress-Archive -Path (Join-Path $release '*') -DestinationPath $zip -CompressionLevel Optimal -Force
Write-Host "Windows Steam package created: $zip"

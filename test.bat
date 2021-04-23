@echo off
adb devices
pause
for %%X in (

"amazon.fireos"
"amazon.jackson19"
"amazon.speech.audiostreamproviderservice"
"amazon.speech.davs.davcservice"
"amazon.speech.sim"
"amazon.speech.wakewordservice"
 
) do (
adb shell pm uninstall -k --user 0 %%X
)
pause

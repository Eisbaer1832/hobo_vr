@echo off
IF EXIST "C:\Program Files (x86)\Steam\steamapps\common\SteamVR\bin\win32\" (
rem fuck windows, this shit is disgusting, you need a fucking for loop to capture an output of a command wtf
	FOR /F "tokens=* USEBACKQ" %%F IN (`cd`) DO (
	SET var=%%F
	)
	"C:\Program Files (x86)\Steam\steamapps\common\SteamVR\bin\win32\vrpathreg.exe" adddriver "%var%"
	"C:\Program Files (x86)\Steam\steamapps\common\SteamVR\bin\win32\vrpathreg.exe" show

) ELSE (
	echo "SteamVR not located in C:\\Program Files (x86)\\Steam\\steamapps\\common\\SteamVR - Installation Failed"
)
pause

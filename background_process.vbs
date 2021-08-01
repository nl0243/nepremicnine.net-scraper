Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "Link_to_bat_file" & Chr(34), 0
Set WshShell = Nothing
# delete "build" and "dist" folders
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue -Path "$PSScriptRoot\build", "$PSScriptRoot\dist"

# delete spec files
Get-ChildItem -Path "$PSScriptRoot\*.spec" -ErrorAction SilentlyContinue | Remove-Item -Force
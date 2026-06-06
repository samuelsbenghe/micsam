(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned);
(& "$PSScriptRoot\venv\Scripts\Activate.ps1");
# build with pyinstaller
pyinstaller --onefile --noconsole --name micsam main.py
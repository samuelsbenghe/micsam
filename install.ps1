(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned);
(& "$PSScriptRoot\venv\Scripts\Activate.ps1");
pip install -r "$PSScriptRoot\requirements.txt"
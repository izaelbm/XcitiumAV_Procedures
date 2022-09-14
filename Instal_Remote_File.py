#Procedimento para instalação do SW Remoto
#Author: Izael Magalhaes
#09.22
#!/usr/bin/python

#importando bibliotecas
import os
import sys
import subprocess
import time

#Funcao para escrever o script
def makeCopy(string):
    name_file = "C:\\\\temp\\script.ps1"
    report = open(name_file, 'a')    
    report.write(string+"\n")

if os.path.isdir("C:\\\\temp"):
    print("temp - OK")
else:
	os.mkdir('C:\\\\temp')

#criando script
makeCopy('$username = "user"')
makeCopy('$pwd = ConvertTo-SecureString "password" -asplaintext -force;')
makeCopy('$credential = New-Object -TypeName PSCredential -argumentlist $username, $pwd')
makeCopy('$session = New-PSSession -ComputerName DKSP100 -Credential $credential')
makeCopy('Copy-Item -Path "C:\\\\TEMP\\sw.msi" -FromSession $session -Destination "C:\\\\temp\\sw.msi"')
makeCopy('Remove-PSSession -Session $session')

#executando o script
subprocess.Popen('powershell.exe C:\\\\temp\\script.ps1')
time.sleep(30)
#remover script
#os. remove("C:\\\\temp\\script.ps1")

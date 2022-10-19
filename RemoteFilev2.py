#!/usr/bin/python

#importando bibliotecas
import os
import subprocess
import hashlib
import pysftp
import time

#credenciais
host = hostip
port = hostport
username = user
password= pass

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

#capturando pacotes instalados
def bibliotecas():
    pipe = os.popen('pip freeze')
    bibliotecas = pipe.read()
    pipe.close()

    bibliotecas = str.split(bibliotecas)

    for line in bibliotecas:
        name_mod = line.split('=')
        if name_mod[0] == 'pysftp':
            rs = 1
            break
        else:
            rs = 0

    if name_mod[0] == 'pysftp':
        print("PYSFTP Instalado\n")               
    else:
        print('Instalando PYSFTP\n')
        subprocess.Popen('pip install pysftp')       

def GetMD5Hash(filename):
    md5_h = hashlib.md5() 
    with open(filename,'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024) 
            md5_h.update(chunk)  
    return md5_h.hexdigest()

#comparar Hash MD5
def HashCompare():
    #hash do arquivo remoto
    file = open('C:\\temp\\hash.txt', 'r')  
    file_remoto = file.read()
    #hash do arquivo local
    file_local = GetMD5Hash('C:\\temp\\app.msi')

    if str(file_local).strip() == str(file_remoto).strip():
        print("Sucesso:\n")
        print("[Local]: "+file_local+" [Remoto]: "+file_remoto+"\n")
        pass
    else:
        print("Erro:\n")
        print("[Local]: "+file_local+" [Remoto]: "+file_remoto+"\n")
        exit()

#Funcao para escrever o script
def makeCopy(string):
    name_file = "C:\\\\temp\\app.ps1"
    report = open(name_file, 'a')    
    report.write(string+"\n")

    
#iniciando o Script        
print('Iniciando o Script...\n')
bibliotecas()
try:
    print("Testando a Conexao com o Servidor...\n")
    #Testando a conexao
    with pysftp.Connection(host=host,port=port,username=username, password=password,cnopts=cnopts):
        print("Conexao OK\n")
except:
    print('Erro ao Conectar\n')

#Baixando Arquivos
with pysftp.Connection(host=host,port=port,username=username, password=password,cnopts=cnopts) as sftp:
    print("Iniciando o Download Arquivo\n")
    sftp.get('/temp/app.msi', 'C:\\temp\\app.msi')

    print("Iniciando o Download do Hash\n")
    sftp.get('/temp/hash.txt', 'C:\\temp\\hash.txt')

    print("Comparando os Arquivos\n")
    #comparando os hashes
    HashCompare() 

if os.path.isdir("C:\\temp"):
    print("temp - OK")
else:
	os.mkdir('C:\\temp')

#criando script
makeCopy('msiexec /i C:\\temp\\app.msi')

#executando o script
subprocess.Popen('powershell.exe C:\\temp\\app.ps1')
time.sleep(60)
#remover script
os. remove("C:\\temp\\app.ps1")

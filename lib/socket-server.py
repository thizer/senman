import socket
import pyautogui as gui
# import sys
import re

# Captura tamanho da tela do servidor
screenWidth, screenHeight = gui.size()
mouseX, mouseY = gui.position()

# Isso serve para impedir que o mouse saia para fora da tela
gui.FAILSAFE = False

# Params to create server
HOST = ''              # Endereco IP do Servidor
PORT = 1989            # Porta que o Servidor esta

# Start server itself
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)

print("Servidor iniciado: conecte-se em "+str(socket.gethostname())+' atrav\xc3s da porta '+str(PORT))

while True:
    con, cliente = tcp.accept()
    print 'Concetado por', cliente
    
    while True:

        msg = con.recv(1024)
        if not msg: break
        
        if (msg == ''):
            continue

        if (msg == 'exit'):
            con.close()
            tcp.close()
            # sys.exit()
            
        # Apenas um comando por vez
        cmds = msg.split(';')

        newMouseX = None
        newMouseY = None

        for cmd in cmds[0:2]:

            if (cmd == 'leftclick'):
                gui.click()
                continue

            if (cmd == 'rightclick'):
                gui.rightClick()
                continue

            if (cmd == 'doubleclick'):
                gui.doubleClick()
                continue
            
            if (cmd.startswith('scroll=+')):
                # SCROLL UP
                gui.scroll(int(cmd[8:]))
                continue
            elif (cmd.startswith('scroll=-')):
                # SCROLL DOWN
                gui.scroll(int(cmd[8:])*-1)
                continue

            if (cmd.startswith('mouseY=+')):
                # UP
                newMouseY = int(cmd[8:])*-1
                
            elif (cmd.startswith('mouseY=-')):
                # Down
                newMouseY = int(cmd[8:])
                
            if (cmd.startswith('mouseX=-')):
                # Left
                newMouseX = int(cmd[8:])*-1
                
            elif (cmd.startswith('mouseX=+')):
                # Right
                newMouseX = int(cmd[8:])
                
        gui.move(newMouseX, newMouseY)

    print 'Finalizando conexao do cliente', cliente
    con.close()


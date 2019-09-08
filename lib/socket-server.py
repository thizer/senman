import socket
import pyautogui as gui
import re

# Params to create server
HOST = ''              # Endereco IP do Servidor
PORT = 1987            # Porta que o Servidor esta
orig = (HOST, PORT)

""" Start the server socket"""
def main():
    
    # Captura tamanho da tela do servidor
    # screenWidth, screenHeight = gui.size()
    # mouseX, mouseY = gui.position()

    # Isso serve para impedir que o mouse saia para fora da tela
    gui.FAILSAFE = False

    # Start server itself
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(orig)
    tcp.listen(1) # Aceita apenas um cliente por vez

    print('Server up: connect over \''+socket.getfqdn()+':'+str(PORT)+'\'')

    socketloop(tcp)

"""Start the loop wainting for clients"""
def socketloop(tcp):

    itsplit = str.rsplit

    while True:
        con, cliente = tcp.accept()
        print cliente[0], 'is among us'
        
        ## Each message received from client {
        while True:

            msg = con.recv(1024)
            if not msg: break
            
            if (msg == ''):
                continue

            if (msg == 'exit'):
                break
                
            # Apenas um comando por vez
            cmds = itsplit(msg, ';')
            cmd = cmds[len(cmds) - 2]

            print(cmd)

            newMouseX = None
            newMouseY = None

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

        ## } End Each message received from client

        print cliente[0], 'is gone'
        con.close()
        break

    tcp.close()
    exit

""" Start application """
main()
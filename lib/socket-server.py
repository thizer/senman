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
    
    move = gui.move
    click = gui.click
    rightClick = gui.rightClick
    doubleClick = gui.doubleClick
    scroll = gui.scroll

    while True:
        con, cliente = tcp.accept()
        recv = con.recv
        print cliente[0], 'is among us'
        
        ## Each message received from client {
        while True:

            msg = recv(1024)
            if not msg: break
            
            if (msg == ''):
                continue

            if (msg == 'exit'):
                break
                
            # Apenas um comando por vez
            cmds = itsplit(msg, ';')
            cmd = cmds[len(cmds) - 2]

            if (cmd == 'leftclick'):
                click()
                continue

            if (cmd == 'rightclick'):
                rightClick()
                continue

            if (cmd == 'doubleclick'):
                doubleClick()
                continue
            
            if (cmd.startswith('scroll=+')):
                # SCROLL UP
                scroll(int(cmd[8:]))
                continue
            elif (cmd.startswith('scroll=-')):
                # SCROLL DOWN
                scroll(int(cmd[8:])*-1)
                continue

            if (cmd.find('mouse') != -1):
                
                # X positive = RIGHT
                # X negative = LEFT
                # Y positive = UP
                # Y negative = DOWN

                newMouseX = None
                newMouseY = None

                mouseX, mouseY = itsplit(cmd, '&')
                # print mouseX, mouseY

                newMouseX, signalX = strtoint(itsplit(mouseX, '=')[1])
                newMouseY, signalY = strtoint(itsplit(mouseY, '=')[1])

                newMouseY *= -1

                move(newMouseX, newMouseY)

            ## } Endif mouse

        ## } End Each message received from client

        print cliente[0], 'is gone'
        con.close()
        break

    tcp.close()
    exit

############################
##    Funcoes diversas    ##
############################

def strtoint(value):
    result = 0

    if (value == ''):
        return result

    resultRegex = re.sub(r'[^0-9]+', '', value)
    if (resultRegex != ''):
        result = int(resultRegex)

    signal = '+'

    if (value.find('-') != -1):
        result *= -1
        signal = '-'

    return (result, signal)


################################
##    FIM Funcoes diversas    ##
################################


""" Start application """
main()


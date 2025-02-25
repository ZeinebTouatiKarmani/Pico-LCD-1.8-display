import Pico-LCD-1.8

MenuText=[]
MenuFunction=[]

def add(text, function):
    MenuText.append(text)
    MenuFunction.append(function)
    
def run():
    linjecntr = 0
    #Vis MeuText
    for for s in MenuText:
        FrameBuffer.text(s, 2, linjecntr *10+2, LCD.GREEN)
        linjecntr +=1
    
    print("Hej")
    #Higlight
   
    #Mulighed for at tilføje

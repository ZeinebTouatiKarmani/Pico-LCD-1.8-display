#It work but without MenuSystem module
#All is in the same file

from machine import Pin, SPI, PWM
import framebuf
import time

# Initialize LED pin
led = Pin("LED", Pin.OUT)

# LCD Pin Configuration
BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

class LCD_1inch8(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 160
        self.height = 128
        
        self.cs = Pin(CS, Pin.OUT)
        self.rst = Pin(RST, Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1, 10000000, polarity=0, phase=0, sck=Pin(SCK), mosi=Pin(MOSI), miso=None)
        self.dc = Pin(DC, Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        # Color Definitions
        self.WHITE = 0xFFFF
        self.BLACK = 0x0000
        self.GREEN = 0x07E0
        self.BLUE = 0x001F
        self.RED = 0xF800

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize display"""
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)
        
        self.write_cmd(0x3A)
        self.write_data(0x05)

        # ST7735R Frame Rate
        self.write_cmd(0xB1)
        self.write_data(0x01)
        self.write_data(0x2C)
        self.write_data(0x2D)

        self.write_cmd(0xB2)
        self.write_data(0x01)
        self.write_data(0x2C)
        self.write_data(0x2D)

        self.write_cmd(0xB3)
        self.write_data(0x01)
        self.write_data(0x2C)
        self.write_data(0x2D)
        self.write_data(0x01)
        self.write_data(0x2C)
        self.write_data(0x2D)

        self.write_cmd(0xB4) # Column inversion
        self.write_data(0x07)

        # ST7735R Power Sequence
        self.write_cmd(0xC0)
        self.write_data(0xA2)
        self.write_data(0x02)
        self.write_data(0x84)
        self.write_cmd(0xC1)
        self.write_data(0xC5)

        self.write_cmd(0xC2)
        self.write_data(0x0A)
        self.write_data(0x00)

        self.write_cmd(0xC3)
        self.write_data(0x8A)
        self.write_data(0x2A)
        self.write_cmd(0xC4)
        self.write_data(0x8A)
        self.write_data(0xEE)

        self.write_cmd(0xC5) # VCOM
        self.write_data(0x0E)

        # ST7735R Gamma Sequence
        self.write_cmd(0xe0)
        self.write_data(0x0f)
        self.write_data(0x1a)
        self.write_data(0x0f)
        self.write_data(0x18)
        self.write_data(0x2f)
        self.write_data(0x28)
        self.write_data(0x20)
        self.write_data(0x22)
        self.write_data(0x1f)
        self.write_data(0x1b)
        self.write_data(0x23)
        self.write_data(0x37)
        self.write_data(0x00)
        self.write_data(0x07)
        self.write_data(0x02)
        self.write_data(0x10)

        self.write_cmd(0xe1)
        self.write_data(0x0f)
        self.write_data(0x1b)
        self.write_data(0x0f)
        self.write_data(0x17)
        self.write_data(0x33)
        self.write_data(0x2c)
        self.write_data(0x29)
        self.write_data(0x2e)
        self.write_data(0x30)
        self.write_data(0x30)
        self.write_data(0x39)
        self.write_data(0x3f)
        self.write_data(0x00)
        self.write_data(0x07)
        self.write_data(0x03)
        self.write_data(0x10)

        self.write_cmd(0xF0) # Enable test command
        self.write_data(0x01)

        self.write_cmd(0xF6) # Disable ram power save mode
        self.write_data(0x00)

        # Sleep out
        self.write_cmd(0x11)
        time.sleep(0.12)

        # Turn on the LCD display
        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x00)
        self.write_data(0xA0)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x02)
        self.write_data(0x00)
        self.write_data(0x81)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)

# Functions to control the LED
def TurnOn():
    led.value(1)
    time.sleep(2)
    led.value(0)

def TurnOff():
    led.value(0)
    time.sleep(2)
    led.value(1)

# Menu system
MenuText = []
MenuFunction = []
selected_item = 0

def add(text, function):
    MenuText.append(text)
    MenuFunction.append(function)

def run():
    global selected_item
    linjecntr = 0
    # Display MenuText
    for i, s in enumerate(MenuText):
        if i == selected_item:
            # Highlight the selected item
            LCD.fill_rect(12, linjecntr * 22 + 42, 160, 10, LCD.BLUE)
            LCD.text(s, 12, linjecntr * 22 + 42, LCD.WHITE)
        else:
            LCD.text(s, 12, linjecntr * 22 + 42, LCD.GREEN)
        linjecntr += 1
    LCD.show()

def next_item():
    global selected_item
    selected_item = (selected_item + 1) % len(MenuText)
    run()

def previous_item():
    global selected_item
    selected_item = (selected_item - 1) % len(MenuText)
    run()

def select_item():
    MenuFunction[selected_item]()

if __name__ == '__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768) # max 65535

    LCD = LCD_1inch8()
    # Color BRG
    LCD.fill(LCD.WHITE)
    LCD.show()
    
    LCD.fill_rect(0, 0, 160, 20, LCD.RED)
    LCD.rect(0, 0, 160, 20, LCD.RED)
    LCD.text("Raspberry Pi Pico test", 2, 8, LCD.WHITE)
    
    LCD.fill_rect(0, 20, 160, 20, LCD.BLUE)
    LCD.rect(0, 20, 160, 20, LCD.BLUE)
    LCD.text("PicoGo", 2, 28, LCD.WHITE)
    
    LCD.fill_rect(0, 40, 160, 20, LCD.GREEN)
    LCD.rect(0, 40, 160, 20, LCD.GREEN)
    LCD.text("Pico-LCD-1.8", 2, 48, LCD.WHITE)
    
    LCD.fill_rect(0, 60, 160, 10, 0x07FF)
    LCD.rect(0, 60, 160, 10, 0x07FF)
    LCD.fill_rect(0, 70, 160, 10, 0xF81F)
    LCD.rect(0, 70, 160, 10, 0xF81F)
    LCD.fill_rect(0, 80, 160, 10, 0x7FFF)
    LCD.rect(0, 80, 160, 10, 0x7FFF)
    LCD.fill_rect(0, 90, 160, 10, 0xFFE0)
    LCD.rect(0, 90, 160, 10, 0xFFE0)
    LCD.fill_rect(0, 100, 160, 10, 0xBC40)
    LCD.rect(0, 100, 160, 10, 0xBC40)
    LCD.fill_rect(0, 110, 160, 10, 0xFC07)
    LCD.rect(0, 110, 160, 10, 0xFC07)
    LCD.fill_rect(0, 120, 160, 10, 0x8430)
    LCD.rect(0, 120, 160, 10, 0x8430)
    LCD.show()
    
    time.sleep(1)
    LCD.fill(LCD.WHITE)
    LCD.text("ZEINEB LCD Menu", 12, 8, LCD.RED)
    LCD.show()
    
    add("Led On", TurnOn)
    add("Led Off", TurnOff)
    run()

    # Initialize buttons
    button_up = Pin(2, Pin.IN, Pin.PULL_UP)
    button_down = Pin(3, Pin.IN, Pin.PULL_UP)
    button_select = Pin(4, Pin.IN, Pin.PULL_UP)

    # Main loop
    while True:
        if not button_up.value():
            previous_item()
            time.sleep(0.2)  # Debounce delay
        if not button_down.value():
            next_item()
            time.sleep(0.2)  # Debounce delay
        if not button_select.value():
            select_item()
            time.sleep(0.2)  # Debounce delay
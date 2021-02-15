import sensor, image, time
from fpioa_manager import fm
from machine import UART
from board import board_info
fm.register(board_info.PIN15,fm.fpioa.UART1_TX)
fm.register(board_info.PIN17,fm.fpioa.UART1_RX)
fm.register(board_info.PIN9,fm.fpioa.UART2_TX)
fm.register(board_info.PIN10,fm.fpioa.UART2_RX)
uart_A = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)
uart_B = UART(UART.UART2, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)
write_str = 'hello world'
for i in range(20):
    uart_A.write(write_str)
    read_data = uart_B.read()
    read_str = read_data.decode('utf-8')
    print("string = ",read_str)
    if read_str == write_str:
        print("baudrate:115200 bits:8 parity:None stop:1 ---check Successfully")
uart_A.deinit()
uart_B.deinit()
del uart_A
del uart_B

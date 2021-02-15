'''
kernel_size = 1 # kernel width = (size*2)+1, kernel height = (size*2)+1
kernel = [-1, -1, -1,\
          -1, +8, -1,\
          -1, -1, -1]
'''
#fm.register(board_info.PIN15, fm.fpioa.UART1_TX, force=True)
#fm.register(board_info.PIN17, fm.fpioa.UART1_RX, force=True)
#fm.register(board_info.PIN9,fm.fpioa.UART2_TX)
#fm.register(board_info.PIN10,fm.fpioa.UART2_RX)
#uart_A = UART(UART.UART1, 115200,8,0,0, timeout=1000, read_buf_len=4096)
#uart_B = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len=4096)
#uart_A = uart_A.init(UART.UART1, 115200,8,0,0, timeout=1000, read_buf_len=4096)
'''
fm.register(board_info.PIN15,fm.fpioa.UART1_TX)
fm.register(board_info.PIN17,fm.fpioa.UART1_RX)
fm.register(board_info.PIN9,fm.fpioa.UART2_TX)
fm.register(board_info.PIN10,fm.fpioa.UART2_RX)
'''

#sensor.set_auto_gain(False) # must be turned off for color tracking
#sensor.set_auto_whitebal(False) # must be turned off for color tracking
#lcd.init()




#    uart_A.write(datax1) #输出的是目标区域中心的横坐标
#    uart_A.write(datax2)
#    FH2= bytearray([0xb4])
#    readdata = uart_B.read()
#    print('111 %f',readdata)
#    uart_A.write(FH2) #输出是帧尾
#    print('hello world')
#    lcd.display(img)
#    uart_A.deinit()
#    uart_B.deinit()
#    del uart_A
#    del uart_B

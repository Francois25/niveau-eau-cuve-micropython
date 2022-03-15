def connect():
    import network
    station = network.WLAN(network.STA_IF)
    if not station.isconnected():
        print('connecting to network...')
        station.active(True)
        station.connect('<your_wifi>', '<your_passeword>')
        while not station.isconnected():
            pass
    print('network config:', station.ifconfig())

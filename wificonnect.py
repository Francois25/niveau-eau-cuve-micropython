def connect():
    import network
    station = network.WLAN(network.STA_IF)
    if not station.isconnected():
        print('connecting to network...')
        station.active(True)
        station.connect('PAROLA_WIFI', 'Lilie@Lulu-Kelia25')
        while not station.isconnected():
            pass
    print('network config:', station.ifconfig())
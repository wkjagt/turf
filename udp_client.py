import socket, sys, json

HOST, PORT = "localhost", 9900
event = {
    'event_type' : 'registratsion',
    'event_data' : {
        'context' : 'halo',
        'timestamp' : 298376896
    }
}

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(json.dumps(event), (HOST, PORT))

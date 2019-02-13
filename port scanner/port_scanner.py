import threading, socket

host = input("Enter an address to scan: ")
ip = socket.gethostbyname(host)
threads=[]
open_ports={}
NUMBER_OF_PORTS_TO_CHECK=4023

def try_port(ip,port,delay, open_ports):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.settimeout(delay)
    result = sock.connect_ex((ip,port))
    if result == 0:
        open_ports[port] = "open"
        return True
    else:
        open_ports[port] = "closed"
        return None

def scannPort(ip, delay):

    for port in range(0,NUMBER_OF_PORTS_TO_CHECK):
        thread = threading.Thread(target=try_port, args=(ip,port,delay,open_ports))
        threads.append(thread)
    for i in range(0,NUMBER_OF_PORTS_TO_CHECK):
        threads[i].start()
    for i in range(0,NUMBER_OF_PORTS_TO_CHECK):
        threads[i].join()
    for i in range(0,NUMBER_OF_PORTS_TO_CHECK):
        if open_ports[i] == "open":
            print("Port {0} is open\n".format(str(i)))

if __name__ == "__main__":
    scannPort(ip, 3)
    
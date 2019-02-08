from lib import *
from threading import Thread
from queue import Queue
import logging

logging.basicConfig(level="INFO", format='%(threadName)-6s | %(message)s')
logger = logging.getLogger(__name__)

seeds = """dnsseed.bitcoin.dashjr.org
dnsseed.bluematt.me
seed.bitcoin.sipa.be
seed.bitcoinstats.com
seed.bitcoin.sprovoost.nl
seed.bitnodes.io"""

def get_initial_addresses():

    def fetch_ips(dns_seed):
        print(dns_seed)
        ip_list = []
        ais = socket.getaddrinfo(dns_seed,0,0,0,0)
        for result in ais:
            ip_list.append(result[-1][0])
        return list(set(ip_list))

    result = []
    for seed in seeds.split("\n"):
        try:
            ips = fetch_ips(seed.strip())
            addresses = [(ip, 8333) for ip in ips]
                            
            result.extend(addresses)
        except:
            print("error")

    return result

def worker(worker_id, address_queue):
    address = address_queue.get()
    logger.info(f'connecting to {address}')

    sock = handshake(address)
    
    getaddr = NetworkEnvelope(b"getaddr" + b"\x00"*5, b"").serialize()
    sock.send(getaddr)
    logger.info(f'sent "getaddr"')
    stream = sock.makefile("rb")

    print("Waiting for addr message")
    listening = True
    while listening:
        try:
            packet = NetworkEnvelope.parse(stream)
            if packet.command == b"addr":
                print()
                print(packet.payload)
                print()
                addr_message = AddrMessage.parse(BytesIO(packet.payload))
                if len(addr_message.addresses) == 1 and addr_message.addresses[0].ip == address[0]:
                    print("Received addr message with only our peer's address. Still waiting ...")
                else:
                    print(f"Received {len(addr_message.addresses)} addrs")
                    for address in addr_message.addresses:
                        address_queue.put((address.ip, address.port))
                    listening = False
        except Exception as e:
            print(f"Encountered error: {e}")
            break
def master():
    address_queue = Queue()
    
#     addresses = [
#         ("35.198.151.21", 8333),
#         ("91.221.70.137", 8333),
#         ("92.255.176.109", 8333),
#         ("94.199.178.17", 8333),
#         ("213.250.21.112", 8333),
#         ("aihen7kfbtscyknf.onion", 8333),
#     ]

    addresses = get_initial_addresses()

    for address in addresses:
        address_queue.put(address)
        
    threads = []
    
    for worker_id in range(1, 50):
        thread = Thread(target=worker, args=(worker_id, address_queue))
        thread.start()
        threads.append(thread)

    # FIXME: what to do here? does the main thread need to do anything?
    for thread in threads:
        thread.join()

        
if __name__ == "__main__":
    master()

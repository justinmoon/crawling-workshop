from queue import Queue
from threading import Thread
from lib import *
from db import *

def worker(worker_id, address_queue):
    while True:
        start = time.time()

        address = address_queue.get()
        print(f'connecting to {address}')

        # If we can't connect, proceed to next addressf
        try:
            sock, version_payload = handshake(address)
        except Exception as e:
            print(f"Encountered error: {e}")
            return

        stream = sock.makefile("rb")

        # Save the address & version payload
        observe_node(address, version_payload)

        # Request their peer list
        sock.send(serialize_msg(b"getaddr", b""))
        print(f'sent "getaddr"')

        print("Waiting for addr message")
        while True:
            # Only wait 5 seconds for addr message
            if time.time() - start > 5:
                break

            # If connection breaks, proceed to next address
            try:
                msg = read_msg(stream)
            except:
                print("Error reading message")
                break

            # Only handle "addr" messages
            if msg["command"] == b"addr":
                addr_payload = read_addr_payload(BytesIO(msg["payload"]))
                for address in addr_payload["addresses"]:
                    address_queue.put((address["ip"], address["port"]))            
                    print(f'Received {len(addr_payload["addresses"])} addrs')
                break
            else:
                print("ignoring", msg['command'])
                  
def threaded_crawler(addresses):
    address_queue = Queue()
    for address in addresses:
        address_queue.put(address)
        
    threads = []
    
    for worker_id in range(10):
        thread = Thread(target=worker, args=(worker_id, address_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    create_table()
    addresses = fetch_addresses(dns_seeds)
    threaded_crawler(addresses)
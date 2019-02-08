from io import BytesIO

from crawler1 import NetworkEnvelope, VersionMessage, AddrMessage, bytes_to_ip, ip_to_bytes



VM1  = b'\xf9\xbe\xb4\xd9version\x00\x00\x00\x00\x00z\x00\x00\x00\x83\xa5\x04\xc2\x7f\x11\x01\x00\r\x04\x00\x00\x00\x00\x00\x00wuZ\\\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x8aD\xabn\xa8 \r\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x008;l\xe5\xe7\xea\xa5a$/Satoshi:0.17.0(UASF-SegWit-BIP148)/\\\x92\x08\x00\x01'

VM2 = b'\xf9\xbe\xb4\xd9version\x00\x00\x00\x00\x00f\x00\x00\x00y\xda\xd5\x92\x7f\x11\x01\x00\r\x04\x00\x00\x00\x00\x00\x00\x186Y\\\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00*\x03\xb0\xc0\x00\x01\x00\xd0\x00\x00\x00\x00\x0c\x1b@\x01\xa7\xce\r\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00iI\x9b\x8b[\x16\r\xd4\x10/Satoshi:0.17.0/\xcc\x91\x08\x00\x01'

def test_version_message():
    stream = BytesIO(VM1)
    ne = NetworkEnvelope.parse(stream)
    vm = VersionMessage.parse(BytesIO(ne.payload))
    serialized_vm = vm.serialize()
    serialized_ne = NetworkEnvelope(b"version", serialized_vm).serialize()
    
    stream2 = BytesIO(serialized_ne)
    ne2 = NetworkEnvelope.parse(stream2)
    vm2 = VersionMessage.parse(BytesIO(ne2.payload))
    
    print(vm.__dict__)
    print()
    print(vm2.__dict__)
    
    assert vm.__dict__ == vm2.__dict__
    
    print(VM1)
    print()
    print(serialized_ne)
    
    print(ne.__dict__)
    print()
    print(ne2.__dict__)
    
    assert VM1 == serialized_ne
    
def test_version_message2():
    stream = BytesIO(VM2)
    ne = NetworkEnvelope.parse(stream)
    vm = VersionMessage.parse(BytesIO(ne.payload))
    serialized_vm = vm.serialize()
    serialized_ne = NetworkEnvelope(b"version", serialized_vm).serialize()
    
    stream2 = BytesIO(serialized_ne)
    ne2 = NetworkEnvelope.parse(stream2)
    vm2 = VersionMessage.parse(BytesIO(ne2.payload))
    
    print(vm.__dict__)
    print()
    print(vm2.__dict__)
    
    assert vm.__dict__ == vm2.__dict__
    
    print(VM2)
    print()
    print(serialized_ne)
    
    print(ne.__dict__)
    print()
    print(ne2.__dict__)
    
#     for i in range(len(VM2)):
#         print(i, VM2[i], serialized_ne[i])
    
    assert VM2 == serialized_ne
    
def test_onions():
    assert bytes_to_ip(ip_to_bytes('aihen7kfbtscyknf.onion'))
    
from lib import *

def test_message():
    stream = BytesIO(VM1)
    msg = read_msg(stream)
    payload_dict = read_version_payload(BytesIO(msg["payload"]))
    payload = serialize_version_payload(**payload_dict)
    serialized = serialize_msg(msg["command"], payload)
    assert serialized == VM1


# def test_version():
#     stream = BytesIO(VM1)
#     msg = read_message(stream)
#     assert msg["payload"]["version"] == 70015
#     serialized = serialize_message(msg)

# def test_addrs():
#     pass

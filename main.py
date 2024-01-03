import os
from typing import List

from scapy.all import rdpcap

from groups import get_group
from influxdb_gateway import InfluxDBGateway, Packet
from mongodb_gateway import MongoDBGateway


def to_text(x): return x if type(x) == str else x.decode()


def read_pcap(path):
    packets = rdpcap(path)
    return packets


def convert_to_ip_host_mapping(packets):
    print(packets)
    result = {}
    for packet in packets:
        if "DNSRR" in packet:
            for idx in range(packet["DNS"].ancount):
                answer_record = packet["DNSRR"][idx]
                # ignore HTTPS record
                if answer_record.type != 65:
                    ip_address = to_text(answer_record.rdata)
                    host_name = to_text(answer_record.rrname)
                    result[ip_address] = host_name
    return result


def write_ip_host_mapping(ip_host_mapping):
    for ip, host in ip_host_mapping.items():
        mongoGateway.write_host_mapping(ip, host)


def convert_packet_to_data(packets) -> List[Packet]:
    result = []
    for packet in packets:
        if packet.haslayer('IP'):
            src = mongoGateway.get_host_by_ip(packet.getlayer('IP').src)
            dest = mongoGateway.get_host_by_ip(packet.getlayer('IP').dst)
            src_service = get_group(src)
            dest_service = get_group(dest)
            protocol = packet.name
            time = int(packet.time)
            packet_length = len(packet)

            result.append({
                'src': src,
                'src_service': src_service,
                'dest_service': dest_service,
                'dest': dest,
                'protocol': protocol,
                'time': time,
                'packet_length': packet_length
            })
    return result


pcap_file_dir = "./logs/"
influxGateway = InfluxDBGateway()
mongoGateway = MongoDBGateway()

if __name__ == "__main__":
    try:
        for pcap_file in os.listdir(pcap_file_dir):
            if pcap_file.endswith('.pcap'):
                pcap_file_path = os.path.join(pcap_file_dir, pcap_file)
                packets = read_pcap(pcap_file_path)
                ip_host_mapping = convert_to_ip_host_mapping(packets)
                write_ip_host_mapping(ip_host_mapping)
                data = convert_packet_to_data(packets)
                influxGateway.write_packets(data)

    finally:
        mongoGateway.close_connection()
        influxGateway.close_connection()

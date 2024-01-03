from datetime import datetime
from typing import List, TypedDict

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUXDB_CONFIG = {
    # see docker compose
    'token': 'initial_token',
    'org': 'test org',
    'url': 'http://localhost:8086',
    'bucket': "test_bucket"
}


class Packet(TypedDict):
    src: str
    dest: str
    protocol: str
    time: str
    packet_length: int


class InfluxDBGateway:
    def __init__(self):
        self.client = InfluxDBClient(
            url=INFLUXDB_CONFIG['url'], token=INFLUXDB_CONFIG['token'], org=INFLUXDB_CONFIG['org'])
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

    def write_packets(self, packets: List[Packet]):
        for packet in packets:
            print(packet)
            timestamp = datetime.utcfromtimestamp(
                packet['time']).strftime('%Y-%m-%dT%H:%M:%SZ')
            point = (Point("network_traffic")
                     .tag("source_ip", packet['src'])
                     .tag("destination_ip", packet['dest'])
                     .tag("src_service", packet['src_service'])
                     .tag("dest_service", packet['dest_service'])
                     .tag("protocol", packet['protocol'])
                     .time(timestamp)
                     .field("length", packet['packet_length'])
                     )
            # print(point)
            self.write_api.write(
                bucket=INFLUXDB_CONFIG['bucket'], org=INFLUXDB_CONFIG['org'], record=point)
        print(f"write {len(packets)} data successfully")

    def close_connection(self):
        self.client.close()

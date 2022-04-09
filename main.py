from dataclasses import dataclass
from typing import Dict, List, Optional
import requests
from pypresence import Presence
import time

import requests


@dataclass
class Toy:
    identifier: str
    nickname: str
    name: str
    version: str
    battery: int
    status: int

    @staticmethod
    def from_dict(data: dict) -> "Toy":
        return Toy(
            identifier=data["id"],
            nickname=data["nickName"],
            name=data["name"].capitalize(),
            battery=data["battery"],
            status=data["status"],
            version=data["version"],
        )



@dataclass
class Connection:
    device_id: str
    domain: str
    http_port: int
    https_port: int
    platform: str
    app_version: str
    toys: List[Toy]

    @staticmethod
    def from_dict(data: dict) -> "Connection":
        return Connection(
            device_id=data["deviceId"],
            domain=data["domain"],
            http_port=data["httpPort"],
            https_port=data["httpsPort"],
            platform=data["platform"],
            app_version=data["appVersion"],
            toys=[Toy.from_dict(t) for t in data["toys"].values()],
        )

    def vibrate_toy(self, power_level: int, toy: Optional[Toy] = None):
        toy_query_opt = f'&t={toy.identifier}' if toy else ''
        url = f"https://{self.domain}:{self.https_port}/Vibrate?v={power_level}" + toy_query_opt
        r = requests.get(url)
        print(r.status_code)
        print(r.json())

    def stop_vibration(self, toy: Optional[Toy] = None):
        toy_query_opt = f'&t={toy.identifier}' if toy else ''
        url = f"https://{self.domain}:{self.https_port}/Vibrate?v=0" + toy_query_opt
        r = requests.get(url)
        print(r.status_code)
        print(r.json())


def fetch_connections() -> Optional[List[Connection]]:
    result = requests.get("https://api.lovense.com/api/lan/getToys")
    if result.ok:
        data = result.json()
        return [Connection.from_dict(v) for _, v in data.items()]
    return None


CLIENT_ID = "962344637270458388"

if __name__ == "__main__":
    # rpc = Presence(CLIENT_ID)
    # rpc.connect()

    # start_time = time.time()
    connections = fetch_connections()
    toy = connections[0].toys[0]
    conn = connections[0]
    conn.vibrate_toy(16)
    connections = fetch_connections()
    print(connections)
    time.sleep(10)
    conn.stop_vibration()
    # while True:
    #     connections = fetch_connections()
    #     toy = connections[0].toys[0]
    #     rpc.update(
    #         details=f"💤 {toy.name} {toy.version}",
    #         state=f"🔋 {toy.battery}%",
    #         start=start_time,
    #         large_image="lovense-logo",
    #     )
    #     time.sleep(5)

import time
from pymavlink import mavutil

target_system = 1  # Sistem ID
target_component = 1  # Bileşen ID
master = mavutil.mavlink_connection('udpout:127.0.0.1:14550', source_system=target_system)

def send_heartbeat():
    while True:
        master.mav.heartbeat_send(
            type=mavutil.mavlink.MAV_TYPE_QUADROTOR,
            autopilot=mavutil.mavlink.MAV_AUTOPILOT_GENERIC,
            base_mode=0,
            custom_mode=0,
            system_status=mavutil.mavlink.MAV_STATE_ACTIVE
        )
        print("Heartbeat mesajı gönderildi.")
        time.sleep(1.5)

if __name__ == '__main__':
    send_heartbeat()

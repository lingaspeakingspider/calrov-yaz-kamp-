import time
import threading
import logging
import keyboard
from pymavlink import mavutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# MAVLink bağlantısı
connection = mavutil.mavlink_connection('udp:127.0.0.1:14550')

connection.wait_heartbeat()
logging.info("Heartbeat mesajı alındı!")

def heartbeat_listener():
    with open('heartbeat_log.txt', 'a') as f:
        while True:
            msg = connection.recv_match(type='HEARTBEAT', blocking=True)
            if msg:
                msg_dict = msg.to_dict()
                f.write(f"{msg_dict}\n")
                f.flush()
                logging.info(f"HEARTBEAT mesajı dosyaya yazıldı: {msg_dict}")
            else:
                logging.warning("No heartbeat message received!")

def arm():
    connection.arducopter_arm()
    logging.info("Drone armed")

def disarm():
    connection.arducopter_disarm()
    logging.info("Drone disarmed")

def set_mode(mode):
    mode_mapping = {'manual': 'MANUAL', 'depth_hold': 'ALT_HOLD', 'stabilize': 'STABILIZE'}
    if mode in mode_mapping:
        connection.set_mode(mode_mapping[mode])
        logging.info(f"Mode set to {mode}")

def send_movement_command(x=0, y=0, z=0, yaw=0):
    connection.mav.manual_control_send(
        connection.target_system,
        x, y, z, yaw, 0)
    logging.info(f"Movement command sent: x={x}, y={y}, z={z}, yaw={yaw}")

def send_servo_command(servo_number, pwm_value):
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        0,
        servo_number,
        pwm_value,
        0, 0, 0, 0, 0)
    logging.info(f"Servo command sent: servo={servo_number}, pwm={pwm_value}")

def keyboard_listener():
    while True:
        if keyboard.is_pressed('w'):
            send_movement_command(x=500)
        if keyboard.is_pressed('s'):
            send_movement_command(x=-500)
        if keyboard.is_pressed('a'):
            send_movement_command(y=-500)
        if keyboard.is_pressed('d'):
            send_movement_command(y=500)
        if keyboard.is_pressed('up'):
            send_movement_command(z=500)
        if keyboard.is_pressed('down'):
            send_movement_command(z=-500)
        if keyboard.is_pressed('left'):
            send_movement_command(yaw=-500)
        if keyboard.is_pressed('right'):
            send_movement_command(yaw=500)
        if keyboard.is_pressed('q'):
            arm()
        if keyboard.is_pressed('e'):
            disarm()
        if keyboard.is_pressed('1'):
            set_mode('manual')
        if keyboard.is_pressed('2'):
            set_mode('depth_hold')
        if keyboard.is_pressed('3'):
            set_mode('stabilize')
        if keyboard.is_pressed('z'):
            send_servo_command(servo_number=1, pwm_value=1500)
        if keyboard.is_pressed('esc'):
            logging.info("Keyboard moddan çıkılıyor.")
            break
        time.sleep(0.1)

heartbeat_thread = threading.Thread(target=heartbeat_listener)
heartbeat_thread.daemon = True
heartbeat_thread.start()

keyboard_listener()

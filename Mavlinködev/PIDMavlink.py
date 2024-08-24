import time
import threading
import logging
import keyboard
from pymavlink import mavutil
from simple_pid import PID

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

connection = mavutil.mavlink_connection('udp:127.0.0.1:14550')
connection.wait_heartbeat()
logging.info("Heartbeat mesajı alındı!")

# PID
pid_roll = PID(1, 0.1, 0.05, setpoint=0)
pid_pitch = PID(1, 0.1, 0.05, setpoint=0)
pid_yaw = PID(1, 0.1, 0.05, setpoint=0)
pid_z = PID(1, 0.1, 0.05, setpoint=0)

running = True

def heartbeat_listener():
    with open('heartbeat_log.txt', 'a') as f:
        while running:
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
        int(x), int(y), int(z), int(yaw), 0)
    logging.info(f"Movement command sent: x={int(x)}, y={int(y)}, z={int(z)}, yaw={int(yaw)}")

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

def pid_control():
    while running:
        roll_setpoint = pid_roll.setpoint
        pitch_setpoint = pid_pitch.setpoint
        yaw_setpoint = pid_yaw.setpoint
        z_setpoint = pid_z.setpoint

        roll_value = 0  # roll verisi...
        pitch_value = 0  # pitch verisi...
        yaw_value = 0  # yaw verisi...
        z_value = 0  # z verisi...

        roll_output = pid_roll(roll_value)
        pitch_output = pid_pitch(pitch_value)
        yaw_output = pid_yaw(yaw_value)
        z_output = pid_z(z_value)

        send_movement_command(x=roll_output, y=pitch_output, z=z_output, yaw=yaw_output)

        time.sleep(0.1)

def keyboard_listener():
    global running
    while running:
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
            running = False
        time.sleep(0.1)

heartbeat_thread = threading.Thread(target=heartbeat_listener)
heartbeat_thread.daemon = True
heartbeat_thread.start()

pid_thread = threading.Thread(target=pid_control)
pid_thread.daemon = True
pid_thread.start()

keyboard_listener()

logging.info("Program sonlanıyor.")

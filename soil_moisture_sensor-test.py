from smbus2 import SMBus
#from smbus import SMBus
from time import sleep


if __name__ == "__main__":


    while True:
        try:
            bus = SMBus(1)

            response = bus.read_i2c_block_data(0x10, 0, 4)
            value = int.from_bytes(response, "little")
            print(f"Value: {value} | bytes: {response}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            bus.close()
            sleep(0.5)

 



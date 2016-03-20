import RPi.GPIO as GPIO
import time
import atexit

class Servo:
	"""
	A servo class to hold attributes and
	functions for controlling Mahri's servos.
	"""
	def __init__(self, pin, angle):
		"""
		Initialize a servo. Also initizlizes
		a given PWM pin to control the servo.
		"""
		self.pin = pin
		self.angle = angle
		GPIO.setup(pin, GPIO.OUT)
		self.pwm = GPIO.PWM(pin, 100)
		self.pwm.start(5)

	def set(self, angle):
		"""
		Set the angle of a servo.
		"""
		self.pwm.ChangeDutyCycle(float(angle) / 10.0 + 2.5)
		self.angle = angle

def main():
	"""
	Create servo objects that can be
	easily controlled.
	"""
	# Define pin number mode
	GPIO.setmode(GPIO.BCM)

	# Initialize left and right servos
	leftServo = Servo(18, 0)
	rightServo = Servo(20, 20)

	leftServo.set(50)

	cleanup()

def cleanup():
	"""
	Close GPIO pins after code is run.
	"""
	GPIO.cleanup()

if __name__ == "__main__":
	main()
	# atexit.register(cleanup)
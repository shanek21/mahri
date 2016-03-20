import RPi.GPIO as GPIO
import time
import atexit
import sys

class Servo:
	"""
	A servo class to hold attributes and
	functions for controlling Mahri's servos.
	"""
	def __init__(self, pin, unwoundAngle, woundAngle):
		"""
		Initialize a servo. Also initizlizes
		a given PWM pin to control the servo.
		"""
		self.pin = pin
		self.unwoundAngle = unwoundAngle
		self.woundAngle = woundAngle
		GPIO.setup(self.pin, GPIO.OUT)
		self.pwm = GPIO.PWM(self.pin, 100)
		self.pwm.start(5)

	def set(self, angle):
		"""
		Move the servo to the given angle.
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
	lServo = Servo(20, 210, 21)
	rServo = Servo(18, 20, 225)

	demo(lServo, rServo)

	cleanup()

def demo(lServo, rServo):
	"""
	Run servos to have Mahri execute
	basic movements.
	"""

	delay = 2

	# Stand up
	lServo.set(lServo.unwoundAngle)
	rServo.set(rServo.unwoundAngle)
	time.sleep(delay)

	# Crouch down
	lServo.set(lServo.woundAngle)
	rServo.set(rServo.woundAngle)
	time.sleep(delay)

	# Stand up
	lServo.set(lServo.unwoundAngle)
	rServo.set(rServo.unwoundAngle)
	time.sleep(delay)

	# Lean left
	lServo.set(lServo.woundAngle)
	rServo.set(rServo.unwoundAngle)
	time.sleep(delay)

	# Lean right
	lServo.set(lServo.unwoundAngle)
	rServo.set(rServo.woundAngle)
	time.sleep(delay)

	# Stand up
	lServo.set(lServo.unwoundAngle)
	rServo.set(rServo.unwoundAngle)
	time.sleep(delay)

def cleanup():
	"""
	Close GPIO pins after code is run.
	"""
	GPIO.cleanup()

if __name__ == "__main__":
	main()
	# atexit.register(cleanup)
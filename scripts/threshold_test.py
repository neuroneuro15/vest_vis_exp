import random
from psychopy import event, sound
import time
    
## Define function to get rotation threshold


def get_tracker():
    return natnetclient.NatClient()


def rotation_threshold_detector(tracker, rigidbody, acc_threshold=0, vel_threshold=0, end_success_threshold = 3):
    
    rot, vel, n_successes = 0., 0., 0
    while 1: ## loop while rotating stimuli
        try:
            acc = ((rigidbody.rotation.y - rot) - vel) / tracker.timestamp
        except:
            pass
        try:
            vel = (rigidbody.rotation.y - rot) / tracker.timestamp
        except:
            pass
            
        rot = rigidbody.rotation.y
        
        n_successes = n_successes + 1 if abs(vel) > vel_threshold and acc > acc_threshold else 0
       ## if n_successes == end_success_threshold: ## return only when staying above threshold for defined time
        ##    if vel > 0: return 1
         ##   else: return -1
        if n_successes == end_success_threshold: return 1


def new_threshold_detector(tracker, rigidbody, acc_threshold=2000, vel_threshold=50, end_success_threshold = 5):
    frame_num = tracker.iFrame
    rot = rigidbody.rotation.y
    vel = 0.1
    timesecs = tracker.timestamp - .01
    n_successes = 0.
    acc = 0.0
    while True:
        if tracker.iFrame != frame_num:
            # Set the new value
            frame_num = tracker.iFrame
            try:
                acc = ((rigidbody.rotation.y - rot) - vel) / (tracker.timestamp - timesecs)
                vel = (rigidbody.rotation.y - rot) / (tracker.timestamp - timesecs)
                rot = rigidbody.rotation.y
                timesecs = tracker.timestamp
                print("Vel: {}\tAcc: {}\tNSucc: ".format(vel, acc, n_successes))
            except ZeroDivisionError:
                pass

        if abs(acc) > acc_threshold and abs(vel) > vel_threshold:
            n_successes += 1
        else:
            n_successes = 0

        if n_successes > end_success_threshold:
            return vel

def velocity_threshold_detector(tracker, rigidbody, vel_threshold=50, end_success_threshold = 5):
    frame_num = tracker.iFrame
    rot = rigidbody.rotation.y
    vel = .1
    timesecs = tracker.timestamp - .01
    n_successes = 0.
    while True:
        if tracker.iFrame != frame_num:
            # Set the new value
            frame_num = tracker.iFrame
            try:
                vel = (rigidbody.rotation.y - rot) / (tracker.timestamp - timesecs)
                rot = rigidbody.rotation.y
                timesecs = tracker.timestamp
                print("Vel: {}\tNSucc: {}".format(vel, n_successes))
            except ZeroDivisionError:
                pass

        if abs(vel) > vel_threshold:
            n_successes += 1
        else:
            n_successes = 0

        if n_successes > end_success_threshold:
            return vel


def get_velocity(tracker, rigidbody):
    frame_num = tracker.iFrame
    rot = rigidbody.rotation.y
    timesecs = tracker.timestamp - .01
    while 'escape' not in event.getKeys():
        if tracker.iFrame != frame_num:
            # Set the new value
            frame_num = tracker.iFrame
            try:
                vel = (rigidbody.rotation.y - rot) / (tracker.timestamp - timesecs)
                rot = rigidbody.rotation.y
                timesecs = tracker.timestamp
                print(vel)
            except ZeroDivisionError:
                pass

def get_acceleration(tracker, rigidbody):
    frame_num = tracker.iFrame
    rot = rigidbody.rotation.y
    vel = 0.1
    timesecs = tracker.timestamp - .01
    while 'escape' not in event.getKeys():
        if tracker.iFrame != frame_num:
            # Set the new value
            frame_num = tracker.iFrame
            try:
                acc = ((rigidbody.rotation.y - rot) - vel) / (tracker.timestamp - timesecs)
                vel = (rigidbody.rotation.y - rot) / (tracker.timestamp - timesecs)
                rot = rigidbody.rotation.y
                timesecs = tracker.timestamp
                print("Vel: {}\tAcc: {}".format(vel, acc))
            except ZeroDivisionError:
                pass

if __name__ == '__main__':

    import natnetclient
    tracker = natnetclient.NatClient()
    headmount = tracker.rigid_bodies['HeadMount']

    tone = sound.Sound(secs=.3)

    #acc_thresh = input('What acc. threshold should we use: ')
    vel_thresh = input('What vel. threshold should we use: ')

    while 1:
        velocity_threshold_detector(tracker, headmount, vel_threshold=vel_thresh, end_success_threshold = 10)
        tone.play()
        time.sleep(1.5)

            

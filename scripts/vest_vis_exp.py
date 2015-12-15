import random
import time
import csv
import sys
from datetime import datetime
from psychopy import event, gui, visual, core, data, sound
from threshold_test import velocity_threshold_detector
import natnetclient
import copy

# Connect to the optical tracker
tracker = natnetclient.NatClient()
head_mount = tracker.rigid_bodies['HeadMount']

# Connect to the Stimulus Computer
#raise NotImplementedError("Still need to write network connection to stimulus computer!")

# Get Session Data and write it to the log header
session_data = {'Experiment': 'VisVestib',
                'Participant': 'TestSubj',
                'nTrials': 50,
                'Velocity Threshold': .1,
                'N Frames Above Threshold': 3,
                'Left Response Key': 'left',
                'Right Response Key': 'right',
                }

dlg = gui.DlgFromDict(dictionary=session_data, title='Please Input Data', fixed=['Experiment'])
if dlg.OK:
    session_data['nTrials'] = int(session_data['nTrials'])
    session_data['Velocity Threshold'] = float(session_data['Velocity Threshold'])
    session_data['N Frames Above Threshold'] = int(session_data['N Frames Above Threshold'])
    session_data['Left Response Key'] = str(session_data['Left Response Key'])
    session_data['Right Response Key'] = str(session_data['Right Response Key'])
else:
    sys.exit()

# Create CSV Log, and write the session data as a header to it.
log_filename = session_data['Experiment'] +  '_' + session_data['Participant'] + datetime.now().strftime('%H%M%S') + '.csv'
with open(log_filename, 'w') as log:
    log.writelines([": ".join([key, str(value)]) + '\n' for (key, value) in session_data.items()])
    log.writelines('\n\n')  # Make a couple of blank lines after the header


# Setup Staircase
staircase = data.StairHandler(startVal=.35,
        nTrials=session_data['nTrials'], nUp=1, nDown=2,
        minVal = 0.01, maxVal=1,
        stepSizes=.05, stepType='lin' #[.1,.1,.05,.05,.01,.01],
        )

staircases=[[copy.deepcopy(staircase), copy.deepcopy(staircase)],
            [copy.deepcopy(staircase), copy.deepcopy(staircase)]]

# If not, run a trial in the staircase
tone = sound.Sound(secs=.2)
win = visual.Window(screen=1)
with open(log_filename, 'a') as log:

    # Write Column headers
    log.write(','.join(['Trial', 'MoveDir', 'VisDir', 'VisCoherence', 'Response', 'RT']) + '\n')
    trial_num = 0
    
    while trial_num < session_data['nTrials'] * 5:
        trial_num += 1

        # Measure which movement direction the subject is being pushed in.
        movement_direction = velocity_threshold_detector(tracker,
                                                         head_mount,
                                                         vel_threshold=session_data['Velocity Threshold'],
                                                         end_success_threshold = session_data['N Frames Above Threshold'])
        tone.play()


        # Randomly choose which visual direction will be used
        visual_direction = random.choice([0, 1])

        # Choose the Motion Coherence Level
        staircase = staircases[int(movement_direction>=0)][visual_direction]     
        try:
            stimulus_level = staircase.next()
        except StopIterationError:
            break  # FIXME: The Experiment will currently end prematurely with this decision!

        # Draw the Stimulus!
        # send_stimulus_data(visual_direction,stimulus_level)
        # wait_for_draw_confirmation()

        # Collect Participant Response and Response Time
        start_time = time.time()
        event.getKeys()
        print('Waiting for participant response...')
        while True:
            response = event.waitKeys()[0]
            print(response)
            if response in [session_data['Left Response Key'], session_data['Right Response Key']]:
                response_time = time.time() - start_time
                break



        # Evaluate Response
        if response == session_data['Left Response Key'] and visual_direction==0: 
            wasCorrect= 1
        elif response == session_data['Right Response Key'] and visual_direction==1: 
            wasCorrect= 1
        else: 
            wasCorrect = 0
        
        # Write Trial Data to the Log
        log.write(','.join([str(trial_num), str(movement_direction), str(visual_direction), str(stimulus_level), str(response), str(response_time)]) + '\n')

        # Put the subject response into the staircase
        staircase.addData(wasCorrect) #so that the staircase adjusts itself
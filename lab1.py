    #region VEXcode Generated Robot Configuration
    from vex import *
    import urandom
    import math

    # Brain should be defined by default
    brain=Brain()

    # Robot configuration code
    left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
    right_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
    controller_1 = Controller(PRIMARY)
    ultrasonic_sensor = Distance(Ports.PORT17)
    lightSensor = Line(brain.three_wire_port.b)


    # wait for rotation sensor to fully initialize
    wait(30, MSEC)


    # Make random actually random
    def initializeRandomSeed():
        wait(100, MSEC)
        random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
        urandom.seed(int(random))
        
    # Set random seed 
    initializeRandomSeed()


    def play_vexcode_sound(sound_name):
        # Helper to make playing sounds from the V5 in VEXcode easier and
        # keeps the code cleaner by making it clear what is happening.
        print("VEXPlaySound:" + sound_name)
        wait(5, MSEC)

    # add a small delay to make sure we don't print in the middle of the REPL header
    wait(200, MSEC)
    # clear the console to make sure we don't have the REPL in the console
    print("\033[2J")

    #endregion VEXcode Generated Robot Configuration

    # ------------------------------------------
    # 
    # 	Project:      VEXcode Project
    #	Author:       VEX
    #	Created:
    #	Description:  VEXcode V5 Python Project
    # 
    # ------------------------------------------

    # Library imports
    from vex import *

    # Begin project code

    # define the states
    IDLE = 0
    DRIVING_FWD = 1
    DRIVING_BKWD = 2



    # start out in the idle state
    current_state = IDLE

    # Bumper
    ## TODO: Add a Bumper with the Device Manager

    # Reflectance
    ## TODO: Add a reflectance sensor (Linetracker) with the Device Manager

    # Rangefinder
    ## TODO: Add an ultrasonic rangefinder (Rangefinder) with the Device Manager

    PI = 3.142
    wheelDiameterCM = 4.0 * 2.54
    wheelRadiusCM = wheelDiameterCM/2
    wheelCircumferenceCM = PI * wheelDiameterCM
    gearRatio = 5.0
    wheelTrackCM = 11.0 * 2.54
    degreesPerCM = 360.0 / wheelCircumferenceCM

    # Function to drive BaseBot straight for some number of CM

    def driveStraightCM(direction, distanceInCM, speed_CM_per_sec):
        left_motor.spin_for(direction, distanceInCM*gearRatio*degreesPerCM, DEGREES, speed_CM_per_sec/wheelRadiusCM*60*gearRatio/(2*PI), RPM, False)
        right_motor.spin_for(direction, distanceInCM*gearRatio*degreesPerCM, DEGREES, speed_CM_per_sec/wheelRadiusCM*60*gearRatio/(2*PI), RPM, False)
        

    def drive_for(direction, turns, speed):
        left_motor.set_velocity(speed, RPM);
        left_motor.spin_for(direction, turns, TURNS, wait = False)

        right_motor.set_velocity(speed, RPM);
        right_motor.spin_for(direction, turns, TURNS, wait = False)

    """
    Pro-tip: print out state _transistions_.
    """
    def handleLeft1Button():
        global current_state
        print('Left 1 Button Pressed')

        if(current_state == IDLE):
            print('IDLE -> FORWARD')
            current_state = DRIVING_FWD

            # Note how we set the motor to drive here, just once. 
            # No need to call over and over and over in a loop.
            # Also, note that we call the non-blocking version so we can
            # return to the main loop.

            ## TODO: You'll need to update the speed and number of turns
            drive_for(FORWARD, 5, 60)
            
        else: # in any other state, the button acts as a kill switch
            print(' -> IDLE')
            current_state = IDLE
            left_motor.stop()
            right_motor.stop()

    """
    Pro-tip: print out state _transistions_.
    """
    def handleBumperG():
        global current_state

        ## Todo: Add code to handle the bumper being presses
        pass


    # Here, we give an example of a proper event checker. It checks for the _event_ 
    # of stopping (not just if the robot is stopped).
    wasMoving = False
    def checkMotionComplete():
        global wasMoving

        retVal = False

        isMoving = left_motor.is_spinning() or right_motor.is_spinning()

        if(wasMoving and not isMoving):
            retVal = True

        wasMoving = isMoving
        return retVal

    # Then we declare a handler for the completion of the motion.
    def handleMotionComplete():
        global current_state

        if(current_state == DRIVING_FWD):
            print('FORWARD -> BACKWARD')
            current_state = DRIVING_BKWD

            ## TODO: You'll need to update the speed and number of turns       
            drive_for(REVERSE, 5, 60)
        
        elif(current_state == DRIVING_BKWD):
            print('BACKWARD -> IDLE')
            current_state = IDLE

        else:
            print('E-stop') # Should print when button is used as E-stop

    def checkLight():
        print("Value: %d " % lightSensor.reflectivity(PERCENT))
        retVal = False
        if lightSensor.reflectivity(PERCENT) > 30:
            retVal = True
            print("Below threshold")
        else: 
            print("Above threshold")
        return retVal
    def handleLight():
        global current_state  
        if(current_state == DRIVING_FWD):
            print('FORWARD -> BACKWARD')
            current_state = DRIVING_BKWD

            drive_for(REVERSE, 5, 60)
        else:
            print('Reflection sensor below threshold, no change')

    ## TODO: Add a checker for the reflectance sensor
    ## See checkMotionComplete() for a good example

    ## TODO: Add a handler for when the reflectance sensor triggers


    """
    The line below makes use of VEX's built-in event management. Basically, we set up a "callback", 
    basically, a function that gets called whenever the button is pressed (there's a corresponding
    one for released). Whenever the button is pressed, the handleButton function will get called,
    _without you having to do anything else_.

    """
    controller_1.buttonL1.pressed(handleLeft1Button)

    ## TODO: Add event callback for bumper

    """
    Note that the main loop only checks for the completed motion. The button press is handled by 
    the VEX event system.
    """
    # The main loop
    while True:
        #if(checkMotionComplete()): handleMotionComplete()
        if(checkLight()): handleLight()

        #print(ultrasonic_sensor.object_distance(units))

    ## TODO: Add various checkers/handlers; print ultrasonic; etc. See handout.


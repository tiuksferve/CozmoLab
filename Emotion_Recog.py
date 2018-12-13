#!/usr/bin/env python3
# Code wrote by Tiago Veiga - veigatf@gmail.com - IG: tiuksferve - Mobile: +55 61 999.682.129
# Feel free to perform improvements and put you name right after this comment:
#

import time
import cozmo
import asyncio
from cozmo.util import degrees, distance_mm, speed_mmps

# Cozmo voice - True to activate / False to Deactivate
Voice = True

# Phrases to be said when emotions are recognized
happy = "You look happy!"
sad = "You look sad."
angry = "You look angry."
surprised = "You look surprised!"

# Reset default True to False in order to drive Cozmo off the charger
cozmo.robot.Robot.drive_off_charger_on_connect = False


def check_bat(robot: cozmo.robot.Robot):
    # Volts on battery
    battery = robot.battery_voltage
    # check battery when requested
    if battery < 3.69:
        robot.play_anim_trigger(cozmo.anim.Triggers.NeedsSevereLowEnergyGetIn, in_parallel=True).wait_for_completed()
        robot.say_text("I need to charge my battery. Please, place me on the charger.", use_cozmo_voice=Voice, duration_scalar=0.65).wait_for_completed()
    else:
        robot.say_text("Let's continue...", use_cozmo_voice=Voice, duration_scalar=0.65).wait_for_completed()
        # Cozmo starts the analysis animation.
        robot.play_anim_trigger(cozmo.anim.Triggers.MeetCozmoScanningIdle, in_parallel=True)


def initial_settings(robot: cozmo.robot.Robot):
    # Set Neutral Face fot Cozmo
    robot.play_anim_trigger(cozmo.anim.Triggers.NeutralFace, in_parallel=True).wait_for_completed()
    # check if Cozmo is on charger
    charger = robot.is_on_charger
    # Set Cozmo volume
    robot.set_robot_volume(robot_volume=0.3)
    # Activate face expression estimation
    robot.enable_facial_expression_estimation()
    # Activate stop on cliff
    robot.enable_stop_on_cliff(enable=True)
    # Volts on battery
    battery = robot.battery_voltage
    # If Cozmo is on charger, drive off it to start FindFaces behavior
    if charger is True:
        robot.drive_off_charger_contacts(in_parallel=True).wait_for_completed()
        robot.drive_straight(distance_mm(120), speed_mmps(50), in_parallel=True)
    # Set lift to down position5
    robot.move_lift(-3)
    # Start "Battery check" animation
    robot.say_text("Checking battery level", in_parallel=True, use_cozmo_voice=Voice, duration_scalar=0.85).wait_for_completed()
    # Cozmo announce that he is ready to play if battery is higher then 3.6 volts - If less than 3.6 volts, Cozmo as to be placed on charger
    if battery > 3.69:
        robot.play_anim_trigger(cozmo.anim.Triggers.VC_Alrighty, in_parallel=True).wait_for_completed()
        robot.say_text("My battery is good! I am ready to play!", in_parallel=True, play_excited_animation=False, use_cozmo_voice=Voice, duration_scalar=0.85).wait_for_completed()
        robot.set_head_angle(degrees(30)).wait_for_completed()
    else:
        robot.play_anim_trigger(cozmo.anim.Triggers.SparkFailure).wait_for_completed()
        robot.play_anim_trigger(cozmo.anim.Triggers.NeedsSevereLowEnergyGetIn, in_parallel=True).wait_for_completed()
        robot.say_text("I need to charge my battery. Please, place me on the charger.", in_parallel=True, use_cozmo_voice=Voice, duration_scalar=0.85).wait_for_completed()

def scan_face(robot: cozmo.robot.Robot):
    # initial execution settings
    initial_settings(robot)
    face = None

    while True:

        if face and face.is_visible is True:

            # If Cozmo detects HAPPYNESS
            if face.expression == "happy" and face.expression_score > 90:
                robot.play_anim_trigger(cozmo.anim.Triggers.CozmoSaysSpeakGetInMedium, in_parallel=True).wait_for_completed()
                robot.set_all_backpack_lights(cozmo.lights.green_light)
                robot.say_text(happy, use_cozmo_voice=Voice, in_parallel=True, duration_scalar=0.85, voice_pitch=0.5).wait_for_completed()
                robot.set_backpack_lights_off()
                robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabHappy, in_parallel=True).wait_for_completed()
                robot.set_head_angle(degrees(30)).wait_for_completed()
                check_bat(robot)

            # If Cozmo detects SADNESS
            if face.expression == "sad" and face.expression_score > 90:
                robot.play_anim_trigger(cozmo.anim.Triggers.CozmoSaysSpeakGetInMedium, in_parallel=True).wait_for_completed()
                robot.set_all_backpack_lights(cozmo.lights.blue_light)
                robot.say_text(sad, use_cozmo_voice=Voice, in_parallel=True, duration_scalar=0.85, voice_pitch=-0.5).wait_for_completed()
                robot.set_backpack_lights_off()
                robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabUnhappy, in_parallel=True).wait_for_completed()
                robot.set_head_angle(degrees(30)).wait_for_completed()
                check_bat(robot)

            # If Cozmo detects AGGRESSIVENESS
            if face.expression == "angry" and face.expression_score > 90:
                robot.play_anim_trigger(cozmo.anim.Triggers.CozmoSaysSpeakGetInMedium, in_parallel=True).wait_for_completed()
                robot.set_all_backpack_lights(cozmo.lights.red_light)
                robot.say_text(angry, use_cozmo_voice=Voice, in_parallel=True, duration_scalar=0.85, voice_pitch=-0.5).wait_for_completed()
                robot.set_backpack_lights_off()
                robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabScaredCozmo, in_parallel=True).wait_for_completed()
                robot.set_head_angle(degrees(30)).wait_for_completed()
                check_bat(robot)

            # If Cozmo detects SURPRISE
            if face.expression == "surprised" and face.expression_score > 80:
                robot.play_anim_trigger(cozmo.anim.Triggers.CozmoSaysSpeakGetInMedium, in_parallel=True).wait_for_completed()
                robot.set_all_backpack_lights(cozmo.lights.white_light)
                robot.say_text(surprised, use_cozmo_voice=Voice, in_parallel=True, duration_scalar=0.85, voice_pitch=0.7).wait_for_completed()
                robot.set_backpack_lights_off()
                robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabSurprise, in_parallel=True).wait_for_completed()
                robot.set_head_angle(degrees(30)).wait_for_completed()
                check_bat(robot)

        else:
            # turn off backpack lights
            robot.set_backpack_lights_off()
            # Cozmo returns to FindFaces behavior
            robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)

            # try to find face for 30 seconds
            try:
                face = robot.world.wait_for_observed_face(timeout=30)
                # Cozmo stops Face detection and starts emotional prediction analysis
                robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces).stop()
                # Cozmo starts the analysis animation.
                robot.play_anim_trigger(cozmo.anim.Triggers.MeetCozmoScanningIdle, in_parallel=True)

            # When 30 seconds of the timeout set on FACE variable is reached, cozmo performs final animations and leave program
            except asyncio.TimeoutError:
                # Cozmo stops Face detection and starts final animations
                robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces).stop()
                robot.say_text("Where are you?", use_cozmo_voice=Voice, in_parallel=True, duration_scalar=0.78, voice_pitch=0.5).wait_for_completed()
                robot.play_anim_trigger(cozmo.anim.Triggers.ComeHere_SearchForFace, in_parallel=True).wait_for_completed()
                robot.say_text("Fine! I'll take a nap then!", use_cozmo_voice=Voice, in_parallel=True, duration_scalar=0.85).wait_for_completed()
                robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabSleep).wait_for_completed()
                return

        time.sleep(.7)


cozmo.run_program(scan_face, use_viewer=True, force_viewer_on_top=True)
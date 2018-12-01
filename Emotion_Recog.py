#!/usr/bin/env python3

import time
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Angle
import asyncio

# Ativa ou desativa a voz do Cozmo - True para voz e False para sintetizador
Voice = True

# Frases que vão ser ditas ao detectar as expressões
happy = "You look happy!"
sad = "You look sad."
angry = "You look angry."
surprised = "You look surprised!"
saudacao = None
bateria = None

def verifica_bat(robot: cozmo.robot.Robot):
    bateria = robot.battery_voltage
    if bateria < 3.6:
        robot.say_text("I need to charge my battery. Please, place me on the charger.", use_cozmo_voice=Voice, duration_scalar=0.65).wait_for_completed()
        robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabBored, in_parallel=True)
    else:
        robot.say_text("Let's continue...", use_cozmo_voice=Voice, duration_scalar=0.65).wait_for_completed()
    print("Nível da bateria:", bateria, "Volts")


def procura_Face(robot: cozmo.robot.Robot):
    robot.set_robot_volume(robot_volume=0.3)
    # valor dos volts na bateria
    bateria = robot.battery_voltage
    # verificar se esta no carregador
    carga = robot.is_on_charger
    # Reseta variável para face
    face = None
    # Ativa a detecção de expressões
    robot.enable_facial_expression_estimation()
    # Ajusta a cabeça - Primeiro indo para baixo e depois levantar em 15 graus
    robot.set_head_angle(cozmo.robot.MIN_HEAD_ANGLE, in_parallel=True).wait_for_completed()
    robot.set_head_angle(degrees(22), in_parallel=True).wait_for_completed()
    # Ajusta os braços para baixo
    robot.move_lift(-3)

    # MENSAGENS PARA O CONSOLE - STATUS E CONTEÚDO DE VARIÁVEIS
    print("Pressione CTRL-C para sair")
    print("Nível inicial da bateria:", bateria, "Volts")
    print(carga)

    # Cozmo anuncia que está pronto se a bateria estiver maior que 3.5volts
    if bateria > 3.6:
        robot.say_text("My battery is good! I am ready to play!", in_parallel=True, play_excited_animation=False, use_cozmo_voice=Voice, duration_scalar=0.75).wait_for_completed()
        robot.set_head_angle(degrees(22)).wait_for_completed()
    else:
        robot.say_text("I need to charge my battery. Please, place me on the charger.", in_parallel=True, use_cozmo_voice=Voice, duration_scalar=0.65).wait_for_completed()
        robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabBored, in_parallel=True).wait_for_completed()

    robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)

    while True:
        # Cozmo para a deteccao de rosto e inicia analise
        robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces).stop()
        # Cozmo inicia a detecção e reage como se estivesse analisando
        robot.play_anim_trigger(cozmo.anim.Triggers.MeetCozmoScanningIdle, in_parallel=True)

        if face and face.is_visible == True:

            # se cozmo interpreta felicidade, diz que você está feliz e reage
            if face.expression == "happy" and face.expression_score > 90:
                robot.play_anim_trigger(cozmo.anim.Triggers.CozmoSaysSpeakGetInMedium, in_parallel=True).wait_for_completed()
                robot.set_all_backpack_lights(cozmo.lights.green_light)
                robot.say_text(happy, use_cozmo_voice=Voice, in_parallel=True, duration_scalar=0.78).wait_for_completed()
                #robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabHappy, in_parallel=True).wait_for_completed()
                robot.set_backpack_lights_off()
                robot.set_head_angle(degrees(22)).wait_for_completed()
                verifica_bat(robot)

            # se cozmo interpreta tristeza, diz que você está triste e reage
            if face.expression == "sad" and face.expression_score > 90:
                robot.play_anim_trigger(cozmo.anim.Triggers.CozmoSaysSpeakGetInMedium, in_parallel=True).wait_for_completed()
                robot.set_all_backpack_lights(cozmo.lights.blue_light)
                robot.say_text(sad, use_cozmo_voice=Voice, in_parallel=True, duration_scalar=1.0).wait_for_completed()
                #robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabUnhappy, in_parallel=True).wait_for_completed()
                robot.set_backpack_lights_off()
                robot.set_head_angle(degrees(22)).wait_for_completed()
                verifica_bat(robot)

            # se cozmo interpreta raiva, diz que você está com raiva e reage
            if face.expression == "angry" and face.expression_score > 90:
                robot.play_anim_trigger(cozmo.anim.Triggers.CozmoSaysSpeakGetInMedium, in_parallel=True).wait_for_completed()
                robot.set_all_backpack_lights(cozmo.lights.red_light)
                robot.say_text(angry, use_cozmo_voice=Voice, in_parallel=True, duration_scalar=0.9).wait_for_completed()
                #robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabScaredCozmo, in_parallel=True).wait_for_completed()
                robot.set_backpack_lights_off()
                robot.set_head_angle(degrees(22)).wait_for_completed()
                verifica_bat(robot)

            # se cozmo interpreta surpresa, diz que você está surpreso e reage
            if face.expression == "surprised" and face.expression_score > 90:
                robot.play_anim_trigger(cozmo.anim.Triggers.CozmoSaysSpeakGetInMedium, in_parallel=True).wait_for_completed()
                robot.set_all_backpack_lights(cozmo.lights.white_light)
                robot.say_text(surprised, use_cozmo_voice=Voice, in_parallel=True, duration_scalar=0.78).wait_for_completed()
                #robot.play_anim_trigger(cozmo.anim.Triggers.VC_Listening, in_parallel=True).wait_for_completed()
                robot.set_backpack_lights_off()
                robot.set_head_angle(degrees(22)).wait_for_completed()
                verifica_bat(robot)

        else:
            # Desliga as luzes
            robot.set_backpack_lights_off()
            robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)

            # Espera até achar uma outra face para observar
            try:
                face = robot.world.wait_for_observed_face(timeout=60)

                if face and face.name:
                    # Cozmo para a deteccao de rosto e inicia analise
                    robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces).stop()
                    # Cozmo cumprimenta quem ele identificou
                    saudacao = "Hello %s!!!" % (face.name)
                    robot.say_text(saudacao, in_parallel=True).wait_for_completed()

            except asyncio.TimeoutError:
                print("Não tem ninguém por perto.")
                return

        time.sleep(.5)


cozmo.run_program(procura_Face, use_viewer=True, force_viewer_on_top=True)

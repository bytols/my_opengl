import pygame as pg
from pygame import mixer
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader
from models import Street, Tunel, exp_model, Square
from textures import Texture
from utils import create_shader_from_single_file
from props import Props_class
import pyrr
import time

class App():

    def __init__(self):

        pg.init()
        mixer.init()
        mixer.music.load("../song/music.wav")
        # create the window
        pg.display.set_mode((1080, 720) , pg.OPENGL|pg.DOUBLEBUF) #double buff logic
        # define the clear color for glclear
        glClearColor(0.1, 0.2, 0.3, 1)
        glEnable(GL_DEPTH_TEST)
        self.shader = create_shader_from_single_file("../shaders/texturizado.glsl")
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45,
            aspect=1080/720,
            near=0.1,
            far=100,
            dtype=np.float32
        )

        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"), 1, GL_FALSE, projection_transform
        )

        view_transform = pyrr.matrix44.create_look_at(
            eye = [0, 2, 5],
            target = [0, 0, -10],
            up = [0, 1, 0],
            dtype=np.float32
        )
        
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "view") , 1, GL_FALSE, view_transform
        )

        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")
        self.car_pos = [0, 1 , 2]
        self.main_car = exp_model("../models/vehicle-drag-racer.obj")
        self.obj_texture = Texture("../models/Textures/colormap.png")
        self.street = Street()
        self.street_texture = Texture("../textures/asfalto.png")
        self.tunel = Tunel()
        self.tunel_texture = Texture("../textures/tijolo.png")
        self.create_props = Props_class()
        self.back = Square(150.00 , 150.00)
        self.back_texture = Texture("../textures/background.png")
        self.empty = Square(20.00, 10.00)
        self.empty_texture = Texture("../textures/black.jpg")
        self.main_loop()


    def main_loop(self):
        running = True
        mixer.music.play()
        while (running):

            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
            keys = pg.key.get_pressed()
            if keys[pg.K_w] and self.car_pos[2] > -5: # Tecla 'A'
                self.car_pos[2] -= 0.01
            elif keys[pg.K_s] and self.car_pos[2] < 2: # Tecla 'D'
                self.car_pos[2] += 0.01
            elif keys[pg.K_a] and self.car_pos[0] > -2: # Tecla 'A'
                self.car_pos[0] -= 0.01
            elif keys[pg.K_d] and self.car_pos[0] < +2:
                self.car_pos[0] += 0.01
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.shader) 

            #draw background
            self.back_texture.use()
            glBindVertexArray(self.back.vao)
            posicao_back = [0, -17.5 , -80.0]
            matriz_back = pyrr.matrix44.create_from_translation(vec=posicao_back ,dtype=np.float32)
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, matriz_back)
            glDrawArrays(GL_TRIANGLES, 0, self.back.vertex_count)    

            #draw black_pit
            self.empty_texture.use()
            glBindVertexArray(self.empty.vao)
            posicao_empty = [0, 0 , -70.0]
            matriz_empty = pyrr.matrix44.create_from_translation(vec=posicao_empty ,dtype=np.float32)
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, matriz_empty)
            glDrawArrays(GL_TRIANGLES, 0, self.empty.vertex_count)    

            #draw street
            self.street_texture.use()
            glBindVertexArray(self.street.vao)
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)
            glDrawArrays(GL_TRIANGLES, 0, self.street.vertex_count)

            #draw tunel
            self.tunel_texture.use()
            glBindVertexArray(self.tunel.vao)
            posicao_tunel = [0, 0 , -25.0]
            matriz_tunel = pyrr.matrix44.create_from_translation(vec=posicao_tunel ,dtype=np.float32)
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, matriz_tunel)
            glDrawArrays(GL_TRIANGLES, 0, self.tunel.vertex_count)

            #draw car
            self.obj_texture.use()
            glBindVertexArray(self.main_car.vao)
            matriz_main_car = pyrr.matrix44.create_from_translation(vec=self.car_pos ,dtype=np.float32)
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, matriz_main_car)
            glDrawArrays(GL_TRIANGLES, 0, self.main_car.vertex_count)

            self.create_props.draw_props()
            if self.create_props.check_colision(self.car_pos) == True:
                print("bateu")
                running = False         

            pg.display.flip() # change to the second buffer
        self.quit()

    def quit(self):

        self.tunel.destroy()
        self.street.destroy()
        self.main_car.destroy()
        self.empty.destroy()
        self.back.destroy()
        pg.quit()

App()
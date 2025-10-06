import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader
from models import Street, Tunel, exp_model
from textures import Texture
from utils import create_shader_from_single_file
from props import check_colision
import pyrr

class App():

    def __init__(self):

        pg.init()
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
        self.prop_pos = [1, 1, -25]
        self.main_car = exp_model("../models/vehicle-drag-racer.obj")
        self.obj_texture = Texture("../models/Textures/colormap.png")
        self.street = Street()
        self.street_texture = Texture("../textures/asfalto.jpg")
        self.tunel = Tunel()
        self.tunel_texture = Texture("../textures/tijolo.jpg")
        self.cone = exp_model("../models/item-cone.obj")
        self.main_loop()


    def main_loop(self):
        running = True
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
            self.prop_pos[2] += 0.01
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.shader) 
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

            #draw cone
            self.obj_texture.use()
            glBindVertexArray(self.cone.vao)
            matriz_cone = pyrr.matrix44.create_from_translation(vec=self.prop_pos ,dtype=np.float32)
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, matriz_cone)
            glDrawArrays(GL_TRIANGLES, 0, self.cone.vertex_count)

            if check_colision(self.car_pos, self.prop_pos) == True:
                running = False
            

            pg.display.flip() # change to the second buffer
        self.quit()

    def quit(self):

        self.tunel.destroy()
        self.street.destroy()
        self.main_car.destroy()
        pg.quit()

App()
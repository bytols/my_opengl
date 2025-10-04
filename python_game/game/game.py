import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader
from models import Street
from textures import Texture
from utils import create_shader_from_single_file
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

        self.street = Street()
        self.street_texture = Texture("../textures/asfalto.jpg")
        self.main_loop()


    def main_loop(self):
        running = True
        while (running):

            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.shader)
            self.street_texture.use()
            glBindVertexArray(self.street.vao)
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)
            glDrawArrays(GL_TRIANGLES, 0, self.street.vertex_count)
            pg.display.flip() # change to the second buffer
        self.quit()

    def quit(self):

        pg.quit()

App()
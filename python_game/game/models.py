import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from utils import load_model_from_file

class Tunel():

    def __init__(self):

        largura_tunel = 8.0
        altura_tunel = 4.0
        comprimento_tunel = 35.0

        self.vertices = (
            # TETO (6 vértices)
            # Triângulo 1
            -largura_tunel/2, altura_tunel, 0,                  0.0, 1.0, # v3
            largura_tunel/2, altura_tunel, 0,                  1.0, 1.0, # v2
            largura_tunel/2, altura_tunel, -comprimento_tunel, 1.0, 0.0, # v6
            # Triângulo 2
            -largura_tunel/2, altura_tunel, 0,                  0.0, 1.0, # v3
            largura_tunel/2, altura_tunel, -comprimento_tunel, 1.0, 0.0, # v6
            -largura_tunel/2, altura_tunel, -comprimento_tunel, 0.0, 0.0, # v7

            # PAREDE ESQUERDA (6 vértices)
            # Triângulo 1
            -largura_tunel/2, 0,            0,                  1.0, 0.0, # v0
            -largura_tunel/2, altura_tunel, 0,                  1.0, 1.0, # v3
            -largura_tunel/2, altura_tunel, -comprimento_tunel, 0.0, 1.0, # v7
            # Triângulo 2
            -largura_tunel/2, 0,            0,                  1.0, 0.0, # v0
            -largura_tunel/2, altura_tunel, -comprimento_tunel, 0.0, 1.0, # v7
            -largura_tunel/2, 0,            -comprimento_tunel, 0.0, 0.0, # v4

            # PAREDE DIREITA (6 vértices)
            # Triângulo 1
            largura_tunel/2, 0,            0,                  0.0, 0.0, # v1
            largura_tunel/2, altura_tunel, 0,                  0.0, 1.0, # v2
            largura_tunel/2, altura_tunel, -comprimento_tunel, 1.0, 1.0, # v6
            # Triângulo 2
            largura_tunel/2, 0,            0,                  0.0, 0.0, # v1
            largura_tunel/2, altura_tunel, -comprimento_tunel, 1.0, 1.0, # v6
            largura_tunel/2, 0,            -comprimento_tunel, 1.0, 0.0, # v5
        )
        self.vertex_count = 18
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = len(self.vertices) // 5

        # creating manual for building the object
        self.vao = glGenVertexArrays(1)
        #ligando a instrução para a GPU com index 1?
        glBindVertexArray(self.vao)
        #creating the buffer that will hold the obj
        self.vbo = glGenBuffers(1)
        # binding the buffer to the gpu
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        # Definindo o tamanho do buffer
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        #definindo os atributos
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))

    def destroy(self):
            glDeleteVertexArrays(1, (self.vao,))
            glDeleteBuffers(1, (self.vbo,))


class Street():

    def __init__(self):

        largura = 5.0
        comprimento = 70.0
        altura = 1.0 

        # x, y, z, s, t, nx, ny, nz
        self.vertices = (
            # Triângulo 1
            -largura / 2, altura, -comprimento / 2,  0.0, 0.0, # Canto inferior esquerdo
             largura / 2, altura, -comprimento / 2,  1.0, 0.0, # Canto inferior direito
             largura / 2, altura,  comprimento / 2,  1.0, 1.0, # Canto superior direito

            # Triângulo 2
            -largura / 2, altura, -comprimento / 2,  0.0, 0.0, # Canto inferior esquerdo
             largura / 2, altura,  comprimento / 2,  1.0, 1.0, # Canto superior direito
            -largura / 2, altura,  comprimento / 2,  0.0, 1.0, # Canto superior esquerdo
        )
        # conveting to array
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = len(self.vertices) // 5

        # creating manual for building the object
        self.vao = glGenVertexArrays(1)
        #ligando a instrução para a GPU com index 1?
        glBindVertexArray(self.vao)
        #creating the buffer that will hold the obj
        self.vbo = glGenBuffers(1)
        # binding the buffer to the gpu
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        # Definindo o tamanho do buffer
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        #definindo os atributos
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))

class exp_model():

    def __init__(self, path):

        self.vertices = load_model_from_file(path)
        
        self.vertex_count = len(self.vertices) // 5

        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
        
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))
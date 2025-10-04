import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader


class Texture():

    def __init__(self, filepath):

        #criando uma texturea
        self.texture = glGenTextures(1)
        # ligando a textura ao gpu
        glBindTexture(GL_TEXTURE_2D, self.texture)
        #gpu params
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) #?
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT) #?
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST) #?
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) #?
        # carregando binário da imagem
        image = pg.image.load(filepath).convert_alpha()
        # pegando altura e comprimento da imagem
        image_width, image_height = image.get_rect().size
        # convertendo binário para string com RGBA
        image_data = pg.image.tostring(image, "RGBA")
        #criando imagem
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data) #?
        glGenerateMipmap(GL_TEXTURE_2D) #?

    def use(self):

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self):

        glDeleteTextures(1, (self.texture,))
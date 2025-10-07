import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader
from models import Street, Tunel, exp_model
from textures import Texture
from utils import create_shader_from_single_file
import pyrr
import time
import random

class Props_class():

    def __init__(self):
        self.shader = create_shader_from_single_file("../shaders/texturizado.glsl")
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45,
            aspect=1080/720,
            near=0.1,
            far=500,
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
        self.time = time.time()
        self.props = []
        self.texture = Texture("../models/Textures/colormap.png")
        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")
        self.count = 0
        self.velocidade = 5
        self.tempo_anterior = time.time()
        self.speed_time = time.time()
        self.spawn_time = 2
        self.models = [
            "../models/item-cone.obj",
            "../models/item-banana.obj",
            "../models/item-box.obj",
            "../models/wheel-small.obj",
            "../models/tree.obj",
        ]

    def draw_props(self):
        self.create_props()
        tempo_agora = time.time()
        deltaTime = tempo_agora - self.tempo_anterior
        self.tempo_anterior = tempo_agora
        for element in self.props:
            obj = element[0]
            position = element[1]
            self.texture.use()
            glBindVertexArray(obj.vao)
            matriz = pyrr.matrix44.create_from_translation(vec=position ,dtype=np.float32)
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, matriz)
            glDrawArrays(GL_TRIANGLES, 0, obj.vertex_count)
            position[2] += self.velocidade * deltaTime
            if position[2] > 2:
                obj.destroy()
                del self.props[0]
                self.count += 1
                print(f"pontuação: {self.count}")
            if (time.time() > self.speed_time + 10 and self.velocidade < 40):
                self.spawn_time -= 0.5
                self.speed_time = time.time()
                self.velocidade += 10
                print("speed up!")

    def create_props(self):
        now = time.time()
        if now > self.time + self.spawn_time and len(self.props) < 5:
            self.time = time.time()
            tex = random.randint(0,4)
            obj = exp_model(self.models[tex])
            position = random.randint (-2, 2)
            position_list = [position, 1, -25]
            element = [obj, position_list]
            self.props.append(element)

    def check_colision(self, pos_carro):
        """
        Verifica a colisão assumindo que ambos os objetos têm um "raio" de 0.5
        em cada eixo (ou seja, uma largura/profundidade total de 1.0).
        Retorna True se houver colisão, False caso contrário.
        """
        for element in self.props:
            pos_prop = element[1]
            # Calcula a distância absoluta (sempre positiva) entre os centros no eixo X
            distancia_x = abs(pos_carro[0] - pos_prop[0])
            
            # Calcula a distância absoluta entre os centros no eixo Z
            distancia_z = abs(pos_carro[2] - pos_prop[2])
            
            # A soma dos "meio-tamanhos" é 0.5 + 0.5 = 1.0
            tamanho_total_colisao = 0.6
            
            # Se a distância em AMBOS os eixos for menor que o tamanho total, há colisão
            if distancia_x < tamanho_total_colisao and distancia_z < tamanho_total_colisao:
                return True # Houve colisão!
            
        # Se não, eles estão separados em pelo menos um eixo
        return False # Sem colisão
            

        

        



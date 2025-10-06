import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader
from models import Street, Tunel, exp_model
from textures import Texture
from utils import create_shader_from_single_file
import pyrr

def check_colision(pos_carro, pos_prop):
    """
    Verifica a colisão assumindo que ambos os objetos têm um "raio" de 0.5
    em cada eixo (ou seja, uma largura/profundidade total de 1.0).
    Retorna True se houver colisão, False caso contrário.
    """
    
    # Calcula a distância absoluta (sempre positiva) entre os centros no eixo X
    distancia_x = abs(pos_carro[0] - pos_prop[0])
    
    # Calcula a distância absoluta entre os centros no eixo Z
    distancia_z = abs(pos_carro[2] - pos_prop[2])
    
    # A soma dos "meio-tamanhos" é 0.5 + 0.5 = 1.0
    tamanho_total_colisao = 1.0
    
    # Se a distância em AMBOS os eixos for menor que o tamanho total, há colisão
    if distancia_x < tamanho_total_colisao and distancia_z < tamanho_total_colisao:
        return True # Houve colisão!
        
    # Se não, eles estão separados em pelo menos um eixo
    return False # Sem colisão
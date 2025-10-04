import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader

def create_shader_from_single_file(filepath):
    """
    Lê um único arquivo .glsl que contém ambos os shaders (vertex e fragment),
    separados por #shader vertex e #shader fragment, e compila o programa.
    """
    
    shader_sources = {GL_VERTEX_SHADER: [], GL_FRAGMENT_SHADER: []}
    current_shader_type = None

    with open(filepath, 'r') as f:
        for line in f:
            if '#shader vertex' in line:
                current_shader_type = GL_VERTEX_SHADER
            elif '#shader fragment' in line:
                current_shader_type = GL_FRAGMENT_SHADER
            elif current_shader_type:
                shader_sources[current_shader_type].append(line)

    # Converte as listas de linhas em strings únicas
    vertex_src = "".join(shader_sources[GL_VERTEX_SHADER])
    fragment_src = "".join(shader_sources[GL_FRAGMENT_SHADER])
    
    # Compila o programa da mesma forma que antes, mas com as fontes separadas
    shader = compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(fragment_src, GL_FRAGMENT_SHADER)
    )
    
    return shader
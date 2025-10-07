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

# Em um arquivo como utils.py

def load_model_from_file(filepath):
    """
    Lê um arquivo .obj e retorna uma tupla de vértices
    no formato (x, y, z, u, v).
    """
    v = []   # Lista de posições de vértices (x,y,z)
    vt = []  # Lista de coordenadas de textura (u,v)
    vn = []  # Lista de normais (não vamos usar por enquanto)
    
    vertices_finais = []

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            parts = line.split()
            
            if parts[0] == 'v':
                # Posição do vértice
                v.append([float(parts[1]), float(parts[2]), float(parts[3])])
                
            elif parts[0] == 'vt':
                # Coordenada de textura
                vt.append([float(parts[1]), float(parts[2])])
                
            elif parts[0] == 'vn':
                # Normal (guardamos mas não usamos ainda)
                vn.append([float(parts[1]), float(parts[2]), float(parts[3])])
                
            elif parts[0] == 'f':
                # Face no formato: f v1/vt1/vn1 v2/vt2/vn2 v3/vt3/vn3
                face_data = parts[1:]
                
                # Coleta os vértices da face
                face_vertices = []
                for vertex_data in face_data:
                    indices = vertex_data.split('/')
                    
                    # Índices começam em 1 no .obj
                    v_idx = int(indices[0]) - 1
                    
                    # Coordenada de textura (segunda posição)
                    if len(indices) > 1 and indices[1]:
                        vt_idx = int(indices[1]) - 1
                        if vt_idx >= 0 and vt_idx < len(vt):
                            tex_coord = vt[vt_idx]
                        else:
                            tex_coord = [0.0, 0.0]
                    else:
                        tex_coord = [0.0, 0.0]
                    
                    position = v[v_idx]
                    face_vertices.append((position, tex_coord))
                
                # Triangula a face se tiver mais de 3 vértices
                for i in range(1, len(face_vertices) - 1):
                    # Cria triângulo com vértices 0, i, i+1
                    for idx in [0, i, i+1]:
                        pos, tex = face_vertices[idx]
                        vertices_finais.extend(pos)
                        vertices_finais.extend(tex)
    
    return tuple(vertices_finais)



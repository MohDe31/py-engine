from typing import Any
from OpenGL.GL import *

import numpy as np


BASIC_VERT = """
#version 310 es
precision highp float;

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;

out vec3 fColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    fColor = aColor;
}
"""

BASIC_FRAG = """
#version 310 es
precision highp float;

out vec4 FragColor;

in vec3 fColor;

void main()
{
    FragColor = vec4(fColor, 1.0f);
} 
"""

class Shader:
    
    ID = None

    @staticmethod
    def load_basic():
        shader = Shader()

        shader.load(BASIC_VERT, BASIC_FRAG)

        return shader

    def from_file(vertex_path, fragment_path):
        with open(vertex_path) as f:
            vert = f.read()

        with open(fragment_path) as f:
            frag = f.read()

        shader = Shader()

        shader.load(vert, frag)

        return shader

    def load(self, vert, frag):
        vertexShader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertexShader, vert)
        glCompileShader(vertexShader)
        

        success = glGetShaderiv(vertexShader, GL_COMPILE_STATUS)

        if not success:
            logs = glGetShaderInfoLog(vertexShader)
            assert False, f'[ERROR::SHADER::VERTEX::COMPILATION_FAILED]\n {logs}'


        fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)

        
        glShaderSource(fragmentShader, frag)
        glCompileShader(fragmentShader)

        success = glGetShaderiv(fragmentShader, GL_COMPILE_STATUS)

        if not success:
            logs = glGetShaderInfoLog(fragmentShader)
            assert False, f'[ERROR::SHADER::FRAGMENT::COMPILATION_FAILED]\n {logs}'


        self.ID = glCreateProgram()

        glAttachShader(self.ID, vertexShader)
        glAttachShader(self.ID, fragmentShader)
        glLinkProgram(self.ID)

        success = glGetProgramiv(self.ID, GL_LINK_STATUS)

        if not success:
            logs = glGetProgramInfoLog(self.ID)
            assert False, f'[ERROR::PROGRAM::LINKING_FAILED]\n {logs}'

        glDeleteShader(vertexShader)
        glDeleteShader(fragmentShader)
    
    def __init__(self) -> None:
        pass

    def use(self):
        glUseProgram(self.ID)

    def setBool(self, name: str, value: bool):
        glUniform1i(glGetUniformLocation(self.ID, name), int(value))

    def setInt(self, name: str, value: int):
        glUniform1i(glGetUniformLocation(self.ID, name), value)

    def setFloat(self, name: str, value: float):
        glUniform1f(glGetUniformLocation(self.ID, name), value)

    def setMat4(self, name: str, value: Any):
        glUniformMatrix4fv(glGetUniformLocation(self.ID, name), 1, GL_FALSE, np.matrix(value).T)
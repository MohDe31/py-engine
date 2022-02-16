from typing import Any
from OpenGL.GL import *

import numpy as np

class Shader:
    
    ID = None

    def __init__(self, vertex_path, fragment_path) -> None:
        vertexShader = glCreateShader(GL_VERTEX_SHADER)

        with open(vertex_path) as f:
            data = f.read()
        
        glShaderSource(vertexShader, data)
        glCompileShader(vertexShader)

        success = glGetShaderiv(vertexShader, GL_COMPILE_STATUS)

        if not success:
            logs = glGetShaderInfoLog(vertexShader)
            assert False, f'[ERROR::SHADER::VERTEX::COMPILATION_FAILED]\n {logs}'

        fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)

        with open(fragment_path) as f:
            data = f.read()
        
        glShaderSource(fragmentShader, data)
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


    def use(self):
        glUseProgram(self.ID)

    def setBool(self, name: str, value: bool):
        glUniform1i(glGetUniformLocation(self.ID, name), int(value))

    def setInt(self, name: str, value: int):
        glUniform1i(glGetUniformLocation(self.ID, name), value)

    def setFloat(self, name: str, value: float):
        glUniform1f(glGetUniformLocation(self.ID, name), value)

    def setMat4(self, name: str, value: Any):
        glUniformMatrix4fv(glGetUniformLocation(self.ID, name), 1, GL_FALSE, value)
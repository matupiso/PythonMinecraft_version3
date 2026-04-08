#version 330 core

layout (location = 0) in vec2 in_tex_coord_0;
layout (location = 1) in vec3 in_position;

uniform mat4 proj;
uniform mat4 view;
uniform mat4 model;


out vec2 uv;


void main() {
    uv = in_tex_coord_0;

    gl_Position = proj * view * model * vec4(in_position, 1.0);
}
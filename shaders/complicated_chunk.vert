#version 330 core


layout (location = 0) in vec3 in_position;
layout (location = 1) in float tex_type;
layout (location = 2) in vec2 in_uv;



uniform mat4 model;
uniform mat4 proj;
uniform mat4 view;


flat out int type;

out vec2 uv;


void main(){
    uv = in_uv;
    type = int(tex_type);
    gl_Position = proj * view * model * vec4(in_position, 1);
}
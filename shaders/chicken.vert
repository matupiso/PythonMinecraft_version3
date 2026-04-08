#version 330 core


layout (location = 0) in vec3 in_position;


uniform mat4 model;
uniform mat4 proj;
uniform mat4 view;


flat out int t;


void main(){

    gl_Position = proj * view  * model * vec4(in_position, 21);
    t = int(in_position.x * in_position.y + in_position.z);
}
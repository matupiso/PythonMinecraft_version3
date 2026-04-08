#version 330 core

layout (location = 0) out vec4 fragColor;


in vec2 uv;

uniform sampler2D image;
uniform int tfi;
uniform vec2 water_screen;

void main() {
    vec3 tex = texture(image, uv).rgb; 
    if (tex.r == 0 && tex.b == 0 && tex.g == 0){
        fragColor = vec4(0, 0, 0, 0);
    }else if (tex.r == 1 && tex.g == 0 && tex.b == 0){
        fragColor = vec4(0, 0, 1, water_screen.y);
    }else{
        fragColor = vec4(tex, 1.0);
    }
}


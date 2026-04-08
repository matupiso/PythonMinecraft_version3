#version 330 core

layout (location = 0) out vec4 fragColor;


in vec2 uv;

uniform sampler2D u_texture_0;

void main() {
    fragColor = texture(u_texture_0, uv);
    fragColor.a = (fragColor.r + fragColor.b > 1.0) ? 0.0 : 1.0;
    fragColor.rgb -= vec3(0.9, 0.9, 0.9);
}
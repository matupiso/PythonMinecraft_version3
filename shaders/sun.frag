#version 330 core

layout (location = 0) out vec4 fragColor;


in vec2 uv;

uniform sampler2D u_texture_0;

void main() {
    vec3 tex_col = texture(u_texture_0, uv).rgb;

    tex_col = vec3(1, 1, 1);

    fragColor = vec4(tex_col, 1);
}
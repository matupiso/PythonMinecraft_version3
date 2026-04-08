#version 330 core


layout (location = 0) in ivec3 in_position;
layout (location = 1) in int voxel_id;
layout (location = 2) in int face_id;
layout (location = 3) in int ao_id;
layout (location = 4) in int light_id;
layout (location = 5) in int crack_id;




uniform mat4 model;
uniform mat4 proj;
uniform mat4 view;


flat out int Voxel_id;
flat out int Face_id;
flat out int light;
flat out int Break_index;


out vec2 uv;
out vec3 ao_value;
out vec3 voxel_color;

const vec2 uv_coords[4] = vec2[4](
    vec2(0, 0), vec2(0, 1),
    vec2(1, 0), vec2(1, 1)
);

const int uv_indicies[12] = int[12](
    1, 0, 2, 1, 2, 3, //even faces
    3, 0, 2, 3, 1, 0 // odd faces
);

vec3 hash31(float p){
    vec3 p3 = fract(vec3(p * 21.2) * vec3(0.1031, 0.1030, 0.0973)); 
    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.xxy + p3.yzz) * p3.zyx)  + 0.05;
}
const vec3 ao_values[4] = vec3[4](
    vec3(0.2), vec3(0.35), vec3(0.65), vec3(0.998)
);

void main(){
    Break_index = crack_id;

    light = light_id;
    int uv_index = gl_VertexID % 6 + (face_id & 1)  * 6;
    uv = uv_coords[uv_indicies[uv_index]];
    ao_value = ao_values[ao_id];
    voxel_color = hash31(voxel_id);

    Face_id = face_id;
    Voxel_id = voxel_id;

    
    gl_Position = proj * view * model * vec4(in_position, 1);
}
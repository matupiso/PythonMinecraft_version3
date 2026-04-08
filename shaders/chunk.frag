#version 330 core

layout (location = 0) out vec4 fragColor;


const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

uniform sampler2DArray u_texture_array_0;
uniform sampler2DArray block_breaking_array;
uniform vec3 bg_color;
uniform vec3 sun_light;




in vec2 uv;
in vec3 ao_value;
in vec3 voxel_color;

flat in int Voxel_id;
flat in int Face_id;
flat in int light;
flat in int Break_index;


void main(){
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(Face_id, 2) / 3.0;

    vec3 tex_col = texture(u_texture_array_0, vec3(face_uv, Voxel_id)).rgb;
    int crack_index = Break_index;
    if (Break_index < 6){
        crack_index = 5 - crack_index;
    }
    vec3 break_tex_col = texture(block_breaking_array, vec3(uv, crack_index)).rgb;


    //tex_col *= voxel_color;
    tex_col = pow(tex_col, gamma);
    tex_col *= sun_light;
    tex_col *= ao_value;
    tex_col = pow(tex_col, inv_gamma);
    if (Break_index < 6){
    tex_col *= break_tex_col;
    }
    tex_col *= clamp(((light /  100) + 0.25), 0, 1);
    
    //fog 
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
    tex_col = mix(tex_col, bg_color, (1.0 - exp2(-0.000015 * fog_dist * fog_dist)));

    if (Voxel_id == 13 && tex_col.x == 0){
        fragColor = vec4(tex_col,  0.01);
    }else if (Voxel_id == 15){
        fragColor = vec4(tex_col, 0.5);
    }else{
        fragColor = vec4(tex_col, 1);
    }
  

    
   
}   
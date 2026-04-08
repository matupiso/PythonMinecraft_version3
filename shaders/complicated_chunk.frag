#version 330 core

layout (location = 0) out vec4 fragColor;

uniform sampler2D torch_top;
uniform sampler2D torch_side;
uniform sampler2D tf_1;
uniform sampler2D tf_2;
uniform sampler2D tf_3;
uniform sampler2D tf_4;
uniform sampler2D tf_5;
uniform sampler2D tf_6;
uniform sampler2D glass_side;



in vec2 uv;

flat in int type;


void main(){
    
    if (type == 0){
        fragColor = texture(torch_top, uv);
    }else if (type == 1){
        fragColor = texture(torch_side, uv);
    }else if (type == 2){
        fragColor = texture(tf_1, uv);
    }else if (type == 3){
        fragColor = texture(tf_2, uv);
    }else if (type == 4){
        fragColor = texture(tf_3, uv);
    }else if (type == 5){
        fragColor = texture(tf_4, uv);
    }else if (type == 6){
        fragColor = texture(tf_5, uv);
    }else if (type == 7){
        fragColor = texture(tf_6, uv);
    }else if (type == 8){
        vec4 tex_col = texture(glass_side, uv);
        if (tex_col.x == 0){
            fragColor = vec4(0, 0, 0, 0);
        }else{  
            fragColor = tex_col;
        }
        
    }else{
        fragColor = vec4(1);
    }

        if (type > 1 && type <= 7 && fragColor.rgb == vec3(0, 0, 0)){fragColor = vec4(0);}
}
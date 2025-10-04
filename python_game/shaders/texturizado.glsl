#shader vertex
#version 330 core

layout (location=0) in vec3 aPos;
layout (location=1) in vec2 aTexCoord;

out vec2 v_texCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    v_texCoord = aTexCoord;
}

#shader fragment
#version 330 core

in vec2 v_texCoord;

out vec4 FragColor;

uniform sampler2D imageTexture;

void main()
{
    FragColor = texture(imageTexture, v_texCoord);
}
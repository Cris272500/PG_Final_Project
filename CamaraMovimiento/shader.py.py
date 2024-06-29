import moderngl

def load_shader(ctx):
    program = ctx.program(
        vertex_shader="""
        #version 330

        in vec3 in_position;
        in vec3 in_normal;

        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;

        void main() {
            gl_Position = projection * view * model * vec4(in_position, 1.0);
        }
        """,
        fragment_shader="""
        #version 330

        out vec4 frag_color;

        void main() {
            frag_color = vec4(1.0, 0.0, 0.0, 1.0);
        }
        """
    )
    return program

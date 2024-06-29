from vbo import VBO
from shader_program import ShaderProgram


class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        # cube vao
        self.vaos['cube'] = self.get_vao(
            program=self.program.programs['default'],
            vbo = self.vbo.vbos['cube'])

        # shadow cube vao
        self.vaos['shadow_cube'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo = self.vbo.vbos['cube'])

        #  gradas vao
        self.vaos['cat'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['cat'])

        # gradas cat vao
        self.vaos['shadow_cat'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['cat'])
        # cesped
        self.vaos['cesped'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['cesped'])

        # shadow cesped vao
        self.vaos['shadow_cesped'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['cesped'])

        # detalles
        self.vaos['detalles'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['detalles'])

        # shadow detalles vao
        self.vaos['shadow_detalles'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['detalles'])




        

        # vestuario
        self.vaos['vestuario'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['vestuario'])

        # shadow vestuario vao
        self.vaos['shadow_vestuario'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['vestuario'])


        # cesped
        self.vaos['trofeo2'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['trofeo2'])

    
        self.vaos['shadow_trofeo2'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['trofeo2'])


        
        self.vaos['trofeo'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['trofeo'])

        # shadow cvao
        self.vaos['shadow_trofeo'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['trofeo'])

        self.vaos['champ'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['champ'])

        # shadow cvao
        self.vaos['shadow_champ'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['champ'])

        self.vaos['mundial'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['mundial'])

        # shadow cvao
        self.vaos['shadow_mundial'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['mundial'])


        self.vaos['ball'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['ball'])

        # shadow cvao
        self.vaos['shadow_ball'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['ball'])

        self.vaos['serie'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['serie'])

        # shadow cvao
        self.vaos['shadow_serie'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['serie'])






        # skybox vao
        self.vaos['skybox'] = self.get_vao(
            program=self.program.programs['skybox'],
            vbo=self.vbo.vbos['skybox'])

        # advanced_skybox vao
        self.vaos['advanced_skybox'] = self.get_vao(
            program=self.program.programs['advanced_skybox'],
            vbo=self.vbo.vbos['advanced_skybox'])

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)], skip_errors=True)
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()

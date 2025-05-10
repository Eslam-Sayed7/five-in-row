import pywavefront
from OpenGL.GL import *
from OpenGL.GLU import *

class ObjLoader:
    @staticmethod
    def load_obj(models, path, name=None):
        model = pywavefront.Wavefront(
            path, 
            collect_faces=True,
            create_materials=True,
            parse=True,
            strict=False
        )
        if name:
            models[name] = model
        return model
    
    @staticmethod
    def draw_obj(model, position=(0, 0, 0), rotation=(0, 1, 0, 0), scale = (1,1,1)):
        if model is None:
            return
        glPushMatrix()

        glTranslatef(*position)
        angle, rx, ry, rz = rotation
        if angle != 0:
            glRotatef(angle, rx, ry, rz)
        sx,sy,sz = scale
        glScalef(sx,sy,sz)

        for mesh in model.mesh_list:
            if mesh.materials:
                material = mesh.materials[0]
                if hasattr(material, 'diffuse'):
                    glColor3fv(material.diffuse[:3])
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3fv(model.vertices[vertex_i])
            glEnd()
        glPopMatrix()


from PIL import Image


bl_info = {
    "name": "GridPlacer",
    "author": "Alfy Benny",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Creates a surface plot for a given matrix data",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

import bpy
import random
import numpy as np
import re

def main(context):
    bound = 1
    '''
    ngrid = 20
    
    x = np.linspace(-bound, bound, ngrid)
    y = np.linspace(-bound, bound, ngrid)

    def PES(x, y):
        return x**2 + y**2

    X, Y = np.meshgrid(x, y)

    pes_data = PES(X, Y)
    '''
    #--------------

    pes_file = bpy.path.abspath('data.txt')
    pes_data = np.genfromtxt(pes_file)

    x = np.linspace(-bound,bound, len(pes_data))
    y = np.linspace(-bound, bound, len(pes_data))

    #--------------

    def make_surface(x, y, z, meshname, objname):
        verts = []
        faces = []

        for i in range(0, len(x)):
            for j in range(0, len(y)):
                vert = (x[i], y[j], z[i][j]) 
                verts.append(vert)

        # Fill faces
        counta = 0
        N = len(pes_data)
        for i in range(0, N*(N-1)):
            if counta  < N-1:
                A = i
                B = i+1
                C = (i+N)+1
                D = (i+N)
                
                face = (A, B, C, D)
                faces.append(face)
                counta = counta + 1
                
            else:
                counta = 0    

        # Create mesh and object
        mesh = bpy.data.meshes.new(meshname)
        object = bpy.data.objects.new(objname, mesh)

        #set mesh location
        object.location = bpy.context.scene.cursor.location
        bpy.context.collection.objects.link(object)


        #create mesh from python data
        mesh.from_pydata(verts,[],faces)
        mesh.update(calc_edges=True)

        #item = bpy.context.object
        #object.data.materials.append(bpy.data.materials['wpckt'])


    make_surface(x, y, pes_data, 'wpckt0', 'wpckt0_obj')


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    def execute(self, context):
        main(context)
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SimpleOperator.bl_idname, text=SimpleOperator.bl_label)

#-----------------------------------

class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Layout Demo"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # Big render button
        layout.label(text="Big Button:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("object.simple_operator")

# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(SimpleOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    bpy.utils.register_class(LayoutDemoPanel)

def unregister():
    bpy.utils.unregister_class(SimpleOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(LayoutDemoPanel)


if __name__ == "__main__":
    register()

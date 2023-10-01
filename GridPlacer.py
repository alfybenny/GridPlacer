bl_info = {
    "name": "BlendGridder",
    "author": "Alfy Benny",
    "version": (1, 1),
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
#----------------------------------------------------------------
def make_material():
    material = bpy.data.materials.new(name='surf_material')
    material.use_nodes=True
    material_nodes = material.node_tree.nodes
    material_link = material.node_tree.links
    material_nodes['Principled BSDF'].inputs['Metallic'].default_value=1.0

    node_coloramp = material_nodes.new('ShaderNodeValToRGB')
    node_coloramp.location = (100,100)


    node_grd_txt = material_nodes.new('ShaderNodeTexGradient')
    node_grd_txt.location = (70,100)

    node_XYZ = material_nodes.new('ShaderNodeSeparateXYZ')
    node_XYZ.location = (50,100)

    node_texcoor = material_nodes.new('ShaderNodeTexCoord')
    node_texcoor.location = (20,100)
    # link
    material_link.new(node_coloramp.outputs[0], material_nodes['Principled BSDF'].inputs[0])
    material_link.new(node_grd_txt.outputs[0], node_coloramp.inputs[0])
    material_link.new(node_XYZ.outputs[2], node_grd_txt.inputs[0])
    material_link.new(node_texcoor.outputs[0], node_XYZ.inputs[0])

    #How to add materials
    #'https://www.youtube.com/watch?v=WpI0_uzd9Bs'

    # Coloring
    node_coloramp.color_ramp.elements.new(position = 0.500)
    node_coloramp.color_ramp.elements[1].color = (0, 1, 0, 1)
    node_coloramp.color_ramp.elements[0].color = (1, 0, 0, 1)
    node_coloramp.color_ramp.elements[2].color = (0, 0, 1, 1)
#----------------------------------------------------------------
def main(context, z_height, bound_val):
    make_material()
    print(bound_val)
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
                vert = (x[i], y[j], z[i][j]*int(z_height)) 
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
        object.data.materials.append(bpy.data.materials['surf_material'])


    make_surface(x, y, pes_data, 'wpckt0', 'wpckt0_obj')

#----------------------------------------------------------------
class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Generate surface"
    
    z_height: bpy.props.StringProperty(name="z_height")
    bound_val: bpy.props.StringProperty(name="bound_val")

    def execute(self, context):
        main(context, self.z_height, self.bound_val)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

def menu_func(self, context):
    self.layout.operator(SimpleOperator.bl_idname, text=SimpleOperator.bl_label)

#-----------------------------------

class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Gird Placer"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        
        # Big render button
        layout.label(text="NOTE: a 'data.txt' file with matrix data should be present in the same folder where this blender file is saved")
        row = layout.row()
        row.scale_y = 2.0
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

import bpy

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
import fbx
import json


def fbx_to_json(fbx_file_path):
    
    fbx_file = fbx.load(fbx_file_path)
    
    output = {}
    
    # Hierarchy
    output['hierarchy'] = [] 
    for c in fbx_file.hierarchy:
        hierarchy_data = {
            'name': c.name,
            'parent': c.parent.name if c.parent else None,
            'children': [ch.name for ch in c.children]
        }
        output['hierarchy'].append(hierarchy_data)

    # Nodes 
    output['nodes'] = []
    for node in fbx_file.nodes:
        node_data = {
            'name': node.name,
            'transformation': node.transformation.tolist(),
            'hierarchy': node.hierarchy.name
        }
        output['nodes'].append(node_data)
        
    # Extract nodes
    output['nodes'] = []
    for node in fbx_file.nodes:
        node_data = {
            'name': node.name,
            'transformation': node.transformation.tolist() 
        }
        output['nodes'].append(node_data)

    # Extract meshes
    output['meshes'] = [] 
    for mesh in fbx_file.meshes:
        mesh_data = {
            'name': mesh.name,
            'vertices': mesh.vertices.tolist(),
            'faces': mesh.faces.tolist()
        }
        output['meshes'].append(mesh_data)
        
    # Extract materials
    output['materials'] = []
    for material in fbx_file.materials:
        material_data = {
            'name': material.name,
            'shading_model': material.shading_model, 
            'properties': material.properties
        }
        output['materials'].append(material_data)

    # Textures
    output['textures'] = []
    for texture in fbx_file.textures:
        texture_data = {
            'name': texture.name,
            'filename': texture.filename,
            'properties': texture.properties
        }
        output['textures'].append(texture_data)

    # Animations
    output['animations'] = []
    for anim in fbx_file.animations:
        animation_data = {
            'name': anim.name,
            'start': anim.start,
            'end': anim.end,
            'curves': [{'node': c.node.name, 'curves': c.curves} 
                    for c in anim.curves]  
        }
        output['animations'].append(animation_data)
        
    # Cameras 
    output['cameras'] = []    
    for cam in fbx_file.cameras:
        camera_data = {
            'name': cam.name,
            'position': cam.position.tolist(),
            'interest': cam.interest.tolist(),
            # other properties
        }
        output['cameras'].append(camera_data)   

    # Lights
    output['lights'] = []
    for light in fbx_file.lights:
        light_data = {
            'name': light.name,
            'type': light.light_type,
            'position': light.position.tolist(),
            # other properties
        }
        output['lights'].append(light_data)
        
    with open('scene.json', 'w') as f:
        json.dump(output, f)
        
        with open(fbx_file_path.replace('.fbx', '.json'), 'w') as f:
            json.dump(output, f)

if __name__ == "__main__":
    fbx_file_path = "LoaderCoder/Lunar_Wolf.fbx" 
    fbx_to_json(fbx_file_path)
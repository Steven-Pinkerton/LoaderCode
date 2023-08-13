import json
import os
import fbx

def fbx_to_json(fbx_file_path):

    # Load FBX 
    manager = fbx.FbxManager()
    importer = fbx.FbxImporter(manager)
    scene = importer.importFile(fbx_file_path)

    output = {
        'metadata': {},
        'nodes': [],
        'meshes': [],
        'materials': [],
        'animations': [],
        'cameras': [],
        'lights': []
    }

    # Metadata
    output['metadata']['creator'] = scene.GetSceneInfo().original_author.decode()

    # Nodes
    for node in scene.GetSrcObject(fbx.FbxNode.ClassId).GetNodeAttributeCount():
        attr = scene.GetSrcObject(fbx.FbxNode.ClassId).GetNodeAttributeByIndex(i)
        attr_type = attr.GetAttributeType()
        if attr_type == fbx.FbxNodeAttribute.eMesh:
            # Extract mesh node data
            for i in range(scene.GetSrcObject(fbx.FbxNode.ClassId).GetNodeAttributeCount()): 
                attr = scene.GetSrcObject(fbx.FbxNode.ClassId).GetNodeAttributeByIndex(i)
                if attr.GetAttributeType() == fbx.FbxNodeAttribute.eMesh:
                    mesh = attr.GetNode() 
                    mesh_data = {
                        'name': mesh.GetName(),
                        'vertices': mesh.GetControlPoints(), 
                        'polygons': mesh.GetPolygonVertices()
                    }
                    output['meshes'].append(mesh_data)
            
            
        elif attr_type == fbx.FbxNodeAttribute.eCamera:
            # Extract camera node data
            for i in range(scene.GetSrcObject(fbx.FbxNode.ClassId).GetNodeAttributeCount()):
                attr = scene.GetSrcObject(fbx.FbxNode.ClassId).GetNodeAttributeByIndex(i) 
                if attr.GetAttributeType() == fbx.FbxNodeAttribute.eCamera:
                    cam = attr.GetNode()
                    camera_data = {
                        'name': cam.GetName(),
                        'position': list(cam.LclTranslation.Get()),
                        'rotation': list(cam.LclRotation.Get()), 
                        'fov': cam.FieldOfView.Get()
                    }
                    output['cameras'].append(camera_data)

        
        elif attr_type == fbx.FbxNodeAttribute.eLight:
            # Extract light node data
            for i in range(scene.GetSrcObject(fbx.FbxNode.ClassId).GetNodeAttributeCount()):
                attr = scene.GetSrcObject(fbx.FbxNode.ClassId).GetNodeAttributeByIndex(i)
                if attr.GetAttributeType() == fbx.FbxNodeAttribute.eLight:
                    light = attr.GetNode()
                    light_data = {
                        'name': light.GetName(),
                        'type': light.LightType.Get(),
                        'position': list(light.LclTranslation.Get()),
                        'rotation': list(light.LclRotation.Get())
                    }
                    output['lights'].append(light_data)
        else:
            for i in range(scene.GetSrcObject(fbx.FbxNode.ClassId).GetNodeAttributeCount()):
                attr = scene.GetSrcObject(fbx.FbxNode.ClassId).GetNodeAttributeByIndex(i)
                if attr.GetAttributeType() == fbx.FbxNodeAttribute.eNull:
                    node = attr.GetNode()
                    node_data = {
                        'name': node.GetName(),
                        'translation': list(node.LclTranslation.Get()),
                        'rotation': list(node.LclRotation.Get()),
                        'scaling': list(node.LclScaling.Get()) 
                    }
                    output['nodes'].append(node_data)

    # Meshes
    for mesh in scene.GetSrcObject(fbx.FbxMesh.ClassId):
        mesh_data = {
            'name': mesh.GetName(),
            'vertices': mesh.GetControlPoints(),
            'polygons': mesh.GetPolygonVertices()
        }
        output['meshes'].append(mesh_data)

    # Materials 
    for mat in scene.GetSrcObject(fbx.FbxSurfaceMaterial.ClassId):
        mat_data = {
            'name': mat.GetName(),
            'shading_model': mat.ShadingModel.Get(),
            'properties': mat.GetProperties()
        }
        output['materials'].append(mat_data) 

    # Animations
    for anim in scene.GetSrcObject(fbx.FbxAnimStack.ClassId):
        anim_data = {
            'name': anim.GetName(),
            'start': anim.LocalStart.Get(),
            'end': anim.LocalStop.Get()
        }
        output['animations'].append(anim_data)

    # Cameras
    for cam in scene.GetSrcObject(fbx.FbxCamera.ClassId):
        cam_data = {
            'name': cam.GetName(),
            'position': list(cam.Position.Get()),
            'up_vector': list(cam.UpVector.Get()),
            'interest_position': list(cam.InterestPosition.Get()),
        }
        output['cameras'].append(cam_data)
    
    # Lights
    for light in scene.GetSrcObject(fbx.FbxLight.ClassId):
        light_data = {
            'name': light.GetName(),
            'type': light.LightType.Get(),
            'position': list(light.Position.Get()),
            'color': list(light.Color.Get())
        }
        output['lights'].append(light_data)

    # Write JSON
    with open('output.json', 'w') as f:
        json.dump(output, f)

def main():
    # Get project root directory path
    root_dir = os.path.dirname(os.path.abspath(__file__)) 
    fbx_path = os.path.join(root_dir, '../Lunar_wolf.fbx')


    fbx_to_json(fbx_path)

if __name__ == '__main__':
    main()
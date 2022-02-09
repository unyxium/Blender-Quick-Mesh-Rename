
bl_info = {
    "name": "Quick Mesh Rename",
    "author": "unyxium",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "Search for Quick Mesh Rename",
    "description": "Rename all mesh data blocks with the name of their parent object.",
    "category": "Mesh",
}

import bpy

class QuickMeshRename(bpy.types.Operator):
    bl_idname = "object.quick_mesh_rename"
    bl_label = "Quick Mesh Rename"
    bl_description = "Rename all mesh data blocks with the name of their parent object."
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        named_meshes = [] # stores the new mesh names of meshes with multiple users
        named_meshes_count = 0
        
        # iterate through every object:
        for object in bpy.data.objects:
            
            if object.data.users == 1:
                # object uses this mesh only
                bpy.data.objects[object.name].data.name = object.name
                named_meshes_count += 1
            elif not object.data.name in named_meshes:
                # object shares the mesh with others
                bpy.data.objects[object.name].data.name = object.name
                named_meshes_count += 1

                # add mesh to list so it doesn't get renamed again
                named_meshes.append(object.data.name)
                
        if named_meshes_count == 0:
            self.report({'INFO'}, "Renamed no meshes.")
        elif named_meshes_count == 1:
            self.report({'INFO'}, "Renamed 1 mesh.")
        else:
            self.report({'INFO'}, f"Renamed {named_meshes_count} meshes.")
        
        return {'FINISHED'}


def quick_mesh_rename_search(self, context):
    self.layout.operator(QuickMeshRename.bl_idname, icon="MESH_DATA")
    
def quick_mesh_rename_button(self, context):
    # handles icon with no text
    self.layout.operator(QuickMeshRename.bl_idname, icon="MESH_DATA", text="")

def register():
    bpy.utils.register_class(QuickMeshRename)
    bpy.types.VIEW3D_MT_object.append(quick_mesh_rename_search) # search
    bpy.types.OUTLINER_HT_header.append(quick_mesh_rename_button) # outliner button

def unregister():
    bpy.utils.unregister_class(QuickMeshRename)
    bpy.types.VIEW3D_MT_object.remove(quick_mesh_rename_search)
    bpy.types.OUTLINER_HT_header.remove(quick_mesh_rename_button)


# this allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
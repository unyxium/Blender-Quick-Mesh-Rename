# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Quick Mesh Rename",
    "author": "unyxium",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "Click the mesh icon in the outliner bar.",
    "description": "Rename all mesh data blocks with the name of their parent object.",
    "category": "Mesh",
    "doc_url": "https://github.com/unyxium/Blender-Quick-Mesh-Rename"
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
                
                if not bpy.data.objects[object.name].data.name == object.name:
                    bpy.data.objects[object.name].data.name = object.name
                    named_meshes_count += 1
            elif not object.data.name in named_meshes:
                # object shares the mesh with others
                
                if not bpy.data.objects[object.name].data.name == object.name:
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
bl_info = {
    "name": "Select border edges",
    "author": "dividi",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "EditMode>Select",
    "description": "Select the edges delimiting a selection",
    "warning": "",
    "doc_url": "",
    "category": "Select Edges",
}


import bpy
import bmesh
from bpy.props import BoolProperty


# select the specified edges
def select_edges(all_edges):
    

    # only selected edges
    selected_edges = []

    for e in all_edges:
        if e.select:
            selected_edges.append(e)
    
    

    ### get the border edges of the selected edges
    
        
    # check for each edge if the linked face is selected

    border_edges = []

    for e in selected_edges:
        
        # get the linked faces
        linked_faces = e.link_faces
        
        # border edge of the mesh
        if len(linked_faces) <= 1:
            border_edges.append(e)    
        
        elif linked_faces[0].select != linked_faces[1].select:
            border_edges.append(e)
    
    
    
    
    # deselect all        
    bpy.ops.mesh.select_all(action='DESELECT')

    # select only border edges
    for e in border_edges:
        e.select = True



# return the selected faces
def get_selected_faces (all_faces):
    
    # only selected edges
    selected_faces = []

    for e in all_faces:
        if e.select:
            selected_faces.append(e)
    
    return selected_faces









class MESH_OT_select_selection_border(bpy.types.Operator):
    """Select the edges delimiting a selection"""
    bl_idname = "mesh.select_selection_border"
    bl_label = "Select border"
    bl_options = {'REGISTER', 'UNDO'}


    hide_selection: BoolProperty(
        name="hide selection",
        default=False,
        description="hide the selection",
    )


    mark_seams: BoolProperty(
        name="mark seams",
        default=False,
        description="mark seams edge",
    )

    clear_seams: BoolProperty(
        name="clear seams",
        default=False,
        description="Clear old seams in selection",
    )



    @classmethod

    # limit the script to VIEW_3D
    def poll (cls, context):
        return context.area.type == 'VIEW_3D'


    # execute the script
    def execute(self, context):
        
        ### return all selected edges of a mesh
        ob = bpy.context.object

        # only on meshes
        if ob.type != 'MESH':
            raise TypeError("Active object is not a Mesh")
            return {'CANCELED'}

        me = ob.data

        if me.is_editmode:
            # Gain direct access to the mesh
            bm = bmesh.from_edit_mesh(me)
        else:
            # Create a bmesh from mesh
            # (won't affect mesh, unless explicitly written back)
            bm = bmesh.new()
            bm.from_mesh(me)
        

        # selected faces
        selected_faces = get_selected_faces(bm.faces)
            
        # all edges    
        all_edges = bm.edges



        # check selection        
        if len(all_edges) < 1:
            raise TypeError("Nothing selected")
            return {'CANCELED'}


        # clear old seams
        if self.clear_seams:
            bpy.ops.mesh.mark_seam(clear=True)
            
        # hide selected
        if self.hide_selection:
            for f in selected_faces:
                f.hide = True
        
        edges = select_edges(all_edges)
        
        # add seams
        if self.mark_seams:
            bpy.ops.mesh.mark_seam(clear=False)
            

        return {'FINISHED'}







# Registration

#def add_object_button(self, context):
#    self.layout.operator(
#        OBJECT_OT_add_object.bl_idname,
#        text="Add Object",
#        icon='PLUGIN')








def register():
    bpy.utils.register_class(MESH_OT_select_selection_border)

def unregister():
    bpy.utils.unregister_class(MESH_OT_select_selection_border)


if __name__ == "__main__":
    register()
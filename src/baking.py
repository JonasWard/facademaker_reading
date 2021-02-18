import rhinoscriptsyntax as rs
import scriptcontext as sc
import System.Guid
import Rhino.RhinoDoc
import time

DEFAULT_NAMES={
    "outline":"outline",
    "main_folds":"folds_main",
    "sec_folds":"folds_secondary",
    "inner_folds":"folds_inner",
}


def bake_objects(layer, geos, ghdoc):
    
    sc.doc=Rhino.RhinoDoc.ActiveDoc
    
    if not rs.IsLayer(layer):
        rs.AddLayer(layer)
    
    for geo_id in geos:
        try:
            sc.doc=ghdoc
            
            doc_object=rs.coercerhinoobject(geo_id)
            
            geometry=doc_object.Geometry
            attributes=doc_object.Attributes
            
            sc.doc=Rhino.RhinoDoc.ActiveDoc
            
            rhino_ref=sc.doc.Objects.Add(geometry)
                
            rs.ObjectLayer(rhino_ref, layer)
        except:
            print("failed to bake an object on layer {}".format(layer))
        
    sc.doc = ghdoc

def set_color(layer, color, ghdoc):
    sc.doc=Rhino.RhinoDoc.ActiveDoc
    
    if not rs.IsLayer(layer):
        rs.AddLayer(layer)

    rs.LayerColor(layer, color)

def bake(outline_crv, main_folds, secundary_folds, inner_folds, ghdoc, name_dict=None):
    if name_dict is None:
        global DEFAULT_NAMES
        name_dict=DEFAULT_NAMES
    
    bake_objects(name_dict["outline"], outline_crv, ghdoc)
    bake_objects(name_dict["main_folds"], main_folds, ghdoc)
    bake_objects(name_dict["sec_folds"], secundary_folds, ghdoc)
    bake_objects(name_dict["inner_folds"], inner_folds, ghdoc)
    
    time.sleep(.4)
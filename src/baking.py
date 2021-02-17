import rhinoscriptsyntax as rs
import scriptcontext as sc
import System.Guid
import Rhino.RhinoDoc
import time

def bake_objects(layer, geos, ghdoc):
    
    sc.doc=Rhino.RhinoDoc.ActiveDoc
    
    if not rs.IsLayer(layer):
        rs.AddLayer(layer)
    
    for geo_id in geos:
        
        sc.doc=ghdoc
        
        doc_object=rs.coercerhinoobject(geo_id)
        
        geometry=doc_object.Geometry
        attributes=doc_object.Attributes
        
        sc.doc=Rhino.RhinoDoc.ActiveDoc
        
        rhino_ref=sc.doc.Objects.Add(geometry)
            
        rs.ObjectLayer(rhino_ref, layer)
        
    sc.doc = ghdoc

def bake(outline_crv, main_folds, secundary_folds, inner_folds, ghdoc):
    bake_objects("outline", outline_crv, ghdoc)
    bake_objects("folds_main", main_folds, ghdoc)
    bake_objects("folds_secundary", secundary_folds, ghdoc)
    bake_objects("folds_inner", inner_folds, ghdoc)
    
    time.sleep(.4)
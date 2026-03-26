#!/usr/bin/env python3
import FreeCAD as App
import Part
import Mesh
import os, sys, traceback


def load_exports(export_dir):
    files = sorted([f for f in os.listdir(export_dir) if os.path.isfile(os.path.join(export_dir,f))])
    loaded = []
    for fname in files:
        path = os.path.join(export_dir, fname)
        ext = fname.lower().split('.')[-1]
        try:
            if ext in ('step','stp'):
                shape = Part.Shape()
                shape.read(path)
                obj = App.ActiveDocument.addObject("Part::Feature", fname.replace('.','_'))
                obj.Shape = shape
                loaded.append((fname,'part'))
            elif ext in ('stl','mesh'):
                m = Mesh.Mesh(path)
                mobj = App.ActiveDocument.addObject("Mesh::Feature", fname.replace('.','_'))
                mobj.Mesh = m
                loaded.append((fname,'mesh'))
            else:
                print('SKIP:'+fname)
        except Exception as e:
            print('ERROR_LOADING:'+fname+':'+str(e))
            traceback.print_exc()
    return loaded


def print_bboxes():
    for obj in App.ActiveDocument.Objects:
        try:
            if hasattr(obj,'Shape') and obj.Shape is not None:
                bb = obj.Shape.BoundBox
                print(f'BBOX {obj.Name} {bb.XMin:.3f} {bb.YMin:.3f} {bb.ZMin:.3f} {bb.XMax:.3f} {bb.YMax:.3f} {bb.ZMax:.3f}')
            elif hasattr(obj,'Mesh') and obj.Mesh is not None:
                bb = obj.Mesh.BoundBox
                print(f'MBBOX {obj.Name} {bb.XMin:.3f} {bb.YMin:.3f} {bb.ZMin:.3f} {bb.XMax:.3f} {bb.YMax:.3f} {bb.ZMax:.3f}')
            else:
                print('NO_BBOX ' + obj.Name)
        except Exception as e:
            print('BBOX_ERROR ' + obj.Name + ' ' + str(e))


def main():
    export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exports')
    if not os.path.isdir(export_dir):
        print('EXPORT_DIR_MISSING:'+export_dir)
        return
    doc_name = 'ValidationDoc'
    try:
        doc = App.getDocument(doc_name)
        for o in doc.Objects:
            doc.removeObject(o.Name)
    except Exception:
        doc = App.newDocument(doc_name)
    App.setActiveDocument(doc.Name)
    loaded = load_exports(export_dir)
    doc.recompute()

    print('LOADED_FILES:' + ','.join([name for name,_ in loaded]))
    print('OBJECT_COUNT:' + str(len(doc.Objects)))
    print_bboxes()
    # compute overall bounding box
    bbs = []
    for o in doc.Objects:
        try:
            if hasattr(o,'Shape') and o.Shape is not None:
                bbs.append(o.Shape.BoundBox)
            elif hasattr(o,'Mesh') and o.Mesh is not None:
                bbs.append(o.Mesh.BoundBox)
        except Exception:
            pass
    if bbs:
        Xmin = min(bb.XMin for bb in bbs)
        Ymin = min(bb.YMin for bb in bbs)
        Zmin = min(bb.ZMin for bb in bbs)
        Xmax = max(bb.XMax for bb in bbs)
        Ymax = max(bb.YMax for bb in bbs)
        Zmax = max(bb.ZMax for bb in bbs)
        print(f'ASSEMBLY_BBOX {Xmin:.3f} {Ymin:.3f} {Zmin:.3f} {Xmax:.3f} {Ymax:.3f} {Zmax:.3f}')
    else:
        print('NO_BBOXES_FOUND')

    # final recompute
    doc.recompute()

if __name__ == '__main__':
    main()

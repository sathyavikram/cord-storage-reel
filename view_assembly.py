import FreeCAD as App
import Part
import os

doc = App.ActiveDocument
if doc is None:
    doc = App.newDocument('Doc')

shape = Part.Shape()
shape.read('/Users/intelligentmachine/Documents/workspace/3d-models/cord-storage-reel-v3/exports/assembly.step')
feat = doc.addObject('Part::Feature', 'Assembly')
feat.Shape = shape

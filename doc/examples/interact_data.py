import numpy as np
from dipy.viz import actor, window, widget


# Change with Stanford data
dname = '/home/eleftherios/Data/Cunnane_Elef/08-111-609-AC15/work/'
import nibabel as nib
from nibabel import trackvis as tv

world_coords = False

img = nib.load(dname + 't1_brain_warp.nii.gz')
data = img.get_data()
affine = img.get_affine()


streams, hdr = tv.read(dname + 'results/bundles/cst.right.trk',
                       points_space="rasmm")
streamlines = [s[0] for s in streams]

streams, hdr = tv.read(dname + 'results/bundles/af.left.trk',
                       points_space="rasmm")
streamlines += [s[0] for s in streams]

streams, hdr = tv.read(dname + 'results/bundles/cc_1.trk',
                       points_space="rasmm")
streamlines += [s[0] for s in streams]

if not world_coords:
    from dipy.tracking.streamline import transform_streamlines
    streamlines = transform_streamlines(streamlines, np.linalg.inv(affine))

renderer = window.renderer()

# LOAD FA HERE
stream_actor = actor.line(streamlines, data)

if not world_coords:
    slicer = actor.butcher(data, affine=np.eye(4))
else:
    slicer = actor.butcher(data, affine)

window.add(renderer, stream_actor)
window.add(renderer, slicer)


def change_slice(obj, event):
    global slicer
    z = int(np.round(obj.GetSliderRepresentation().GetValue()))

    print(obj)
    print(event)
    print(z)
    slicer.SetDisplayExtent(0, 255, 0, 255, z, z)
    slicer.Update()

import vtk

ren_win = vtk.vtkRenderWindow()
ren_win.AddRenderer(renderer)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

slider = widget.slider(iren=iren, callback=change_slice)

iren.Initialize()

ren_win.Render()
iren.Start()


ren_win.RemoveRenderer(renderer)
renderer.SetRenderWindow(None)

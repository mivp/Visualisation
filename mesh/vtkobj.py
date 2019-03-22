#!/usr/bin/env python

import vtk
import sys

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " filepath")
    exit(1)

ColorBackground = [0.0, 0.0, 0.0]

reader = vtk.vtkOBJReader()

reader.SetFileName(sys.argv[1])

reader.Update()


mapper = vtk.vtkPolyDataMapper()

if vtk.VTK_MAJOR_VERSION <= 5:

     mapper.SetInput(reader.GetOutput())

else:

     mapper.SetInputConnection(reader.GetOutputPort())

actor = vtk.vtkActor()

actor.SetMapper(mapper)

# Create a rendering window and renderer

ren = vtk.vtkRenderer()

ren.SetBackground(ColorBackground)

renWin = vtk.vtkRenderWindow()

renWin.AddRenderer(ren)

# Create a renderwindowinteractor

iren = vtk.vtkRenderWindowInteractor()

iren.SetRenderWindow(renWin)

# Assign actor to the renderer

ren.AddActor(actor)

# Enable user interface interactor

iren.Initialize()

renWin.Render()

iren.Start()

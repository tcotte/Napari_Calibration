import cv2
import napari
from dock_widget import Form
import numpy as np

if __name__ == "__main__":
    img = cv2.cvtColor(cv2.imread("img/carre.png"), cv2.COLOR_BGR2RGB)
    viewer = napari.view_image(img)
    # viewer = napari.Viewer(img)

    shapes_layer = viewer.add_shapes(ndim=2, shape_type='line', edge_width=5, name="lines")

    viewer.window.add_dock_widget(Form(viewer), name="Form", area="right")
    napari.run()

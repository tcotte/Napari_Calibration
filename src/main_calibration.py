import cv2
import napari
from PyQt5.QtCore import Qt

from src.Image_widget import ImageForm
from src.Video.widget import LiveIDS
from src.dock_widget import Form
import numpy as np


def hide_layer_controls(viewer: napari.viewer, layer: str) -> None:
    """
    Hide almost all control widgets to add our own layer control
    :param viewer: Napari viewer
    :param layer: Name of the active layer
    """
    layout_layer = viewer.window.qt_viewer.controls.widgets[viewer.layers[layer]].grid_layout
    for i in range(1, layout_layer.count()):
        # We can erase all except the color swatch widget for edge_color
        layout_layer.itemAt(i).widget().setVisible(False)


def disable_circle_btn(viewer: napari.viewer, layer: str) -> None:
    layout_layer = viewer.window.qt_viewer.controls.widgets[viewer.layers[layer]].grid_layout
    button_grid = layout_layer.itemAt(0)
    add_circle_button = button_grid.itemAt(6).widget()
    add_circle_button.setEnabled(False)


def init_viewer():
    """
    Set up Napari's viewer
    """
    n_viewer = napari.Viewer(title='SGS - Visual_AI')
    # n_viewer.window._qt_window.setWindowIcon(QIcon(r"Logo/visual_ai.ico"))
    n_viewer.window._qt_window.setWindowState(Qt.WindowMaximized)
    n_viewer.window.qt_viewer.dockLayerList.setVisible(False)
    n_viewer.window.main_menu.setVisible(False)
    return n_viewer


if __name__ == "__main__":
    img = cv2.cvtColor(cv2.imread(r"C:\Users\tristan_cotte\PycharmProjects\calibration\img\Calibration_KFC.png"), cv2.COLOR_BGR2RGB)
    viewer = init_viewer()
    # viewer.add_image(img)
    # viewer = napari.Viewer(img)

    color = "#550000"
    shapes_layer = viewer.add_shapes(ndim=2, edge_color=color, face_color=color, shape_type='line', edge_width=10,
                                     name="lines")
    hide_layer_controls(viewer=viewer, layer="lines")
    disable_circle_btn(viewer=viewer, layer="lines")

    viewer.window.add_dock_widget(ImageForm(viewer), name="Image", area="left")

    viewer.window.add_dock_widget(Form(viewer), name="Form", area="right")
    napari.run()

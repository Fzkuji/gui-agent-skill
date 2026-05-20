"""Registered pre-learning tours per app.

A tour is a list of `{"state": ..., "setup": [...], "reset": [...]}` steps.
learn_app_components() looks up TOURS[app_name] automatically when the caller
doesn't pass an explicit tour.
"""

from gui_harness.planning.tours.gimp import GIMP_TOUR

TOURS: dict[str, list] = {
    "gimp": GIMP_TOUR,
}

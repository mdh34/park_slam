import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class AlgoGrid(Gtk.Grid):
    def __init__(self):
        super().__init__()
        self.set_row_spacing(5)
        self.set_column_spacing(20)
        self.title_label = Gtk.Label.new("Processing")

        algos = ["hdl_graph_slam", "slam_toolbox", "gmapping", "rtab-map"]
        self.algo_label = Gtk.Label.new("SLAM Algorithm:")
        self.algo_box = Gtk.ComboBoxText()
        # self.algoBox.set_entry_text_column(0)
        for item in algos:
            self.algo_box.append_text(item)

        self.attach(self.title_label, 0, 0, 1, 1)
        self.attach_next_to(self.algo_label, self.title_label,
                            Gtk.PositionType.BOTTOM, 1, 1)
        self.attach_next_to(self.algo_box, self.algo_label,
                            Gtk.PositionType.RIGHT, 1, 1)
        self.show_all()

    def get_algo(self):
        return self.algo_box.get_active_text()

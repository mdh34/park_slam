import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class ExtGrid(Gtk.Grid):
    def __init__(self):
        super().__init__()
        self.set_row_spacing(5)
        self.set_column_spacing(20)
        self.titleLabel = Gtk.Label.new("LiDAR Extrinsics")
        # unlikely to have lidar extrinsics > 10M
        self.x_adj = Gtk.Adjustment.new(0, -10, +10, 0.001, 0.01, 0)
        self.y_adj = Gtk.Adjustment.new(0, -10, +10, 0.001, 0.01, 0)
        self.z_adj = Gtk.Adjustment.new(0, -10, +10, 0.001, 0.01, 0)
        self.x_spin = Gtk.SpinButton.new(self.x_adj, 0.01, 3)
        self.y_spin = Gtk.SpinButton.new(self.y_adj, 0.01, 3)
        self.z_spin = Gtk.SpinButton.new(self.z_adj, 0.01, 3)
        self.x_label = Gtk.Label.new("X Offset")
        self.y_label = Gtk.Label.new("Y Offset")
        self.z_label = Gtk.Label.new("Z Offset")

        self.attach(self.titleLabel, 0, 0, 1, 1)
        self.attach_next_to(self.x_label, self.titleLabel,
                            Gtk.PositionType.BOTTOM, 1, 1)
        self.attach_next_to(self.y_label, self.x_label,
                            Gtk.PositionType.RIGHT, 1, 1)
        self.attach_next_to(self.z_label, self.y_label,
                            Gtk.PositionType.RIGHT, 1, 1)
        self.attach_next_to(self.x_spin, self.x_label,
                            Gtk.PositionType.BOTTOM, 1, 1)
        self.attach_next_to(self.y_spin, self.y_label,
                            Gtk.PositionType.BOTTOM, 1, 1)
        self.attach_next_to(self.z_spin, self.z_label,
                            Gtk.PositionType.BOTTOM, 1, 1)

    def get_ext(self):
        return (self.x_spin.get_value(), self.y_spin.get_value(), self.z_spin.get_value())

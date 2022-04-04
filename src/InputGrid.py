import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class InputGrid(Gtk.Grid):
    def __init__(self):
        super().__init__()
        self.set_row_spacing(5)
        self.set_column_spacing(20)
        self.ros_bag_path = ""
        self.input_type = ""
        title_label = Gtk.Label.new("Input")
        self.attach(title_label, 0, 0, 1, 1)
        self.lidar_btn = Gtk.RadioButton.new_with_label_from_widget(
            None, "Hesai LiDAR Sensor")
        self.lidar_btn.connect("toggled", self.on_input_toggled, "sensor")

        self.ros_bag_btn = Gtk.RadioButton.new_with_label_from_widget(
            self.lidar_btn, "ROS Bag Data")
        self.ros_bag_btn.connect("toggled", self.on_input_toggled, "rosbag")
        self.ros_bag_choose_btn = Gtk.Button.new_with_label(
            "Choose Input File")
        self.ros_bag_choose_btn.connect("clicked", self.on_ros_choose_clicked)
        self.ros_bag_choose_btn.set_sensitive(False)

        self.attach_next_to(self.lidar_btn, title_label,
                            Gtk.PositionType.BOTTOM, 1, 1)
        self.attach_next_to(self.ros_bag_btn, self.lidar_btn,
                            Gtk.PositionType.BOTTOM, 1, 1)
        self.attach_next_to(self.ros_bag_choose_btn,
                            self.ros_bag_btn, Gtk.PositionType.RIGHT, 1, 1)
        self.show_all()

    def on_ros_choose_clicked(self, button):
        dlg = Gtk.FileChooserDialog(
            title="Choose ROS Bag File", parent=None, action=Gtk.FileChooserAction.OPEN)
        dlg.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        dlg_filter = Gtk.FileFilter.new()
        dlg_filter.add_pattern("*.bag")
        dlg_filter.set_name("ROS Bag Files")
        dlg.add_filter(dlg_filter)

        response = dlg.run()
        if response == Gtk.ResponseType.OK:
            self.ros_bag_path = dlg.get_filename()

        dlg.destroy()

    def get_rosbag_path(self):
        return self.ros_bag_path

    def get_input_type(self):
        return self.input_type

    def on_input_toggled(self, button, name):
        if(name == "rosbag"):
            self.ros_bag_choose_btn.set_sensitive(button.get_active())

        if(button.get_active()):
            self.input_type = name

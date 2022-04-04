from RosInterface import RosInterface
from ExtGrid import ExtGrid
from OutputGrid import OutputGrid
from InputGrid import InputGrid
from AlgoGrid import AlgoGrid
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="ParkSLAM")
        self.ros_interface = RosInterface()
        self.main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.add(self.main_box)
        self.ext_sec = ExtGrid()
        self.main_box.pack_start(self.ext_sec, True, True, 0)
        self.main_box.pack_start(Gtk.Separator.new(
            Gtk.Orientation.HORIZONTAL), True, True, 0)

        self.input_sec = InputGrid()
        self.main_box.pack_start(self.input_sec, True, True, 0)
        self.main_box.pack_start(Gtk.Separator.new(
            Gtk.Orientation.HORIZONTAL), True, True, 0)

        self.algo_sec = AlgoGrid()
        self.main_box.pack_start(self.algo_sec, True, True, 0)
        self.main_box.pack_start(Gtk.Separator.new(
            Gtk.Orientation.HORIZONTAL), True, True, 0)

        self.output_sec = OutputGrid()
        self.main_box.pack_start(self.output_sec, True, True, 0)
        self.main_box.pack_start(Gtk.Separator.new(
            Gtk.Orientation.HORIZONTAL), True, True, 0)

        self.button_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        self.run_button = Gtk.Button.new_with_label("Run")
        self.run_button.connect("clicked", self.on_ros_run_clicked)
        self.save_button = Gtk.Button.new_with_label("Save")
        self.save_button.connect("clicked", self.on_save_clicked)
        self.stop_button = Gtk.Button.new_with_label("Stop")
        self.stop_button.connect("clicked", self.on_ros_stop_clicked)

        self.button_box.pack_start(self.run_button, True, True, 0)
        self.button_box.pack_start(self.save_button, True, True, 0)
        self.button_box.pack_start(self.stop_button, True, True, 0)
        self.main_box.pack_start(self.button_box, True, True, 0)
        self.set_default_icon_name("system-run")

    def on_ros_run_clicked(self, button):
        self.ros_interface.launch(self.algo_sec.get_algo(), self.input_sec.get_rosbag_path(),
                                  self.input_sec.get_input_type(), self.ext_sec.get_ext())

    def on_ros_stop_clicked(self, button):
        self.ros_interface.stop()

    def on_save_clicked(self, button):
        success = True
        algo = self.algo_sec.get_algo()

        if(algo == "gmapping" or algo == "hdl_graph_slam" or algo == "slam_toolbox" or algo =="rtab-map"):
            success = self.ros_interface.hector_traj_to_csv(
                self.output_sec.get_out_path())

        if(algo == "gmapping" or algo == "slam_toolbox"):
            map_success = self.ros_interface.map_saver(
                self.output_sec.get_out_path())
            success = success and map_success
        elif(algo == "hdl_graph_slam"):
            map_success = self.ros_interface.hdl_graph_save(
                self.output_sec.get_out_path())
            success = success and map_success
        elif(algo == "rtab-map"):
            self.ros_interface.save_latest_pcd(self.output_sec.get_out_path())

        if(success):
            dump_diag = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Poses/Map Successfully Saved"
            )
            dump_diag.run()
            dump_diag.destroy()
        else:
            dump_diag = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Error Occured While Trying To Save Poses/Map"
            )
            dump_diag.run()
            dump_diag.destroy()

if __name__ == '__main__':
    win = MainWindow()
    win.show_all()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()

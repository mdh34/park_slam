import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class OutputGrid(Gtk.Grid):
    def __init__(self):
        super().__init__()
        self.set_row_spacing(5)
        self.set_column_spacing(20)
        self.out_path = ""
        title_label = Gtk.Label.new("Output")
        self.attach(title_label, 0, 0, 1, 1)
        self.out_choose_btn = Gtk.Button.new_with_label("Choose Output Folder")
        self.out_choose_btn.connect("clicked", self.on_out_choose_clicked)
        self.attach_next_to(self.out_choose_btn, title_label,
                            Gtk.PositionType.BOTTOM, 1, 1)
        self.show_all()

    def on_out_choose_clicked(self, button):
        dlg = Gtk.FileChooserDialog(
            title="Choose Output Folder", parent=None, action=Gtk.FileChooserAction.SELECT_FOLDER)
        dlg.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        response = dlg.run()
        if response == Gtk.ResponseType.OK:
            self.out_path = dlg.get_filename()

        dlg.destroy()

    def get_out_path(self):
        return self.out_path

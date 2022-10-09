"""This plugin extends Gaphor with Laravel migrations export functionality."""

import logging
from gaphor import UML
from gi.repository import Gtk
from gaphor.core import action, gettext
from gaphor.abc import ActionProvider, Service

class ExportLaravelMigrations(Service, ActionProvider):
    def __init__(self, main_window, element_factory, file_manager, export_menu):
        # Set attributes
        self.main_window = main_window
        self.export_menu = export_menu
        self.file_manager = file_manager
        self.element_factory = element_factory
        self.logger = logging.getLogger(f'{__name__}:ExportLaravelMigrations')

        # Initialize plugin
        self.export_menu.add_actions(self)

    def shutdown(self):
        self.export_menu.remove_actions(self)

    @action(
        name='export-laravel-migrations',
        label=gettext('Export Laravel Migrations'),
        tooltip=gettext('Export model to Laravel Migrations.'),
    )
    def execute(self):
        dialog = Gtk.FileChooserNative.new(
            'Select Output Folder',
            self.main_window.window,
            Gtk.FileChooserAction.SELECT_FOLDER,
        )

        def response(_, answer):
            if answer == Gtk.ResponseType.ACCEPT:
                path: str = dialog.get_filename() if Gtk.get_major_version() == 3 else dialog.get_file().get_path()
                classes: list[UML.Class] = list(self.element_factory.select(lambda e: e.isKindOf(UML.Class)))
                enums: list[UML.Enumeration] = list(self.element_factory.select(lambda e: e.isKindOf(UML.Enumeration)))

                self.logger.info('Outputting Laravel migrations to: %s' % path)

                for e in enums:
                    self._generate_enum(e, path)

                for e in classes:
                    self._generate_class(e, path, enums)

            dialog.destroy()

        dialog.connect('response', response)

        dialog.set_modal(True)

        dialog.show()

    def _generate_enum(self, enum: UML.Enumeration, folder: str):
        self.logger.info(f'enum: {enum.name}')

    def _generate_class(self, cls: UML.Class, folder: str, enums: list[UML.Enumeration]):
        self.logger.info(f'class: {cls.name}')

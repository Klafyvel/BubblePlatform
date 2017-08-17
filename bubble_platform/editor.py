"""
This is the editor module. It provides a class to edit levels and campaigns.
"""
import os
import importlib

from slugify import slugify

from bubble_platform import settings
from bubble_platform.settings import logger
from bubble_platform import ui
from bubble_platform import campaign


class CampaignEditor(ui.VLayout):
    """
    A class to edit campaigns.
    """

    def __init__(self, *args, **kwargs):
        """
        The __init__ method.

        See the ui.VLayout documentation.

        :param path: path to the campaign.
        :param app: The application.
        """
        super(CampaignEditor, self).__init__(*args, **kwargs)

        self.campaign = campaign.Campaign(self.rc_manager, kwargs['path'])
        self.list_levels()
        self.editor = None
        self.app = kwargs['app']

    def on_new_level(self, name):
        file_content = ""

        with open(os.path.join(settings.APP_DIR, "level_template_header")) as f:
            file_content += f.read()

        file_content += '\nLEVEL_NAME = "{}"\n'.format(name)

        with open(os.path.join(settings.APP_DIR, "level_template_footer")) as f:
            file_content += f.read()

        slug = slugify(name)

        with open(os.path.join(self.campaign.path, 'level', slug+'.py'), "w") as f:
            f.write(file_content)

        with open(os.path.join(self.campaign.path, 'level', slug+'.map'), "w") as f:
            f.write((" "*4+'\n')*3+"0"*4+'\n')

        spec = importlib.util.spec_from_file_location(
            slug,
            os.path.join(self.campaign.path, 'level', slug+'.py')
        )
        self.campaign.levels[slug] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.campaign.levels[slug])
        self.list_levels()

    class on_edit_level:

        def __init__(self, camp, l):
            self.camp = camp
            self.l = l

        def __call__(self):
            level_editor = LevelEditor(
                rc_manager=self.camp.rc_manager,
                campaign=self.camp,
                level=self.camp.campaign.levels[self.l],
                app=self.camp.app
            )
            self.camp.app.main_widget = level_editor


    def list_levels(self):
        self.widgets = []
        for l in self.campaign.levels:
            self.add_widget(ui.Button(
                rc_manager=self.rc_manager,
                text=l,
                background=(250, 250, 250),
                callback=self.on_edit_level(self, l)
            ))
        self.add_widget(ui.Input(
            rc_manager=self.rc_manager,
            text="New level :",
            background=(250, 250, 250),
            callback=self.on_new_level
        ))
        self.add_widget(ui.Button(
            rc_manager=self.rc_manager,
            text="Back",
            background=(250, 250, 250),
            callback=self.on_quit,
        ))

    def on_render(self, dst):
        w, h = dst.get_size()
        super(CampaignEditor, self).on_render(dst, (0, 0, w, h))

    def on_quit(self):
        self.campaign.save()
        self.app.main_widget = self.app.main_menu


class LevelEditor(ui.VLayout):
    """
    A class to edit levels.
    """

    def __init__(self, *args, **kwargs):
        """
        The __init__ method.

        See the ui.VLayout documentation.

        :param campaign: The campaign editor the level belongs to.
        :param level: The level module.
        :param app: The application.
        """
        super(LevelEditor, self).__init__(*args, **kwargs)

        self.app = kwargs['app']
        self.text = ""
        self.background = (0, 0, 0)

        self.campaign = kwargs["campaign"]
        self.level = kwargs['level'].Level(self.campaign.rc_manager)

        self.main_bar = ui.HLayout(
            text="",
            rc_manager=self.rc_manager,
        )
        self.block_chooser = ui.VLayout(
            background=(0, 0, 0),
            text="Pick a block",
            rc_manager=self.rc_manager,
        )

        mainStyle = {
            'color': (255, 255, 255),
            'border': (255, 255, 255),
            'background': (0, 0, 0),
            'border_width': 5,
            'rc_manager': self.rc_manager,
        }

        self.main_bar.add_widget(ui.Button(
            text="Back",
            callback=self.on_quit,
            **mainStyle,
        ))
        self.main_bar.add_widget(ui.Button(
            text="Foreground",
            callback=self.on_foreground,
            **mainStyle,
        ))
        self.main_bar.add_widget(ui.Button(
            text="Middle",
            callback=self.on_middle,
            **mainStyle,
        ))
        self.main_bar.add_widget(ui.Button(
            text="Background",
            callback=self.on_background,
            **mainStyle,
        ))
        self.main_bar.add_widget(ui.Widget(
            text=self.level.name,
            **mainStyle,
        ))
        self.add_widget(self.main_bar)

    def on_render(self, dst):
        w, h = dst.get_size()
        super(LevelEditor, self).on_render(dst, (0, 0, w, h))

    def on_quit(self):
        self.campaign.list_levels()
        self.app.main_widget = self.campaign

    def on_foreground(self):
        pass

    def on_middle(self):
        pass

    def on_background(self):
        pass

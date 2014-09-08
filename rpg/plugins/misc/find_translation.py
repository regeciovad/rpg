from rpg.plugin import Plugin


class FindTranslationPlugin(Plugin):

    def find(self, project_dir, spec, sack):
        for item in list(project_dir.glob('**/*.mo')):
            spec.files.insert(0, "-f %{%s}.lang" % item.name())

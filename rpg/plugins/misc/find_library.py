from rpg.plugin import Plugin


class FindLibraryPlugin(Plugin):

    def installed(self, project_dir, spec, sack):
        self.libs = []  # List of pathes(relative) to libraries
        spec.scripts["postun/post"] = "-p /sbin/ldconfig"
        for item in list(project_dir.glob('**/*.so')):
            if item.name[:3] == 'lib':
                self.libs.append(item.relative_to(project_dir))

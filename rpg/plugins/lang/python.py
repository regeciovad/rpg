from rpg.plugin import Plugin
from modulefinder import ModuleFinder


class PythonPlugin(Plugin):

    def patched(self, project_dir, spec, sack):
            files = list(project_dir.glob('*.py'))
            files.extend(list(project_dir.glob('*/*.py')))

            mod = ModuleFinder()
            for item in files:
                mod.run_script(str(item))

            for name, mod in mod.modules.items():
                if mod.__file__:
                    # replace path:
                    # "/usr/lib/python3.*/" -> "%{python3_sitearch}/"
                    # "/usr/lib/python2.*/" -> "%{python_sitearch}/"
                    spec.Requires.append(mod.__file__)

            # TODO add to set instead of list
            # TODO proceed all *.py files and add to set:
            #   "from ([^\s.]) import" -> s.add(%{python3_sitearch}/\1)
            #   "import ([^\s.])" -> s.add(%{python3_sitearch}/\1)

import logging
from rpg.plugin import Plugin


class FilesToPkgsPlugin(Plugin):

    def installed(self, project_dir, spec, sack):
        """ Resolves files in (Build) requires into packages """
        def _resolve(files, query):
            for _file in files:
                try:
                    yield query.filter(file=_file)[0].name
                except IndexError:
                    logging.log(logging.WARN,
                                "For '{}' have not been found any package"
                                .format(_file))

        def _uniq(_list):
            return list(set(_list))

        _query = sack.query().available()
        logging.info("Resolving Requires")
        spec.Requires = _uniq(_resolve(spec.Requires, _query))
        logging.info("Resolving BuildRequires")
        spec.BuildRequires = _uniq(_resolve(spec.BuildRequires, _query))

from pathlib import Path
from unittest import mock, TestCase
from rpg.spec import Spec


class RpgTestCase(TestCase):
    test_project_dir = Path("tests/project")

    def assertExistInDir(self, expected, pathlibobject):
        path = Path(pathlibobject)
        for files in expected:
            self.assertTrue((path / files).exists(), msg=files)

    def assertRegexMatch(self, expected, files):
        output = {i: [r.pattern for r in expected if r.match(i)]
                  for i in set(files)}
        return output


class PluginTestCase(RpgTestCase):
    sack = mock.MagicMock()
    spec = Spec()

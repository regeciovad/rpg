from tests.support import RpgTestCase
from rpg import Base
import re


class FunctionalTest(RpgTestCase):

    def test_c_project(self):
        base = Base()
        base.load_plugins()
        base.load_project_from_url(
            self.test_project_dir / "hello_project/hello-1.4.tar.gz")
        base.spec.Name = "hello"
        base.spec.Version = "1.4"
        base.spec.Release = "1%{?dist}"
        base.spec.License = "GPLv2"
        base.spec.Summary = "Hello World test program"
        base.spec.description = "desc"
        base.spec.build = "make"
        base.run_extracted_source_analysis()
        base.run_patched_source_analysis()
        expected_required_files = {
            '/usr/include/bits/wordsize.h',
            '/usr/include/bits/typesizes.h',
            '/usr/include/bits/stdio_lim.h',
            '/usr/include/bits/sys_errlist.h',
            '/usr/include/features.h',
            '/usr/include/stdc-predef.h',
            '/usr/include/bits/types.h',
            '/usr/include/_G_config.h',
            '/usr/include/gnu/stubs.h',
            '/usr/include/wchar.h',
            '/usr/include/stdio.h',
            '/usr/include/sys/cdefs.h',
            '/usr/include/libio.h',
            '/usr/lib/gcc/[^/]*-redhat-linux/\d+.\d+.\d+./include/stddef.h',
            '/usr/include/gnu/stubs-64.h',
            '/usr/lib/gcc/[^/]*-redhat-linux/\d+.\d+.\d+./include/stdarg.h'
        }
        dirs = [
            "Makefile",
            "hello.c",
            "hello"
        ]
        base.run_installed_source_analysis()
        self.assertEqual(set(["make"]), base.spec.BuildRequires)
        ref_re = [re.compile(r) for r in expected_required_files]
        output = self.assertRegexMatch(ref_re, base.spec.required_files)
        self.assertEqual(len(output), len(expected_required_files))
        output = self.assertRegexMatch(ref_re, base.spec.build_required_files)
        self.assertEqual(len(output), len(expected_required_files))
        self.assertExistInDir(["Makefile", "hello.c"], base.extracted_dir)
        base.build_project()
        self.assertExistInDir(dirs, base.compiled_dir)
        base.run_compiled_source_analysis()
        base.install_project()
        base.run_installed_source_analysis()
        self.assertEqual(set([
            ("/hello", None, None),
            ("/__pycache__/", r"%exclude", None)
        ]), base.spec.files)
        base.build_srpm()
        self.assertTrue(base.srpm_path.exists())

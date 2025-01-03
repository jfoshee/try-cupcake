from conan import ConanFile, conan_version
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.files import copy

from functools import cached_property
import json
import pathlib

class TryCupcake(ConanFile):

    @cached_property
    def metadata(self):
        path = pathlib.Path(self.recipe_folder) / 'cupcake.json'
        with open(path, 'r') as file:
            return json.load(file)

    def set_name(self):
        if self.name is None:
            self.name = self.metadata['project']['name']

    def set_version(self):
        if self.version is None:
            self.version = self.metadata['project']['version']

    license = 'ISC'
    author = 'Jacob Foshee <jacobf@gmail.com>'

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'fPIC': [True, False]}
    default_options = {'shared': False, 'fPIC': True}

    generators = ['CMakeDeps', 'CMakeToolchain']

    exports_sources = [
        'CMakeLists.txt',
        'cupcake.json',
        'cmake/*',
        'external/*',
        'include/*',
        'src/*',
    ]

    def export(self):
        copy(self, 'cupcake.json', self.recipe_folder, self.export_folder)

    # For out-of-source build.
    # https://docs.conan.io/en/latest/reference/build_helpers/cmake.html#configure
    no_copy_source = True

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        # Available at https://conan.jfreeman.dev.
        # Must pass `test=True` and `build=False`.
        # https://github.com/conan-io/conan/issues/13036#issuecomment-2542553667
        self.requires('cupcake.cmake/1.2.1@github/thejohnfreeman', test=True)
        methods = {
            'tool': 'tool_requires',
            'test': 'test_requires',
        } if conan_version.major.value == 2 else {}
        for requirement in self.metadata.get('imports', []):
            groups = requirement.get('groups', [])
            group = groups[0] if len(groups) == 1 else 'main'
            method = methods.get(group, 'requires')
            getattr(self, method)(requirement['reference'])

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def build(self):
        cmake = CMake(self)
        cmake.configure(variables={'BUILD_TESTING': 'NO'})
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        path = f'{self.package_folder}/share/{self.name}/cpp_info.py'
        with open(path, 'r') as file:
            exec(file.read(), {}, {'self': self.cpp_info})

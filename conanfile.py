from conans import ConanFile, CMake, tools
import os


class CsvParserConan(ConanFile):
    name = "csv-parser"
    version = "1.2.2.1"
    description = "A modern C++ library for reading, writing, and analyzing CSV (and similar) files."
    # topics can get used for searches, GitHub topics, Bintray tags etc. Add here keywords about the library
    topics = ("conan", "csv-parser", "csv")
    url = "https://github.com/bincrafters/conan-csv-parser"
    homepage = "https://github.com/vincentlaucsb/csv-parser"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    exports = ["LICENSE.md"]      # Packages the license for the conanfile.py
    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = self.homepage
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version), sha256="b16a4a1a2f1674842e28cb9c866fdefd337fc7ccac03445aa7d83f79ddd8465c")
        extracted_dir = self.name + "-" + self.version

        # Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)

        cmake.definitions["CSV_CXX_STANDARD"] = 11
        if hasattr(self.settings.compiler, "cppstd"):
            if self.settings.compiler.cppstd in ["17", "gnu17", "20", "gnu20"]:
                cmake.definitions["CSV_CXX_STANDARD"] = 17

        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        if self.options.shared:
            tools.replace_in_file("{}/include/internal/CMakeLists.txt".format(self._source_subfolder), 'add_library(csv STATIC "")', 'add_library(csv SHARED "")')

        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)

        include_folder = os.path.join(self._source_subfolder, "include")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

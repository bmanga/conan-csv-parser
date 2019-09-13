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
    no_copy_source = True
    
    exports = ["LICENSE.md"]      # Packages the license for the conanfile.py
    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"

    def source(self):
        source_url = self.homepage
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version), sha256="b16a4a1a2f1674842e28cb9c866fdefd337fc7ccac03445aa7d83f79ddd8465c")
        extracted_dir = self.name + "-" + self.version

        # Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self._source_subfolder)

    def package(self):
        include_folder = os.path.join(self._source_subfolder, "include")
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*", dst="include", src=include_folder)

    def package_id(self):
        self.info.header_only()

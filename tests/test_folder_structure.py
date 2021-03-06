from unittest import TestCase
import os
from os.path import normpath
import shutil
from click.testing import CliRunner
from vcr import VCR
from icloudpd.base import main
from tests.helpers.print_result_exception import print_result_exception

vcr = VCR(decode_compressed_response=True)

class FolderStructureTestCase(TestCase):

    # This is basically a copy of the listing_recent_photos test #
    def test_default_folder_structure(self):
        ### Tests if the default directory structure is constructed correctly ###
        if os.path.exists("tests/fixtures/Photos"):
            shutil.rmtree("tests/fixtures/Photos")
        os.makedirs("tests/fixtures/Photos")

        # Note - This test uses the same cassette as test_download_photos.py
        with vcr.use_cassette("tests/vcr_cassettes/listing_photos.yml"):
            # Pass fixed client ID via environment variable
            os.environ["CLIENT_ID"] = "DE309E26-942E-11E8-92F5-14109FE0B321"
            runner = CliRunner()
            result = runner.invoke(
                main,
                [
                    "--username",
                    "jdoe@gmail.com",
                    "--password",
                    "password1",
                    "--recent",
                    "5",
                    "--only-print-filenames",
                    "--no-progress-bar",
                    "-d",
                    "tests/fixtures/Photos",
                ],
            )
            print_result_exception(result)
            filenames = result.output.splitlines()

            self.assertEqual(len(filenames), 8)
            self.assertEqual(
                normpath("tests/fixtures/Photos/2018/07/31/IMG_7409.JPG"), filenames[0]
            )
            self.assertEqual(
                normpath("tests/fixtures/Photos/2018/07/31/IMG_7409.MOV"), filenames[1]
            )
            self.assertEqual(
                normpath("tests/fixtures/Photos/2018/07/30/IMG_7408.JPG"), filenames[2]
            )
            self.assertEqual(
                normpath("tests/fixtures/Photos/2018/07/30/IMG_7408.MOV"), filenames[3]
            )
            self.assertEqual(
                normpath("tests/fixtures/Photos/2018/07/30/IMG_7407.JPG"), filenames[4]
            )
            self.assertEqual(
                normpath("tests/fixtures/Photos/2018/07/30/IMG_7407.MOV"), filenames[5]
            )
            self.assertEqual(
                normpath("tests/fixtures/Photos/2018/07/30/IMG_7405.MOV"), filenames[6]
            )
            self.assertEqual(
                normpath("tests/fixtures/Photos/2018/07/30/IMG_7404.MOV"), filenames[7]
            )

            assert result.exit_code == 0


    def test_folder_structure_none(self):
        if os.path.exists("tests/fixtures/Photos"):
            shutil.rmtree("tests/fixtures/Photos")
        os.makedirs("tests/fixtures/Photos")

        # Note - This test uses the same cassette as test_download_photos.py
        with vcr.use_cassette("tests/vcr_cassettes/listing_photos.yml"):
            # Pass fixed client ID via environment variable
            os.environ["CLIENT_ID"] = "DE309E26-942E-11E8-92F5-14109FE0B321"
            runner = CliRunner()
            result = runner.invoke(
                main,
                [
                    "--username",
                    "jdoe@gmail.com",
                    "--password",
                    "password1",
                    "--recent",
                    "5",
                    "--only-print-filenames",
                    "--folder-structure=none",
                    "--no-progress-bar",
                    "-d",
                    "tests/fixtures/Photos",
                ],
            )
            print_result_exception(result)
            filenames = result.output.splitlines()

            self.assertEqual(len(filenames), 8)
            self.assertEqual(
                normpath("tests/fixtures/Photos/IMG_7409.JPG"), filenames[0]
            )
            self.assertEqual(
                normpath("tests/fixtures/Photos/IMG_7409.MOV"), filenames[1]
            )
            self.assertEqual(
                normpath("tests/fixtures/Photos/IMG_7408.JPG"), filenames[2]
            )
            self.assertEqual(
                normpath("tests/fixtures/Photos/IMG_7408.MOV"), filenames[3]
            )
            self.assertEqual(
                normpath("tests/fixtures/Photos/IMG_7407.JPG"), filenames[4]
            )
            self.assertEqual(
                normpath("tests/fixtures/Photos/IMG_7407.MOV"), filenames[5]
            )
            self.assertEqual(
                normpath("tests/fixtures/Photos/IMG_7405.MOV"), filenames[6]
            )
            self.assertEqual(
                normpath("tests/fixtures/Photos/IMG_7404.MOV"), filenames[7]
            )

            assert result.exit_code == 0

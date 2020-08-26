import json
from collections import defaultdict
from enum import Enum
from pathlib import Path

from django.core.files.storage import DefaultStorage
from django.core.management import BaseCommand, CommandError, call_command
from django.test import RequestFactory
from django.utils.translation import ugettext as _

from terra_opp.models import Viewpoint
from terra_opp.point_utilities import update_point_properties


class FileState(Enum):
    NOT_PRESENT = -1
    EXISTING = 0
    UPLOADED = 1


class Command(BaseCommand):
    help = _('Import demo data from `demo.json` fixture. ')

    folder = 'project/fixtures'
    storage = DefaultStorage()

    def add_arguments(self, parser):
        parser.add_argument(
            '-m',
            '--media',
            action='store',
            default='localhost:8000',
            required=False,
            help=_(f'Media server url (default: localhost:8000)'),
        )
        parser.add_argument(
            '-i',
            '--image',
            action='store',
            default=self.folder + '/placeholder.jpg',
            required=False,
            help=_(f'A file name located in {self.folder} to be used as '
                   f'default image'),
        )

    def handle(self, *args, **options):
        """
        Main part of the demo import

        - upload images to bucket
        - load fixtures

        :param args:
        :param options:
        :return:
        """
        folder = Path(self.folder)
        default_image = Path(options['image'])
        if not default_image.exists():
            raise CommandError(f"Image {options['image']} does not exist")

        # Fixture import part
        if not (folder / 'demo.json').exists():
            raise CommandError(
                f"Fixture file {folder / 'demo.json'} does not exist, "
            )

        with open('%s/demo.json' % self.folder) as f:

            # Upload images to bucket
            self.upload_pictures(f, folder, default_image)

            # Import fixture
            self.stdout.write("Importing features...")
            call_command('loaddata', 'demo')

            # Update newly created viewpoints' points' properties
            for viewpoint in Viewpoint.objects.all():
                req = RequestFactory(SERVER_NAME=options['media']).request()
                update_point_properties(viewpoint, req)

    def upload_pictures(self, fixture, folder, default_image):
        """
        Upload images from fixture if they are present in folder (also uploads
        the default image)

        :param fixture: str
        :param folder: Path
        :param default_image: Path
        :return:
        """
        fixtures = json.load(fixture)
        images = set([i['fields']['file'] for i in fixtures
                      if i['model'] == 'terra_opp.picture'])
        states = defaultdict(int)
        self.stdout.write("Uploading images on bucket... (may take a while)")

        # Build a report
        states[self.save_image_on_bucket(folder, default_image.name)] += 1
        for image in images:
            states[self.save_image_on_bucket(folder, image)] += 1

        self.stdout.write(self.style.SUCCESS(
            f"{states[FileState.NOT_PRESENT]} missing\n"
            f"{states[FileState.UPLOADED]} uploaded\n"
            f"{states[FileState.EXISTING]} existing\n"
        ))

    def save_image_on_bucket(self, folder: Path, image: str):
        """
        Check on minio bucket if the file is present and upload it if needed

        :param folder:
        :param image:
        :return: FileState
        """
        if not self.storage.exists(image):
            # Locate it on the fie system
            image_path = folder / image
            if not image_path.exists():
                self.stdout.write(self.style.WARNING(
                    f"{image} not in {folder}"
                ))
                return FileState.NOT_PRESENT
            else:
                # Upload to minio bucket
                with image_path.open('rb') as fi:
                    self.storage.save(image, fi)
                return FileState.UPLOADED
        return FileState.EXISTING

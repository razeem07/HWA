import os
import boto3
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Migrate local uploads folder to AWS S3'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be uploaded without actually uploading',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        uploads_dir = Path(settings.BASE_DIR) / 'uploads'
        if not uploads_dir.exists():
            self.stderr.write(self.style.ERROR(f'Uploads directory not found: {uploads_dir}'))
            return

        bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
        region = os.environ.get('AWS_S3_REGION_NAME')
        access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

        if not all([bucket_name, region, access_key, secret_key]):
            self.stderr.write(self.style.ERROR('Missing AWS credentials in environment.'))
            return

        s3 = boto3.client(
            's3',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

        files = list(uploads_dir.rglob('*'))
        files = [f for f in files if f.is_file()]

        self.stdout.write(f'Found {len(files)} files in {uploads_dir}')
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN — nothing will be uploaded\n'))

        uploaded = 0
        skipped = 0
        failed = 0

        for local_path in files:
            relative = local_path.relative_to(Path(settings.BASE_DIR))
            s3_key = str(relative).replace('\\', '/')

            if dry_run:
                self.stdout.write(f'  Would upload: {s3_key}')
                uploaded += 1
                continue

            # Check if already exists in S3
            try:
                s3.head_object(Bucket=bucket_name, Key=s3_key)
                self.stdout.write(self.style.WARNING(f'  Skipped (exists): {s3_key}'))
                skipped += 1
                continue
            except s3.exceptions.ClientError:
                pass
            except Exception:
                pass

            try:
                content_type = self._guess_content_type(local_path.suffix)
                s3.upload_file(
                    str(local_path),
                    bucket_name,
                    s3_key,
                    ExtraArgs={'ContentType': content_type},
                )
                self.stdout.write(self.style.SUCCESS(f'  Uploaded: {s3_key}'))
                uploaded += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'  Failed: {s3_key} — {e}'))
                failed += 1

        self.stdout.write('\n--- Summary ---')
        if dry_run:
            self.stdout.write(f'Would upload: {uploaded} files')
        else:
            self.stdout.write(self.style.SUCCESS(f'Uploaded : {uploaded}'))
            self.stdout.write(self.style.WARNING(f'Skipped  : {skipped}'))
            if failed:
                self.stdout.write(self.style.ERROR(f'Failed   : {failed}'))

    def _guess_content_type(self, suffix):
        types = {
            '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
            '.png': 'image/png', '.gif': 'image/gif',
            '.webp': 'image/webp', '.svg': 'image/svg+xml',
            '.pdf': 'application/pdf',
        }
        return types.get(suffix.lower(), 'application/octet-stream')

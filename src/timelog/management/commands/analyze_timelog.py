from django.conf import settings
from django.core.management.base import BaseCommand
from timelog.lib import generate_table_from, analyze_log_file, PATTERN


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--noreverse',
            dest='reverse',
            action='store_false',
            default=True,
            help='Show paths instead of views')

    def handle(self, *args, **options):
        # --date-from YY-MM-DD
        #   specify a date filter start
        #   default to first date in file
        # --date-to YY-MM-DD
        #   specify a date filter end
        #   default to now

        LOGFILE = settings.TIMELOG_LOG

        try:
            data = analyze_log_file(LOGFILE, PATTERN, reverse_paths=options.get('reverse'))
        except IOError:
            print "File not found"
            exit(2)

        print generate_table_from(data)

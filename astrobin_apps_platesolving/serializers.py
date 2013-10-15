# restframework
from rest_framework import serializers

# This app
from astrobin_apps_platesolving.models import Solution


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        read_only_fields = (
            'status',
            'submission_id',
            'image_file',
            'objects_in_field',
            'ra',
            'dec',
            'pixscale',
            'orientation',
            'radius',
        )

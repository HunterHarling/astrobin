from django.db.models import Q

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import Authentication

from astrobin.models import Image, ImageRevision, ImageOfTheDay, App
from astrobin.models import SOLAR_SYSTEM_SUBJECT_CHOICES
from astrobin.templatetags.tags import gear_name


class AppAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        try:
            app_key = request.GET.get('api_key')
            app_secret = request.GET.get('api_secret')
        except:
            return False

        if app_key == '' or app_secret == '':
            return False

        try:
            app = App.objects.get(secret = app_secret, key = app_key)
        except App.DoesNotExist:
            return False

        return True


class ImageRevisionResource(ModelResource):
    image = fields.ForeignKey('astrobin.api.ImageResource', 'image')

    class Meta:
        authentication = AppAuthentication()
        queryset = ImageRevision.objects.filter(image__is_wip = False)
        fields = [
            'uploaded',
            'w',
            'h',
            'is_final',
            # TODO: filename somehow
            # TODO: solution
        ]
        allowed_methods = ['get']


class ImageResource(ModelResource):
    user = fields.CharField('user__username')
    revisions = fields.ToManyField(ImageRevisionResource, 'imagerevision_set')

    subjects = fields.ListField()

    imaging_telescopes = fields.ListField()
    imaging_cameras = fields.ListField()

    uploaded = fields.DateField('uploaded')
    updated = fields.DateField('updated')

    class Meta:
        authentication = AppAuthentication()
        queryset = Image.objects.filter(is_wip = False)
        fields = [
            'id',
            'title',
            # TODO: filename somehow

            'uploaded',
            'description',
            'h',
            'w',
            'animated',
            'link',
            'link_to_fits',
            'rating_score',
            'rating_votes',
            'license',

            'is_final',

            # TODO: solution
        ]
        allowed_methods = ['get']
        filtering = {
            'title': ALL,
            'description': ALL,
            # TODO: is_solved
            'user': ALL_WITH_RELATIONS,
            'uploaded': ALL,
            'fieldw': ALL,
            'fieldh': ALL,
            'fieldunits': ALL,
            'imaging_telescopes': ALL,
            'imaging_cameras': ALL,
        }
        ordering = ['rating_score', 'rating_votes', 'uploaded']

    def dehydrate_subjects(self, bundle):
        subjects = bundle.obj.subjects.all()
        ssms = bundle.obj.solar_system_main_subject

        ret = [x.mainId for x in subjects]

        if ssms:
            ret.append(SOLAR_SYSTEM_SUBJECT_CHOICES[ssms][1])

        return ret

    def dehydrate_imaging_telescopes(self, bundle):
        telescopes = bundle.obj.imaging_telescopes.all()
        return [gear_name(x) for x in telescopes]

    def dehydrate_imaging_cameras(self, bundle):
        cameras = bundle.obj.imaging_cameras.all()
        return [gear_name(x) for x in cameras]

    def build_filters(self, filters = None):
        if filters is None:
            filters = {}

        orm_filters = super(ImageResource, self).build_filters(filters)

        if 'subject' in filters:
            qs = Image.objects.filter(
                Q(subjects__mainId = filters['subject']) |
                Q(subjects__idlist__identifier = filters['subject']))
            orm_filters['pk__in'] = [i.pk for i in qs]

        return orm_filters


class ImageOfTheDayResource(ModelResource):
    class Meta:
        authentication = AppAuthentication()
        queryset = ImageOfTheDay.objects.all()
        fields = [
            'image',
            'filename',
            'date',
        ]

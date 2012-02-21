from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.datastructures import MultiValueDictKeyError

from haystack.forms import SearchForm
from haystack.query import SearchQuerySet, EmptySearchQuerySet
from haystack.query import SQ

from models import *

from search_indexes import xapian_escape

import string
import unicodedata
import operator

from management import NOTICE_TYPES

class ImageUploadForm(forms.Form):
    file = forms.ImageField()


class ImageEditPresolveForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('presolve_information',)
        widgets = {
            'presolve_information': forms.RadioSelect(choices = Image.SOLVE_CHOICES),
        }


class ImageEditBasicForm(forms.ModelForm):
    error_css_class = 'error'

    link = forms.RegexField(
        regex = '^(http|https)://',
        required = False,
        help_text = _("If you're hosting a copy of this image on your website, put the address here."),
        error_messages = {'invalid': "The address must start with http:// or https://."},
    )
    link_to_fits = forms.RegexField(
        regex = '^(http|https)://',
        required = False,
        help_text = _("If you want to share the TIFF or FITS file of your image, put a link to the file here. Unfortunately, AstroBin cannot offer to store these files at the moment, so you will have to host them on your personal space."),
        error_messages = {'invalid': "The address must start with http:// or https://."},
    )
    subjects = forms.CharField(
        required = False,
        help_text=_("If possible, use catalog names (e.g. M101, or NGC224 or IC1370)."),
    )

    def __init__(self, user=None, **kwargs):
        super(ImageEditBasicForm, self).__init__(**kwargs)
        self.fields['link'].label = _("Link")
        self.fields['link_to_fits'].label = _("Link to TIFF/FITS")
        self.fields['subjects'].label = _("Subjects")
        self.fields['locations'].label = _("Locations")

        profile = UserProfile.objects.get(user = user)
        locations = Location.objects.filter(user = profile)
        self.fields['locations'].queryset = locations
        self.fields['locations'].required = False

    def clean_link(self):
        return self.cleaned_data['link'].strip()

    def clean(self):
        skip_as = False
        try:
            subjects = self.data['as_values_subjects'].strip()
        except MultiValueDictKeyError:
            skip_as = True

        solar_system = self.cleaned_data['solar_system_main_subject']
        nojs_subjects = self.data['subjects'].strip()

        if solar_system is None and\
             (skip_as or (len(subjects) == 0 or (len(subjects) == 1 and subjects[0] in ('', ',')))) and\
             (len(nojs_subjects) == 0 or (len(nojs_subjects) == 1 and nojs_subjects[0] in ('', ','))):
            raise forms.ValidationError(_("Please enter either some subjects or a main solar system subject."));

        return self.cleaned_data

    class Meta:
        model = Image
        fields = ('title', 'link', 'link_to_fits', 'solar_system_main_subject', 'subjects', 'locations', 'description', 'allow_rating')


class ImageEditWatermarkForm(forms.ModelForm):
    error_css_class = 'error'

    watermark_opacity = forms.IntegerField(
        label = _("Opacity"),
        help_text = _("0 means invisible; 100 means completely opaque. Recommended values are: 10 if the watermark will appear on the dark sky background, 50 if on some bright object."),
        min_value = 0,
        max_value = 100,
    )

    def __init__(self, user=None, **kwargs):
        super(ImageEditWatermarkForm, self).__init__(**kwargs)

    def clean_watermark_text(self):
        data = self.cleaned_data['watermark_text']
        watermark = self.cleaned_data['watermark']

        if watermark and data == '':
            raise forms.ValidationError(_("If you want to watermark this image, you must specify some text."));

        return data.strip()

    class Meta:
        model = Image
        fields = ('watermark', 'watermark_text', 'watermark_position', 'watermark_opacity',)


class ImageEditGearForm(forms.ModelForm):
    def __init__(self, user=None, **kwargs):
        super(ImageEditGearForm, self).__init__(**kwargs)
        profile = UserProfile.objects.get(user=user)
        telescopes = profile.telescopes.all()
        self.fields['imaging_telescopes'].queryset = telescopes
        self.fields['guiding_telescopes'].queryset = telescopes
        cameras = profile.cameras.all()
        self.fields['imaging_cameras'].queryset = cameras
        self.fields['guiding_cameras'].queryset = cameras
        for attr in ('mounts',
                     'focal_reducers',
                     'software',
                     'filters',
                     'accessories',
                    ):
            self.fields[attr].queryset = getattr(profile, attr).all()

        self.fields['imaging_telescopes'].label = _("Imaging telescopes or lenses")
        self.fields['guiding_telescopes'].label = _("Guiding telescopes or lenses")
        self.fields['mounts'].label = _("Mounts")
        self.fields['imaging_cameras'].label = _("Imaging cameras")
        self.fields['guiding_cameras'].label = _("Guiding cameras")
        self.fields['focal_reducers'].label = _("Focal reducers")
        self.fields['software'].label = _("Software")
        self.fields['filters'].label = _("Filters")
        self.fields['accessories'].label = _("Accessories")

    class Meta:
        model = Image
        fields = ('imaging_telescopes',
                  'guiding_telescopes',
                  'mounts',
                  'imaging_cameras',
                  'guiding_cameras',
                  'focal_reducers',
                  'software',
                  'filters',
                  'accessories',
                 )


class UserProfileEditBasicForm(forms.ModelForm):
    error_css_class = 'error'

    website = forms.RegexField(
        regex = '^(http|https)://',
        required = False,
        help_text = _("If you have a personal website, put the address here."),
        error_messages = {'invalid': "The address must start with http:// or https://."},
    )

    class Meta:
        model = UserProfile
        fields = ('website', 'job', 'hobbies', 'timezone', 'about')

    def __init__(self, **kwargs):
        super(UserProfileEditBasicForm, self).__init__(**kwargs)
        self.fields['website'].label = _("Website")

            
class UserProfileEditGearForm(forms.Form):
    telescopes = forms.CharField(
        max_length=256,
        help_text=_("All the telescopes and lenses you own, including the ones you use for guiding, go here."),
        required=False)

    mounts = forms.CharField(
        max_length=256,
        required=False)

    cameras = forms.CharField(
        max_length=256,
        help_text=_("Your DSLRs, CCDs, planetary cameras and guiding cameras go here."),
        required=False)

    focal_reducers = forms.CharField(
        max_length=256,
        required=False)

    software = forms.CharField(
        max_length=256,
        required=False)

    filters = forms.CharField(
        max_length=256,
        help_text=_("Hint: enter your filters separately! If you enter, for instance, LRGB in one box, you won't be able to add separate acquisition sessions for them."),
        required=False)

    accessories = forms.CharField(
        max_length=256,
        required=False)

    def __init__(self, user=None, **kwargs):
        super(UserProfileEditGearForm, self).__init__(**kwargs)
        self.fields['telescopes'].label = _("Telescopes and lenses")
        self.fields['mounts'].label = _("Mounts")
        self.fields['cameras'].label = _("Cameras")
        self.fields['focal_reducers'].label = _("Focal reducers")
        self.fields['software'].label = _("Software")
        self.fields['filters'].label = _("Filters")
        self.fields['accessories'].label = _("Accessories")


class UserProfileEditPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('language',)

    def __init__(self, user=None, **kwargs):
        super(UserProfileEditPreferencesForm, self).__init__(**kwargs)
        for notice_type in NOTICE_TYPES:
            if notice_type[3] == 2:
                self.fields[notice_type[0]] = forms.BooleanField(
                    label=_(notice_type[1]),
                    required=False
                )


class PrivateMessageForm(forms.Form):
    subject = forms.CharField(max_length=255, required=False)
    body = forms.CharField(widget=forms.Textarea, max_length=4096, required=False)


class BringToAttentionForm(forms.Form):
    users = forms.CharField(max_length=64, required=False)

    def __init__(self, user=None, **kwargs):
        super(BringToAttentionForm, self).__init__(**kwargs)
        self.fields['users'].label = _("Users")


class ImageRevisionUploadForm(forms.Form):
    file = forms.ImageField()


class AdvancedSearchForm(SearchForm):
    solar_system_main_subject = forms.ChoiceField(
        required = False,
        choices = (('', '---------'),) + SOLAR_SYSTEM_SUBJECT_CHOICES,
    )

    imaging_telescopes = forms.CharField(
        required = False
    )
    imaging_cameras = forms.CharField(
        required = False
    )
    aperture_min = forms.IntegerField(
        required = False,
        help_text = _("Express value in mm"),
        min_value = 0,
    )
    aperture_max = forms.IntegerField(
        required = False,
        help_text = _("Express value in mm"),
        min_value = 0,
    )

    start_date = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={'class':'datepickerclass'}),
        help_text=_("Please use the following format: yyyy-mm-dd"))

    end_date = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={'class':'datepickerclass'}),
        help_text=_("Please use the following format: yyyy-mm-dd"))

    integration_min = forms.FloatField(
        required=False,
        help_text=_("Express value in hours"))

    integration_max = forms.FloatField(
        required=False,
        help_text=_("Express value in hours"))

    moon_phase_min = forms.FloatField(
        required=False,
        help_text="0-100")

    moon_phase_max = forms.FloatField(
        required=False,
        help_text="0-100")

    license = forms.MultipleChoiceField(
        required = False,
        label = _("License"),
        choices = LICENSE_CHOICES,
        initial = [x[0] for x in LICENSE_CHOICES],
    )

    def __init__(self, data=None, **kwargs):
        super(AdvancedSearchForm, self).__init__(data, **kwargs)
        self.fields['q'].help_text = _("Search for astronomical objects, telescopes or lenses, cameras, filters...")

        self.fields['solar_system_main_subject'].label = _("Main solar system subject")
        self.fields['imaging_telescopes'].label = _("Imaging telescopes or lenses")
        self.fields['imaging_cameras'].label = _("Imaging cameras")
        self.fields['aperture_min'].label = _("Min. telescope aperture")
        self.fields['aperture_max'].label = _("Max. telescope aperture")
        self.fields['start_date'].label = _("Acquired after")
        self.fields['end_date'].label = _("Acquired before")
        self.fields['integration_min'].label = _("Min. integration")
        self.fields['integration_max'].label = _("Max. integration")
        self.fields['moon_phase_min'].label = _("Min. Moon phase %")
        self.fields['moon_phase_max'].label = _("Max. Moon phase %")

    def search(self):
        sqs = EmptySearchQuerySet()

        if self.is_valid():
            q = xapian_escape(self.cleaned_data['q']).replace(' ', '')
            self.cleaned_data['q'] = q

            if self.cleaned_data['q'] == '':
                sqs = SearchQuerySet().all().models(Image)
                if self.load_all:
                    sqs = sqs.load_all()
            else:
                sqs = super(AdvancedSearchForm, self).search().models(Image)

            if self.cleaned_data['solar_system_main_subject']:
                sqs = sqs.filter(solar_system_main_subject = self.cleaned_data['solar_system_main_subject'])

            if self.cleaned_data['start_date']:
                sqs = sqs.filter(last_acquisition_date__gte=self.cleaned_data['start_date'])

            if self.cleaned_data['end_date']:
                sqs = sqs.filter(first_acquisition_date__lte=self.cleaned_data['end_date'])

            if self.cleaned_data['aperture_min'] is not None:
                sqs = sqs.filter(min_aperture__gte = self.cleaned_data['aperture_min'])

            if self.cleaned_data['aperture_max'] is not None:
                sqs = sqs.filter(max_aperture__lte = self.cleaned_data['aperture_max'])

            if self.cleaned_data['integration_min']:
                sqs = sqs.filter(integration__gte=int(self.cleaned_data['integration_min'] * 3600))

            if self.cleaned_data['integration_max']:
                sqs = sqs.filter(integration__lte=int(self.cleaned_data['integration_max'] * 3600))

            if self.cleaned_data['moon_phase_min']:
                sqs = sqs.filter(moon_phase__gte=self.cleaned_data['moon_phase_min'])

            if self.cleaned_data['moon_phase_max']:
                sqs = sqs.filter(moon_phase__lte=self.cleaned_data['moon_phase_max'])

            if self.cleaned_data['license']:
                filters = reduce(operator.or_, [SQ(**{'license': x}) for x in self.cleaned_data['license']])
                sqs = sqs.filter(filters)
            else:
                sqs = EmptySearchQuerySet()
                
        return sqs


class LocationEditForm(forms.ModelForm):
    error_css_class = 'error'

    lat_deg = forms.IntegerField(
        label = _("Latitude (degrees)"),
        help_text = "(0-90)",
        max_value = 90,
        min_value = 0)
    lat_min = forms.IntegerField(
        label = _("Latitude (minutes)"),
        help_text = "(0-60)",
        max_value = 60,
        min_value = 0,
        required = False)
    lat_sec = forms.IntegerField(
        label = _("Latitude (seconds)"),
        help_text = "(0-60)",
        max_value = 60,
        min_value = 0,
        required = False)

    lon_deg = forms.IntegerField(
        label = _("Longitude (degrees)"),
        help_text = "(0-180)",
        max_value = 180,
        min_value = 0)
    lon_min = forms.IntegerField(
        label = _("Longitude (minutes)"),
        help_text = "(0-60)",
        max_value = 60,
        min_value = 0,
        required = False)
    lon_sec = forms.IntegerField(
        label = _("Longitude (seconds)"),
        help_text = "(0-60)",
        max_value = 60,
        min_value = 0,
        required = False)

    def __init__(self, **kwargs):
        super(LocationEditForm, self).__init__(**kwargs)
        self.fields['country'].choices = sorted(COUNTRIES, key = lambda c: c[1])

    class Meta:
        model = Location


class SolarSystem_AcquisitionForm(forms.ModelForm):
    error_css_class = 'error'

    date = forms.DateField(
        required=False,
        input_formats = ['%Y-%m-%d'],
        widget=forms.TextInput(attrs={'class':'datepickerclass'}),
        help_text=_("Please use the following format: yyyy-mm-dd"),
        label = _("Date"),
    )

    def clean_seeing(self):
        data = self.cleaned_data['seeing']
        if data and data not in range(1, 5):
            raise forms.ValidationError(_("Please enter a value between 1 and 5."))

    def clean_transparency(self):
        data = self.cleaned_data['transparency']
        if data and data not in range(1, 10):
            raise forms.ValidationError(_("Please enter a value between 1 and 10."))

    class Meta:
        model = SolarSystem_Acquisition
        fields = (
            'date',
            'time',
            'frames',
            'fps',
            'focal_length',
            'cmi',
            'cmii',
            'cmiii',
            'seeing',
            'transparency',
        )
        widgets = {
            'date': forms.TextInput(attrs={'class': 'datepickerclass'}),
            'time': forms.TextInput(attrs={'class': 'timepickerclass'}),
        }


class DeepSky_AcquisitionForm(forms.ModelForm):
    error_css_class = 'error'

    date = forms.DateField(
        required=False,
        input_formats = ['%Y-%m-%d'],
        widget=forms.TextInput(attrs={'class':'datepickerclass'}),
        help_text=_("Please use the following format: yyyy-mm-dd"),
        label = _("Date"),
    )

    class Meta:
        model = DeepSky_Acquisition

    def __init__(self, user=None, **kwargs):
        queryset = None
        try:
            queryset = kwargs.pop('queryset')
        except KeyError:
            pass

        super(DeepSky_AcquisitionForm, self).__init__(**kwargs)
        if queryset:
            self.fields['filter'].queryset = queryset

    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(DeepSky_AcquisitionForm, self).save(commit=False)
        m.advanced = True
        if commit:
            m.save()
        return m


class DeepSky_AcquisitionBasicForm(forms.ModelForm):
    error_css_class = 'error'

    date = forms.DateField(
        required=False,
        input_formats = ['%Y-%m-%d'],
        widget=forms.TextInput(attrs={'class':'datepickerclass'}),
        help_text=_("Please use the following format: yyyy-mm-dd"),
        label = _("Date"),
    )

    class Meta:
        model = DeepSky_Acquisition
        fields = ('date', 'number', 'duration',)
        widgets = {
            'date': forms.TextInput(attrs={'class': 'datepickerclass'}),
        }


class DefaultImageLicenseForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('default_license',)


class ImageLicenseForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('license',)


class MultipleMessierForm(forms.Form):
    def __init__(self, objects=None, **kwargs):
        super(MultipleMessierForm, self).__init__(**kwargs)
        self.fields['messier_object'] = forms.ChoiceField(choices = [((x, 'M %s' % x)) for x in objects])
        self.fields['messier_object'].label = _("Nominate for")


class CommentForm(forms.ModelForm):
    error_css_class = 'error'

    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(attrs = {
                'rows': 4,
            })
        }


class TelescopeEditForm(forms.ModelForm):
    error_css_class = 'error'

    class Meta:
        model = Telescope
        exclude = ('name')


class MountEditForm(forms.ModelForm):
    error_css_class = 'error'

    class Meta:
        model = Mount
        exclude = ('name')


class CameraEditForm(forms.ModelForm):
    error_css_class = 'error'

    class Meta:
        model = Camera
        exclude = ('name')


class FocalReducerEditForm(forms.ModelForm):
    error_css_class = 'error'

    class Meta:
        model = FocalReducer
        exclude = ('name')


class SoftwareEditForm(forms.ModelForm):
    error_css_class = 'error'

    class Meta:
        model = Software
        exclude = ('name')


class FilterEditForm(forms.ModelForm):
    error_css_class = 'error'

    class Meta:
        model = Filter
        exclude = ('name')


class AccessoryEditForm(forms.ModelForm):
    error_css_class = 'error'

    class Meta:
        model = Accessory
        exclude = ('name')



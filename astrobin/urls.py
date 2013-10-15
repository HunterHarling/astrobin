from django.contrib.auth.decorators import login_required
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import redirect_to

from djangoratings.views import AddRatingFromModel
from hitcount.views import update_hit_count_ajax

from threaded_messages.views import search as messages_search
from threaded_messages.views import inbox as messages_inbox
from threaded_messages.views import outbox as messages_outbox
from threaded_messages.views import compose as messages_compose
from threaded_messages.views import view as messages_view
from threaded_messages.views import delete as messages_delete
from threaded_messages.views import undelete as messages_undelete
from threaded_messages.views import batch_update as messages_batch_update
from threaded_messages.views import trash as messages_trash
from threaded_messages.views import recipient_search as messages_recipient_search
from threaded_messages.views import message_ajax_reply as messages_message_ajax_reply

from threaded_messages.forms import ComposeForm as MessagesComposeForm

admin.autodiscover()

from astrobin import views
from astrobin import lookups
from astrobin.search import SearchView
from astrobin.forms import AdvancedSearchForm

from rawdata.views.helppages import (
    Help1 as RawDataHelp1,
    Help2 as RawDataHelp2,
    Help3 as RawDataHelp3,
)


from tastypie.api import Api
from astrobin.api import ImageResource, ImageRevisionResource,\
                         ImageOfTheDayResource

# These are the old API, not djangorestframework
v1_api = Api(api_name = 'v1')
v1_api.register(ImageResource())
v1_api.register(ImageRevisionResource())
v1_api.register(ImageOfTheDayResource())

urlpatterns = patterns('',
    url(r'^api/v2/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v2/api-auth-token/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^api/v2/nestedcomments/', include('nested_comments.api_urls')),
    url(r'^api/v2/common/', include('common.api_urls')),
    url(r'^api/v2/rawdata/', include('rawdata.api_urls')),
    url(r'^api/v2/platesolving/', include('astrobin_apps_platesolving.api_urls')),

    url(r'^rawdata/', include('rawdata.urls')),


    url(r'^$', views.index, name='index'),

    url(r'^(?P<id>\d+)/(?:(?P<r>\w+)/)?$', views.image_detail, name='image_detail'),
    url(r'^(?P<id>\d+)/(?:(?P<r>\w+)/)?thumb/(?P<alias>\w+)/(?:(?P<mod>\w+)/)?$', views.image_thumb, name='image_thumb'),
    url(r'^full/(?P<id>\d+)/(?:(?P<r>\w+)/)?$', views.image_full, name='image_full'),

    url(r'^upload/$', views.image_upload, name='image_upload'),
    url(r'^upload/process$', views.image_upload_process, name='image_upload_process'),
    url(r'^upload/revision/process/$', views.image_revision_upload_process, name='image_revision_upload_process'),
    url(r'^edit/presolve/(?P<id>\d+)/$', views.image_edit_presolve, name='image_edit_presolve'),
    url(r'^edit/basic/(?P<id>\d+)/$', views.image_edit_basic, name='image_edit_basic'),
    url(r'^edit/watermark/(?P<id>\d+)/$', views.image_edit_watermark, name='image_edit_watermark'),
    url(r'^edit/gear/(?P<id>\d+)/$', views.image_edit_gear, name='image_edit_gear'),
    url(r'^edit/acquisition/(?P<id>\d+)/$', views.image_edit_acquisition, name='image_edit_acquisition'),
    url(r'^edit/makefinal/(?P<id>\d+)/$', views.image_edit_make_final, name='image_edit_make_final'),
    url(r'^edit/revision/makefinal/(?P<id>\d+)/$', views.image_edit_revision_make_final, name='image_edit_revision_make_final'),
    url(r'^edit/license/(?P<id>\d+)/$', views.image_edit_license, name='image_edit_license'),
    url(r'^edit/acquisition/reset/(?P<id>\d+)/$', views.image_edit_acquisition_reset, name='image_edit_acquisition_reset'),
    url(r'^edit/save/basic/$', views.image_edit_save_basic, name='image_edit_save_basic'),
    url(r'^edit/save/watermark/$', views.image_edit_save_watermark, name='image_edit_save_watermark'),
    url(r'^edit/save/gear/$', views.image_edit_save_gear, name='image_edit_save_gear'),
    url(r'^edit/save/acquisition/$', views.image_edit_save_acquisition, name='image_edit_save_acquisition'),
    url(r'^edit/save/license/$', views.image_edit_save_license, name='image_edit_save_license'),
    url(r'^delete/(?P<id>\d+)/$', views.image_delete, name='image_delete'),
    url(r'^delete/revision/(?P<id>\d+)/$', views.image_delete_revision, name='image_delete_revision'),
    url(r'^delete/original/(?P<id>\d+)/$', views.image_delete_original, name='image_delete_original'),
    url(r'^promote/(?P<id>\d+)/$', views.image_promote, name='image_promote'),
    url(r'^demote/(?P<id>\d+)/$', views.image_demote, name='image_demote'),

    url(r'^search/', SearchView(form_class=AdvancedSearchForm), name='haystack_search'),

       (r'^accounts/', include('registration.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
       (r'^admin/', include(admin.site.urls)),
       (r'^sitestatic/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^profile/edit/$', views.user_profile_edit_basic, name='profile_edit_basic'),
    url(r'^profile/edit/basic/$', views.user_profile_edit_basic, name='profile_edit_basic'),
    url(r'^profile/save/basic/$', views.user_profile_save_basic, name='profile_save_basic'),
    url(r'^profile/edit/commercial/$', views.user_profile_edit_commercial, name='profile_edit_commercial'),
    url(r'^profile/edit/retailer/$', views.user_profile_edit_retailer, name='profile_edit_retailer'),
    url(r'^profile/edit/gear/$', views.user_profile_edit_gear, name='profile_edit_gear'),
    url(r'^profile/edit/gear/remove/(?P<id>\d+)/$', views.user_profile_edit_gear_remove, name='profile_edit_gear_remove'),
    url(r'^profile/save/gear/$', views.user_profile_save_gear, name='profile_save_gear'),
    url(r'^profile/edit/locations/$', views.user_profile_edit_locations, name='profile_edit_locations'),
    url(r'^profile/save/locations/$', views.user_profile_save_locations, name='profile_save_locations'),
    url(r'^profile/edit/license/$', views.user_profile_edit_license, name='profile_edit_license'),
    url(r'^profile/save/license/$', views.user_profile_save_license, name='profile_save_license'),
    url(r'^profile/edit/flickr/$', views.user_profile_flickr_import, name='profile_flickr_import'),
    url(r'^profile/seen/realname/$', views.user_profile_seen_realname, name='profile_seen_realname'),
    url(r'^flickr_auth_callback/$', views.flickr_auth_callback, name='flickr_auth_callback'),
    url(r'^profile/edit/preferences/$', views.user_profile_edit_preferences, name='profile_edit_preferences'),
    url(r'^profile/save/preferences/$', views.user_profile_save_preferences, name='profile_save_preferences'),
    url(r'^autocomplete/(?P<what>\w+)/$', lookups.autocomplete, name='autocomplete'),
    url(r'^autocomplete_user/(?P<what>\w+)/$', lookups.autocomplete_user, name='autocomplete_user'),
    url(r'^autocomplete_usernames/$', lookups.autocomplete_usernames, name='autocomplete_usernames'),
    url(r'rate/(?P<object_id>\d+)/(?P<score>\d+)/', AddRatingFromModel(), {
            'app_label': 'astrobin',
            'model': 'image',
            'field_name': 'rating',}, name='image_rate'),
    url(r'get_rating/(?P<image_id>\d+)/', views.image_get_rating, name='image_get_rating'),

    url(r'^me/$', views.me, name='me'),
    url(r'^users/(?P<username>[\w.@+-]+)/$', views.user_page, name='user_page'),

    url(r'^users/(?P<username>[\w.@+-]+)/commercial/products/$', views.user_page_commercial_products, name='user_page_commercial_products'),

    url(r'^commercial/products/claim/(?P<id>\d+)/$', views.commercial_products_claim, name='commercial_products_claim'),
    url(r'^commercial/products/unclaim/(?P<id>\d+)/$', views.commercial_products_unclaim, name='commercial_products_unclaim'),
    url(r'^commercial/products/merge/(?P<from_id>\d+)/(?P<to_id>\d+)/$', views.commercial_products_merge, name='commercial_products_merge'),
    url(r'^commercial/products/edit/(?P<id>\d+)/$', views.commercial_products_edit, name='commercial_products_edit'),
    url(r'^commercial/products/save/(?P<id>\d+)/$', views.commercial_products_save, name='commercial_products_save'),

    url(r'^commercial/products/retailed/claim/(?P<id>\d+)/$', views.retailed_products_claim, name='retailed_products_claim'),
    url(r'^commercial/products/retailed/unclaim/(?P<id>\d+)/$', views.retailed_products_unclaim, name='retailed_products_unclaim'),
    url(r'^commercial/products/retailed/merge/(?P<from_id>\d+)/(?P<to_id>\d+)/$', views.retailed_products_merge, name='retailedgg_products_merge'),
    url(r'^commercial/products/retailed/edit/(?P<id>\d+)/$', views.retailed_products_edit, name='retailed_products_edit'),

    url(r'^users/(?P<username>[\w.@+-]+)/favorites/$', views.user_page_favorites, name='user_page_favorites'),
    url(r'^users/(?P<username>[\w.@+-]+)/plots/$', views.user_page_plots, name='user_page_plots'),
    url(r'^users/(?P<username>[\w.@+-]+)/apikeys/$', views.user_page_api_keys, name='user_page_api_keys'),
    url(r'^users/(?P<username>[\w.@+-]+)/votes$', views.user_page_votes, name='user_page_votes'),
    url(r'^users/(?P<username>[\w.@+-]+)/stats/integration_hours/(?P<period>\w+)/(?P<since>\d+)/$',
        views.user_profile_stats_get_integration_hours_ajax,
        name = 'stats_integration_hours'),
    url(r'^users/(?P<username>[\w.@+-]+)/stats/integration_hours_by_gear/(?P<period>\w+)/$',
        views.user_profile_stats_get_integration_hours_by_gear_ajax,
        name = 'stats_integration_hours_by_gear'),
    url(r'^users/(?P<username>[\w.@+-]+)/stats/uploaded_images/(?P<period>\w+)/$',
        views.user_profile_stats_get_uploaded_images_ajax,
        name = 'stats_uploaded_images'),
    url(r'^users/(?P<username>[\w.@+-]+)/stats/views/(?P<period>\w+)/$',
        views.user_profile_stats_get_views_ajax,
        name = 'stats_views'),
    url(r'^(?P<id>\d+)/stats/views/(?P<period>\w+)/$',
        views.stats_get_image_views_ajax,
        name = 'stats_image_views'),

    url(r'^gear/(?P<id>\d+)/stats/views/$',
        views.stats_get_gear_views_ajax,
        name = 'stats_gear_views'),

    url(r'^gear/stats/affiliated/(?P<username>[\w.@+-]+)/views/(?P<period>\w+)/$',
        views.stats_get_affiliated_gear_views_ajax,
        name = 'stats_affiliated_gear_views'),

     url(r'^stats/camera-types-trend/$',
        views.stats_camera_types_trend_ajax,
        name = 'stats_camera_types_trend'),
     url(r'^stats/telescope-types-trend/$',
        views.stats_telescope_types_trend_ajax,
        name = 'stats_telescope_types_trend'),
     url(r'^stats/subject-type-trend/$',
        views.stats_subject_type_trend_ajax,
        name = 'stats_subject_type_trend'),

    url(r'^subject/stats/images-monthly/(?P<id>\d+)/$',
        views.stats_subject_images_monthly_ajax,
        name = 'stats_subject_images_monthly'),
     url(r'^subject/stats/integration-monthly/(?P<id>\d+)/$',
        views.stats_subject_integration_monthly_ajax,
        name = 'stats_subject_integration_monthly'),
     url(r'^subject/stats/total-images/(?P<id>\d+)/$',
        views.stats_subject_total_images_ajax,
        name = 'stats_subject_total_images'),
     url(r'^subject/stats/camera-types/(?P<id>\d+)/$',
        views.stats_subject_camera_types_ajax,
        name = 'stats_subject_camera_types'),
     url(r'^subject/stats/telescope-types/(?P<id>\d+)/$',
        views.stats_subject_telescope_types_ajax,
        name = 'stats_subject_telescope_types'),

      url(r'^gear/stats/total-images/(?P<id>\d+)/$',
        views.stats_gear_total_images_ajax,
        name = 'stats_gear_total_images'),

    url(r'^follow/(?P<username>[\w.@+-]+)/$', views.follow, name='follow'),
    url(r'^unfollow/(?P<username>[\w.@+-]+)/$', views.unfollow, name='unfollow'),
    url(r'^follow_gear/(?P<id>\d+)/$', views.follow_gear, name='follow_gear'),
    url(r'^unfollow_gear/(?P<id>\d+)/$', views.unfollow_gear, name='unfollow_gear'),
    url(r'^follow_subject/(?P<id>\d+)/$', views.follow_subject, name='follow_subject'),
    url(r'^unfollow_subject/(?P<id>\d+)/$', views.unfollow_subject, name='unfollow_subject'),

       (r'^notices/', include('notification.urls')),
    url(r'^push_notification/$', views.push_notification, name='push_notification'),
    url(r'^notifications/seen/$', views.mark_notifications_seen, name='mark_notification_seen'),
    url(r'^notifications/$', views.notifications, name='notifications'),

    url(r'^messages/inbox/$', messages_inbox, {'template_name': 'messages/inbox.html'}, name='messages_inbox'),
    url(r'^messages/compose/$', messages_compose, {'template_name': 'messages/compose.html'}, name='messages_compose'),
    url(r'^messages/compose/(?P<recipient>[\w.@+-]+)/$', messages_compose, {'template_name': 'messages/compose.html'}, name='messages_compose_to'),
    url(r'^messages/view/(?P<thread_id>[\d]+)/$', messages_view, {'template_name': 'messages/view.html'}, name='messages_detail'),
    url(r'^messages/delete/(?P<thread_id>[\d]+)/$', messages_delete, name='messages_delete'),
    url(r'^messages/batch-update/$', messages_batch_update, name='messages_batch_update'),
    url(r"^messages/recipient-search/$", messages_recipient_search, name="recipient_search"),
    url(r'^messages/message-reply/(?P<thread_id>[\d]+)/$', messages_message_ajax_reply, {'template_name': 'messages/message_list_view.html'}, name="message_reply"),
    # modal composing
    url(r'^messages/modal-compose/(?P<recipient>[\w.@+-]+)/$', messages_compose, {
                            "template_name":"messages/modal_compose.html",
                            "form_class": MessagesComposeForm
                        }, name='modal_messages_compose_to'),
    url(r'^messages/modal-compose/$', messages_compose, {
                            "template_name":"messages/modal_compose.html",
                            "form_class": MessagesComposeForm
                        }, name='modal_messages_compose'),

    url(r'^send_private_message/$', views.send_private_message, name='send_private_message'),

    url(r'^(?P<id>\d+)/bring-to-attention/$', views.bring_to_attention, name='bring_to_attention'),
    url(r'^bring-to-attention/process/$', views.bring_to_attention_process, name='bring_to_attention_process'),
    url(r'^(?P<id>\d+)/bring-to-attention/complete/$', views.bring_to_attention_complete, name='bring_to_attention_complete'),

    url(r'^stats/', views.stats, name='stats'),
    url(r'^leaderboard/', views.leaderboard, name='leaderboard'),
    url(r'^help/$', views.help, name='help'),
    url(r'^help/api/$', views.api, name='api'),
    url(r'^faq/', views.faq, name='faq'),
    url(r'^help/questions/$', views.help_questions, name='help_questions'),
    url(r'^help/rawdata/1/$', RawDataHelp1.as_view(), name='rawdata.help1'),
    url(r'^help/rawdata/2/$', RawDataHelp2.as_view(), name='rawdata.help2'),
    url(r'^help/rawdata/3/$', RawDataHelp3.as_view(), name='rawdata.help3'),
    url(r'^affiliates/$', views.affiliates, name='affiliates'),
    url(r'^tos/', views.tos, name='tos'),
    url(r'^guidelines/', views.guidelines, name='guidelines'),
    url(r'^language/set/(?P<lang>[\w-]+)/$', views.set_language, name='set_language'),

    url(r'^blog/', include('zinnia.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^tinymce/', include('tinymce.urls')),

    url(r'^explore/choose/$', views.expore_choose, name='explore_choose'),
    url(r'^explore/wall/$', views.wall, name='wall'),
    url(r'^explore/iotd/$', views.iotd_archive, name='iotd_archive'),
    url(r'^explore/messier/$', views.messier, name='messier'),
    url(r'^explore/messier/nominate/(?P<id>\d+)/$', views.messier_nomination, name='messier_nomination'),
    url(r'^explore/messier/nominate/process/$', views.messier_nomination_process, name='messier_nomination_process'),
    url(r'^explore/fits/$', views.fits, name='fits'),

    url(r'^hitcount/$', update_hit_count_ajax, name='hitcount_update_ajax'),

    url(r'^get_edit_gear_form/(?P<id>\d+)/$', views.get_edit_gear_form, name='get_edit_gear_form'),
    url(r'^get_empty_edit_gear_form/(?P<gear_type>\w+)/$', views.get_empty_edit_gear_form, name='get_empty_edit_gear_form'),
    url(r'^save_gear_details/$', views.save_gear_details, name='save_gear_details'),
    url(r'^get_is_gear_complete/(?P<id>\d+)/$', views.get_is_gear_complete, name='get_is_gear_complete'),

    url(r'^get_gear_user_info_form/(?P<id>\d+)/$', views.get_gear_user_info_form, name='get_gear_user_info_form'),
    url(r'^save_gear_user_info/$', views.save_gear_user_info, name='save_gear_user_info'),

    url(r'^favorite_ajax/(?P<id>\d+)/$', views.favorite_ajax, name='favorite_ajax'),

    url(r'^gear_popover_ajax/(?P<id>\d+)/$', views.gear_popover_ajax, name='gear_popover_ajax'),
    url(r'^subject_popover_ajax/(?P<id>\d+)/$', views.subject_popover_ajax, name='subject_popover_ajax'),
    url(r'^user_popover_ajax/(?P<username>[\w.@+-]+)/$', views.user_popover_ajax, name='user_popover_ajax'),

    url(r'^subject/(?P<id>\d+)/$', views.subject_page, name='subject_page'),

    url(r'^gear/(?P<id>\d+)/(?:(?P<slug>[a-z0-9-_]+)/)?$', views.gear_page, name='gear_page'),
    url(r'^gear/fix/(?P<id>\d+)/$', views.gear_fix, name='gear_fix'),
    url(r'^gear/fix/save/$', views.gear_fix_save, name='gear_fix_save'),
    url(r'^gear/fix/thanks/$', views.gear_fix_thanks, name='gear_fix_thanks'),
    url(r'^gear/review/save/$', views.gear_review_save, name='gear_review_save'),
    url(r'^gear/by-image/(?P<image_id>\d+)/$', views.gear_by_image, name='gear_by_image'),
    url(r'^gear/by-make/(?P<make>[(\w|\W).+-]*)/$', views.gear_by_make, name='gear_by_make'),
    url(r'^gear/by-ids/(?P<ids>([0-9]+,?)+)/$', views.gear_by_ids, name='gear_by_ids'),

    url(r'^contact/', include("contact_form.urls", namespace="contact_form")),
    url(r'^avatar/', include('avatar.urls')),

    url(r'^get-makes-by-type/(?P<klass>\w+)/$', views.get_makes_by_type, name='get_makes_by_type'),

    url(r'^api/', include(v1_api.urls)),
    url(r'^api/request-key/$', views.app_api_key_request, name = 'app_api_key_request'),
    url(r'^api/request-key/process/$', views.app_api_key_request_process, name = 'app_api_key_request_process'),
    url(r'^api/request-key/complete/$', views.app_api_key_request_complete, name = 'app_api_key_request_complete'),

    url('^activity/', include('actstream.urls')),
    url('^activities/$', views.activities, name = 'activities'),

    url(r'^openid/', include('openid_provider.urls')),
    url(r'^subscriptions/', include('subscription.urls')),
)


/*
 * All of AstroBin's javascript and jQuery code.
 */

/**********************************************************************
 * Common
 *********************************************************************/
astrobin_common = {
    config: {
        image_detail_url           : '/',

        /* Notifications */
        notifications_base_url     : '/activity?id=notification_',
        notifications_element_empty: 'ul#notification-feed li#empty',
        notifications_element_image: 'img#notifications',
        notifications_element_ul   : 'ul#notification-feed'
    },

    globals: {
        requests: [],
        smart_ajax: $.ajax,
        current_username: ''
    },

    utils: {
       getParameterByName: function(name) {
           name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
           var regexS = "[\\?&]" + name + "=([^&#]*)";
           var regex = new RegExp(regexS);
           var results = regex.exec(window.location.search);
           if(results == null)
               return "";
           else
               return decodeURIComponent(results[1].replace(/\+/g, " "));
       },
       checkParameterExists: function(parameter) {
           //Get Query String from url
           fullQString = window.location.search.substring(1);

           paramCount = 0;
           queryStringComplete = "?";

           if(fullQString.length > 0)
           {
               //Split Query String into separate parameters
               paramArray = fullQString.split("&");

               //Loop through params, check if parameter exists.
               for (i=0;i<paramArray.length;i++)
               {
                   currentParameter = paramArray[i].split("=");
                   if(currentParameter[0] == parameter) //Parameter already exists in current url
                   {
                       return true;
                   }
               }
           }

           return false;
       }
    },

    listen_for_notifications: function(username, last_modified, etag) {
        astrobin_common.globals.smart_ajax({
            'beforeSend': function(xhr) {
                xhr.setRequestHeader("If-None-Match", etag);
                xhr.setRequestHeader("If-Modified-Since", last_modified);
            },
            url: astrobin_common.config.notifications_base_url + username,
            dataType: 'text',
            type: 'get',
            cache: 'false',
            success: function(data, textStatus, xhr) {
                etag = xhr.getResponseHeader('Etag');
                last_modified = xhr.getResponseHeader('Last-Modified');

                json = jQuery.parseJSON(data);

                $(astrobin_common.config.notifications_element_empty).remove();
                $(astrobin_common.config.notifications_element_ul)
                    .prepend('<li class="unread">'+json['message']+'</li>');

                /* Start the next long poll. */
                astrobin_common.listen_for_notifications(username, last_modified, etag);
            }
        });
    },

    start_listeners: function(username) {
        astrobin_common.globals.smart_ajax = function(settings) {
            // override complete() operation
            var complete = settings.complete;
            settings.complete = function(xhr) {
                if (xhr) {
                    // xhr may be undefined, for example when downloading JavaScript
                    for (var i = 0, len = astrobin_common.globals.requests.length; i < len; ++i) {
                        if (astrobin_common.globals.requests[i] == xhr) {
                            // drop completed xhr from list
                            astrobin_common.globals.requests.splice(i, 1);
                            break;
                        }
                    }
                }
                // execute base
                if (complete) {
                    complete.apply(this, arguments)
                }
            }

            var r = $.ajax.apply(this, arguments);
            if (r) {
                // r may be undefined, for example when downloading JavaScript
                astrobin_common.globals.requests.push(r);
            }
            return r;
        };

        setTimeout(function() {
            astrobin_common.listen_for_notifications(username, '', '');
        }, 1000);
    },

    clearText: function(field) {
        if (field.defaultValue == field.value) field.value = '';
        else if (field.value == '') field.value = field.defaultValue;
    },

    showHideAdvancedSearch: function() {
    },

    init_ajax_csrf_token: function() {
        $(document).ajaxSend(function(event, xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            function sameOrigin(url) {
                // url could be relative or scheme relative or absolute
                var host = document.location.host; // host + port
                var protocol = document.location.protocol;
                var sr_origin = '//' + host;
                var origin = protocol + sr_origin;
                // Allow absolute or scheme relative URLs to same origin
                return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                    (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                    // or any other URL that isn't scheme relative or absolute i.e relative.
                    !(/^(\/\/|http:|https:).*/.test(url));
            }

            function safeMethod(method) {
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }

            if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        });
    },

    setup_gear_popovers: function() {
        $('.gear-popover').each(function() {
            $(this).qtip({
                position: {
                    my: "left center",
                    at: "right center"
                },
                show: {
                    solo: true
                },
                hide: {
                    fixed: true,
                    delay: 1000
                },
                content: {
                    text: "...",
                    ajax: {
                        loading: false,
                        url:  $(this).attr('data-load'),
                        type: 'GET',
                        dataType: 'json',
                        timeout: 5000,
                        success: function(data, status) {
                            this.set('content.text', data.html);
                            window.loadAstroBinImages(data.html);
                        }
                    }
                }
            });
        });
    },

    setup_subject_popovers: function() {
        $('.subject-popover').each(function() {
            $(this).qtip({
                position: {
                    my: "left center",
                    at: "right center"
                },
                show: {
                    solo: true
                },
                hide: {
                    fixed: true,
                    delay: 1000
                },
                content: {
                    text: "...",
                    ajax: {
                        loading: false,
                        url:  $(this).attr('data-load'),
                        type: 'GET',
                        dataType: 'json',
                        timeout: 5000,
                        success: function(data, status) {
                            this.set('content.text', data.html);
                        }
                    }
                }
            });
        });
    },

    setup_user_popovers: function() {
        $('.user-popover').each(function() {
            $(this).qtip({
                position: {
                    my: "left center",
                    at: "right center"
                },
                show: {
                    solo: true
                },
                hide: {
                    fixed: true,
                    delay: 1000
                },
                content: {
                    text: "...",
                    ajax: {
                        loading: false,
                        url:  $(this).attr('data-load'),
                        type: 'GET',
                        dataType: 'json',
                        timeout: 5000,
                        success: function(data, status) {
                            this.set('content.text', data.html);
                        }
                    }
                }
            });
        });
    },

    init: function(current_username, config) {
        /* Init */
        astrobin_common.globals.current_username = current_username;
        $.extend(true, astrobin_common.config, config);
   }
};

/**********************************************************************
 * Image detail
 *********************************************************************/
astrobin_image_detail = {
    config: {
        /* Menus */
        topmenu   : '.topnav',
        submenu   : 'div.sub',
        timeout   : 500,

        upload_revision_action: {
            dialog: {
                title: '',
                body : ''
            },
            element  : 'a.upload-revision',
            form_html: '',
            csrf_token: '',
            url       : '/upload/revision/process/',
            fileDefaultText: '',
            fileBtnText: '',
            uploadingText: '',
            width: 300
        },

        delete_action: {
            dialog: {
                title : '',
                body  : '',
                button: '',
                height: 230
            },
            element: 'a.delete-everything',
            url    : '/delete/'
        },

        delete_revision_action: {
            dialog: {
                title : '',
                body  : '',
                button: '',
                height: 230
            },
            element: 'a.delete-revision',
            url    : '/delete/revision/'
        },

        delete_original_action: {
            dialog: {
                title : '',
                body  : '',
                button: '',
                height: 230
            },
            element: 'a.delete-original',
            url    : '/delete/original/'
        }
    },

    globals: {
        /* Menus */
        closeTimer    : 0,
        currentItem   : 0,

        /* Common */
        image_id      : 0,
        revision_id   : 0,
        image_username: ''
    },

    top_close: function() {
        if (astrobin_image_detail.globals.currentItem) {
            astrobin_image_detail.globals.currentItem.css('visibility', 'hidden');
        }
    },

    top_open: function(_parent, _klass) {
        astrobin_image_detail.top_canceltimer();
        astrobin_image_detail.top_close();
        astrobin_image_detail.globals.currentItem =
            _parent.find(_klass).css('visibility', 'visible');
    },

    top_timer: function() {
        astrobin_image_detail.globals.closetimer =
            window.setTimeout(astrobin_image_detail.top_close,
                              astrobin_image_detail.config.timeout);
    },

    top_canceltimer: function() {
        if(astrobin_image_detail.globals.closetimer) {
            window.clearTimeout(astrobin_image_detail.globals.closetimer);
            astrobin_image_detail.globals.closetimer = 0;
        }
    },

    setup_upload_revision: function() {
        $(astrobin_image_detail.config.upload_revision_action.element).click(function() {
            var dlg = $('\
                <div id="dialog-attention" title="' + astrobin_image_detail.config.upload_revision_action.dialog.title + '"></div>')
                .html('\
                    <div class="upload-revision">\
                    <p>\
                        ' + astrobin_image_detail.config.upload_revision_action.dialog.body + '\
                    </p>\
                    <form id="upload-revision" class="form-horizontal" action="' + astrobin_image_detail.config.upload_revision_action.url + '" method="post" enctype="multipart/form-data">\
                        ' + astrobin_image_detail.config.upload_revision_action.form_html + '\
                        <div style="display:none;"><input type="hidden" id="csrfmiddlewaretoken" name="csrfmiddlewaretoken" value="' + astrobin_image_detail.config.upload_revision_action.csrf_token + '" /></div> \
                        <input type="hidden" name="image_id" value="' + astrobin_image_detail.globals.image_id  + '"/>\
                    </form>\
                    <div style="text-align:center" class="progressbar"><img src="/sitestatic/images/loading-bar.gif" alt=""/></div>\
                    </div>\
                ')
                .dialog({
                    width: astrobin_image_detail.config.upload_revision_action.width,
                    resizable: false,
                    modal: true});

            $('input:file').uniform(
               {fileDefaultText: astrobin_image_detail.config.upload_revision_action.fileDefaultText,
                fileBtnText: astrobin_image_detail.config.upload_revision_action.fileBtnText
               }
            );
            $('form#upload-revision').live('submit', function() {
                form = $(this);
                progressbar = form.parent().find('.progressbar');

                form.hide();
                progressbar.show();

                return true;
            });

        });
    },

    setup_delete: function() {
        $(astrobin_image_detail.config.delete_action.element).click(function() {
            $('<div id="dialog-confirm" title="' +
              astrobin_image_detail.config.delete_action.dialog.title +
              '"></div>')
                .html('\
                        <p>\
                            <span class="ui-icon ui-icon-alert"\
                                  style="float:left; margin:0 7px 20px 0;">\
                            </span>' + astrobin_image_detail.config.delete_action.dialog.body + '\
                        </p>')
                .dialog({
                    resizable: false,
                    height: astrobin_image_detail.config.delete_action.dialog.height,
                    modal: true,
                    buttons: [
                        {
                            text: 'OK',
                            'class': 'btn btn-primary',
                            click: function() {
                                $(this).dialog('close');
                                window.location = astrobin_image_detail.config.delete_action.url + astrobin_image_detail.globals.image_id;
                            }
                        },
                        {
                            text: $.i18n._('Cancel'),
                            'class': 'btn',
                            click: function() {
                                $(this).dialog('close');
                            }
                        }
                    ]
                });

            return false;
        });
    },

    setup_delete_revision: function() {
        $(astrobin_image_detail.config.delete_revision_action.element).click(function() {
            $('<div id="dialog-confirm" title="' +
              astrobin_image_detail.config.delete_revision_action.dialog.title +
              '"></div>')
                .html('\
                        <p>\
                            <span class="ui-icon ui-icon-alert"\
                                  style="float:left; margin:0 7px 20px 0;">\
                            </span>' + astrobin_image_detail.config.delete_revision_action.dialog.body + '\
                        </p>')
                .dialog({
                    resizable: false,
                    height: astrobin_image_detail.config.delete_revision_action.dialog.height,
                    modal: true,
                    buttons: [
                        {
                            text: 'OK',
                            'class': 'btn btn-primary',
                            click: function() {
                                $(this).dialog('close');
                                window.location = astrobin_image_detail.config.delete_revision_action.url + astrobin_image_detail.globals.revision_id;
                            }
                        },
                        {
                            text: $.i18n._('Cancel'),
                            'class': 'btn',
                            click: function() {
                                $(this).dialog('close');
                            }
                        }
                    ]
                });

            return false;
        });
    },

    setup_delete_original: function() {
        $(astrobin_image_detail.config.delete_original_action.element).click(function() {
            $('<div id="dialog-confirm" title="' +
              astrobin_image_detail.config.delete_original_action.dialog.title +
              '"></div>')
                .html('\
                        <p>\
                            <span class="ui-icon ui-icon-alert"\
                                  style="float:left; margin:0 7px 20px 0;">\
                            </span>' + astrobin_image_detail.config.delete_original_action.dialog.body + '\
                        </p>')
                .dialog({
                    resizable: false,
                    height: astrobin_image_detail.config.delete_original_action.dialog.height,
                    modal: true,
                    buttons: [
                        {
                            text: 'OK',
                            'class': 'btn btn-primary',
                            click: function() {
                                $(this).dialog('close');
                                window.location = astrobin_image_detail.config.delete_original_action.url + astrobin_image_detail.globals.image_id;
                            }
                        },
                        {
                            text: $.i18n._('Cancel'),
                            'class': 'btn',
                            click: function() {
                                $(this).dialog('close');
                            }
                        }
                    ]
                });

            return false;
        });
    },

    setup_view_more_subjects: function() {
        var $reminder = $('#more-subjects .reminder');
        var $more = $('#more-subjects .more');
        var $hide = $('#more-subjects .hide');

        $reminder.hide();
        $more.show();

        $more.find('a').click(function() {
            $reminder.show();
            $more.hide();
            $hide.show();
            return false;
        });

        $hide.find('a').click(function() {
            $reminder.hide();
            $hide.hide();
            $more.show();
            return false;
        });
    },

    init: function(image_id, revision_id, image_username, config) {
        /* Init */
        astrobin_image_detail.globals.image_id = image_id;
        astrobin_image_detail.globals.revision_id = revision_id;
        astrobin_image_detail.globals.image_username = image_username;
        $.extend(true, astrobin_image_detail.config, config);

        /* Revisions */
        astrobin_image_detail.setup_upload_revision();

        /* Delete */
        astrobin_image_detail.setup_delete();
        astrobin_image_detail.setup_delete_revision();
        astrobin_image_detail.setup_delete_original();

        /* View more subjects */
        astrobin_image_detail.setup_view_more_subjects();
    }
};

/**********************************************************************
 * Stats
 *********************************************************************/
astrobin_stats = {
    config: {
    },

    globals: {
        previousPoint: null
    },

    /* Private */
    _showTooltip: function(x, y, contents) {
        $('<div id="stats-tooltip">' + contents + '</div>').css( {
            position: 'absolute',
            display: 'none',
            top: y - 25,
            left: x,
            border: '1px solid #fdd',
            padding: '2px',
            'background-color': '#fee',
            color: '#000',
            opacity: 0.80
        }).appendTo("body").fadeIn(200);
    },

    /* Public */
    enableTooltips: function(plot) {
        $(plot).bind("plothover", function (event, pos, item) {
            if (item) {
                if (astrobin_stats.globals.previousPoint != item.dataIndex) {
                    astrobin_stats.globals.previousPoint = item.dataIndex;

                    $("#stats-tooltip").remove();
                    var x = item.datapoint[0].toFixed(2),
                        y = item.datapoint[1].toFixed(2);

                    astrobin_stats._showTooltip(item.pageX, item.pageY, y);
                }
            }
            else {
                $("#stats-tooltip").remove();
                astrobin_stats.globals.previousPoint = null;
            }
        });
    },

    plot: function(id, url, timeout, data, options) {
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            timeout: timeout,
            cache: false,
            success: function(series) {
                $.plot(
                    $(id),
                    [{
                        label: series['flot_label'],
                        color: "#CC4B2E",
                        data: series['flot_data']
                    }],
                    series['flot_options']);
            }
        });
    },

    plot_pie: function(id, url, timeout, data, options) {
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            timeout: timeout,
            cache: false,
            success: function(series) {
                $.plot(
                    $(id),
                    series['flot_data'],
                    series['flot_options']);
            }
        });
    },


    init: function(config) {
        /* Init */
        $.extend(true, astrobin_stats.config, config);
    }
};

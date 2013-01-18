from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.mail import send_mail

from hu_authzproxy.authzproxy_login_handler import AuthZProxyLoginHandler
from hu_authzproxy.authz_proxy_validation_info import AuthZProxyValidationInfo

from django.conf import settings

#import logging
#logger = logging.getLogger(__name__)

def view_handle_authz_callback(request):
    """View to handle pin callback
    If authentication is succesful:
        - go to a specified 'next' link 
        - or default to the django admin index page
    """

    #
    if request.GET and request.GET.get('next', None) is not None:
        next = request.GET.get('next')
    else:
        next =  reverse('admin:index', args={})
        #next =  reverse('admin:index', args={})

    # How Django handles authentication after pin is verfied. 
    # See "pin_login_handler.PinLoginHandler" class handler for more info
    # This allows anyone with a harvard pin to log in
    access_settings = { 'restrict_to_existing_users':True \
                         , 'restrict_to_active_users':True \
                         , 'restrict_to_staff':True \
                         , 'restrict_to_superusers':False}
    
    
    authz_validation_info = AuthZProxyValidationInfo(request=request\
                                 ,app_names=settings.HU_PIN_LOGIN_APP_NAMES\
                                 , gnupghome=settings.GNUPG_HOME 
                                 , gpg_passphrase=settings.GPG_PASSPHRASE
                                 , is_debug=settings.DEBUG)

    authz_pin_login_handler = AuthZProxyLoginHandler(authz_validation_info\
                                     , **access_settings)

    if authz_pin_login_handler.did_login_succeed():
        login(request, authz_pin_login_handler.get_user())
        return HttpResponseRedirect(next)
    
    # Errors while logging in!
    # 
    # Retrieve error messages from the AuthZProxyLoginHandler
    error_messages = []
    authz_errs = authz_pin_login_handler.get_err_msgs()
    if not authz_errs is None:
        error_messages += authz_errs

    # Retrieve error flags from the AuthZProxyLoginHandler
    err_dict = authz_pin_login_handler.get_error_dict()   # get error lookup for use 
    for k,v in err_dict.iteritems():
        if v is True:
            error_messages.append(' %s -> [%s]' % (k,v))
            print ' %s -> [%s]' % (k,v)
            
    # add the user IP address
    error_messages.append('user IP address: %s' % request.META.get('REMOTE_ADDR', None))

    # send email message to the admins
    try:
        admin_emails = map(lambda x: x[1], settings.ADMINS)
    except:
        admin_emails = None
    #print admin_emails
    if admin_emails and len(admin_emails) > 0:
        send_mail('Course database log in fail info', 'Here is the message. %s' % ('\n'.join(error_messages)), admin_emails[0], admin_emails,fail_silently=False)
        
    # send the error flags to the template
    return render_to_response('hu_authz_handler/view_authz_login_failed.html', err_dict, context_instance=RequestContext(request))


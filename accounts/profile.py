from django.http import QueryDict
from forms import UserProfileForm
from models import UserProfile


def get_profile(request):
    """
    note that this requires an authenticated
    user before we try calling it
    """
    # user = request.user if request.user.is_authenticated() else None
    user = request.user
    try:
        profile = user.userprofile
        # profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=user)
        profile.save()
    return profile


def set_profile(request):
    post_data = request.POST.copy()
    profile = get_profile(request)
    # print('profile admin', profile.sex)
    # print('post_data', post_data)
    new_dict = dict(post_data.iterlists())
    # print('new_dict', new_dict)
    new_dict[u"sex"] = [unicode(profile.sex)]
    # print('new_dict_sex', new_dict)
    #  convertir el dict {} python en un QueryDict
    post_data = QueryDict("", mutable=True)
    for k, v in new_dict.iteritems():
        post_data.setlist(k, v)
    post_data._mutable = False
    print('post_data2', post_data)
    profile_form = UserProfileForm(None, post_data, instance=profile)
    if profile_form.is_valid():
        print('tamos entrando')
        # print(profile_form.se)
        profile_form.save()
    else:
        print('errors', profile_form.errors)

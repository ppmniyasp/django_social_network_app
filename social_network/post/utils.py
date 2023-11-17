from users.models import Profile
from django.db.models import Q

def searchProfile(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    search_profile = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(username__icontains=search_query)
    )

    return search_profile, search_query
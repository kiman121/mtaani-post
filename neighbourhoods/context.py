from django.core.exceptions import ObjectDoesNotExist


def place_label(request):
    user = request.user
    if not user.is_authenticated:
        return {"place_label": "Sample neighbourhood"}
    try:
        profile = user.profile
    except ObjectDoesNotExist:
        return {"place_label": "No neighbourhood yet"}
    if profile.neighbourhood_id:
        return {"place_label": profile.neighbourhood.name}
    return {"place_label": "No neighbourhood yet"}

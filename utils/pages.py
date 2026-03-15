from administrator.models import ListingPage


def get_listing_page(slug):

    return ListingPage.objects.filter(
        slug=slug,
        is_active=True
    ).first()
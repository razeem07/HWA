from administrator.models import GlobalSettings,SocialLink,LegalPage,MenuGroup

def global_data(request):

    def get_menu(slug):
        return MenuGroup.objects.prefetch_related('items').filter(
            slug=slug,
            is_active=True
        ).first()


    settings = GlobalSettings.objects.first()
    social_links = SocialLink.objects.filter(is_active=True).order_by('order')
    legal_pages = LegalPage.objects.filter(is_active=True)
    
    return {
        'global_settings': settings,
         'social_links': social_links,
         'legal_pages':legal_pages,
        'main_menu': get_menu('main-menu'),
        'specialization_menu': get_menu('specialization-menu'),
        'quick_links_menu': get_menu('quick-links-menu'),
    }
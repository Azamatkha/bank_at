from django.contrib.admin import AdminSite

class ResursAdminSite(AdminSite):
    site_header = "BANK RESURS AT ADMIN"
    site_title = "Resurs Admin"
    index_title = "Resurs boshqaruv paneli"

resurs_admin_site = ResursAdminSite(name="resurs_admin")
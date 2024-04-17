from django.contrib import admin


class ProjectAdminSite(admin.AdminSite):
    site_title = "Simple Project admin"
    site_header = "Simple Django Project Administration"

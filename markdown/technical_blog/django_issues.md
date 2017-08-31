### When rendering templates in django, there is one issue that kept me stuck.
> suppose you have 2 templates in 2 sub-apps. Both of which reference 2 different static files with the same name.
This case, django will serve both page with the same static file from the first app(follow the sequence from settings.py installed_apps attribute)

I think this would be an issue since it will cause some rendering problems. So every static file should be identical in django?
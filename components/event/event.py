from django_components import component

@component.register("event")
class Event(component.Component):
    # Templates inside `[your apps]/components` dir and `[project root]/components` dir will be automatically found. To customize which template to use based on context
    # you can override def get_template_name() instead of specifying the below variable.
    template_name = "event/event.html"

    # def get_context_data(self, **kwargs):
    #     return {
    #         "eventname": kwargs['eventname'],
    #         "organization": kwargs['organization'],
    #         "link": kwargs['link'],
    #         "datetime": kwargs['datetime'],
    #         "location": kwargs['location'],
    #     }
    def get_context_data(self, eventname, organization, link, datetime, location):
        return {
            "eventname": eventname,
            "organization": organization,
            "link": link,
            "datetime": datetime,
            "location": location,
        }
    
    class Media:
        css = "components/event.css"
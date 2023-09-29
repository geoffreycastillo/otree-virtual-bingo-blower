from ._builtin import Page


class Welcome(Page):
    form_model = 'player'
    form_fields = ['browser_name', 'browser_version', 'device', 'os_name', 'os_version', 'fps']


page_sequence = [Welcome]

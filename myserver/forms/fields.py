def _clean_form(self):
    try:
        cleaned_data = self.clean()
    except ValidationError as e:
        self.add_error(None, e)
    else:
        if cleaned_data is not None:
            self.cleaned_data = cleaned_data


def clean(self):
    """
    Hook for doing any extra form-wide cleaning after Field.clean() has been
    called on every field. Any ValidationError raised by this method will
    not be associated with a particular field; it will have a special-case
    association with the field named '__all__'.
    """
    return self.cleaned_data
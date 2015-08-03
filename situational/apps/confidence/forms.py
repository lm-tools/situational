from django import forms


class ConfidenceReportForm(forms.Form):
    success_confidence = forms.ChoiceField(
        label="How confident are you that you will find a work?",
        choices=(
            (1, "Not at all - I have serious barriers to overcome"),
            (2, ""),
            (3, ""),
            (4, "About average"),
            (5, ""),
            (6, ""),
            (7, "Very confident - I will find the right thing, quickly"),
        ),
        widget=forms.RadioSelect(),
    )

    search_confidence = forms.ChoiceField(
        label="How confident are you searching for work?",
        choices=(
            (1, "Not at all - I don't know where to start"),
            (2, ""),
            (3, ""),
            (4, "About average"),
            (5, ""),
            (6, ""),
            (7, "Very confident - I can search online, write cover letters, "
                "meet people face-to-face etc"),
        ),
        widget=forms.RadioSelect(),
    )

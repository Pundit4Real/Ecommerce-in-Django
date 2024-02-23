from django import froms
from core.models import ProductReview


class ProductReviewForm(forms.ModelForm):
    review = forms.forms.CharField(widget=forms.Textarea(attrs={'placeholder':"write review"}))

    class Meta:
        model = ProductReview
        fields = ['review','rating']
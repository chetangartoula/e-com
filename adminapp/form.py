

from django import forms

from userapp.models import Orders, Product




class ProductCreationForm(forms.ModelForm):


    class Meta:
        model = Product
        fields= "__all__"
        # include= ["extra_image"]
        exclude= ['id','created_at',"updated_at","vendor","events"]


        widgets = {
            'pro_name':forms.TextInput(attrs={'class':'form-control form-control-line'}),
            'Pro_desc':forms.TextInput(attrs={'class':'form-control form-control-line'}),
            'rate_product':forms.NumberInput(attrs={'class':'form-control form-control-line'}),
            'pro_catagory':forms.Select(attrs={'class':'form-control form-select'}),
            'pro_brnd':forms.Select(attrs={'class':'form-select form-select'}),
            'pro_collection':forms.Select(attrs={'class':'form-control form-select',}),
            'tags':forms.SelectMultiple(attrs={'class':'form-select form-select choices-multiple-remove-button'}),
            'color':forms.SelectMultiple(attrs={'class':'form-control form-control-line choices-multiple-remove-button'}),
            'product_type':forms.SelectMultiple(attrs={'class':'form-control multiselect choices-multiple-remove-button'}),
            'price':forms.NumberInput(attrs={'class':'form-control form-control-line'}),
            'old_price':forms.NumberInput(attrs={'class':'form-control form-select'}),
            'quantity':forms.NumberInput(attrs={'class':'form-control form-select'}),
            # # 'main_image':forms.FileInput(),
            'events':forms.Select(attrs={'class':'form-control form-control-line'}),
            'discount':forms.NumberInput(attrs={'class':'form-control form-control-line'}),
            
        }
   
    
class OrderCreationForm(forms.ModelForm):


       
    class Meta:
        model = Orders
        fields= "__all__"
        exclude = ["id"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user.is_vendor == True:
            self.fields.pop('order_by')
            self.fields.pop('order_product')
            self.fields.pop('total_amount')
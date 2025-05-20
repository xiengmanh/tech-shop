from django import forms
from django.contrib.auth.forms import SetPasswordForm


class CheckoutForm(forms.Form):
    full_name = forms.CharField(label='Họ tên', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Số điện thoại', widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Địa chỉ', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Mật khẩu mới",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Nhập mật khẩu mới"
        }),
        error_messages={'required': 'Bạn chưa nhập mật khẩu mới.'}
    )
    new_password2 = forms.CharField(
        label="Xác nhận mật khẩu mới",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Nhập lại mật khẩu mới"
        }),
        error_messages={'required': 'Bạn chưa xác nhận mật khẩu mới.'}
    )
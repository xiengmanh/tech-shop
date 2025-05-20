from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import CheckoutForm
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Trang chủ
def home(request):
    keyword = request.GET.get('q', '')
    is_searching = bool(keyword)

    if is_searching:
        products = Product.objects.filter(
            Q(name__icontains=keyword) |
            Q(category__name__icontains=keyword)
        )
    else:
        products = Product.objects.all()

    # Dữ liệu theo từng danh mục (chỉ hiển thị nếu có sản phẩm)
    categories = {
        'Laptop': products.filter(category__name__iexact='Laptop'),
        'Điện thoại': products.filter(category__name__iexact='Điện thoại'),
        'Tablet': products.filter(category__name__iexact='Tablet'),
        'Smartwatch': products.filter(category__name__iexact='Smartwatch'),
        'Tai nghe': products.filter(category__name__iexact='Tai nghe'),
        'PC': products.filter(category__name__iexact='PC'),
    }

    # Lọc bỏ các danh mục không có sản phẩm khi đang tìm kiếm
    if is_searching:
        categories = {k: v for k, v in categories.items() if v.exists()}

    context = {
        'keyword': keyword,
        'is_searching': is_searching,
        'categories': categories
    }

    return render(request, 'store/home.html', context)

from django.core.paginator import Paginator

def paginate_products(products, request, per_page=8):
    paginator = Paginator(products, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


# Chi tiết sản phẩm
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

# Đăng ký
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Tài khoản đã tồn tại.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Đăng ký thành công. Vui lòng đăng nhập.')
            return redirect('login')
    return render(request, 'store/register.html')

# Đăng nhập
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Sai tài khoản hoặc mật khẩu.')
    return render(request, 'store/login.html')

# Đăng xuất
def logout_view(request):
    logout(request)
    return redirect('home')

# Giỏ hàng
def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session['cart'] = cart
        messages.success(request, '✅ Đã thêm vào giỏ hàng!')
        
        return redirect('product_detail', pk=product_id)
    else:
        return redirect('home')

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
        total += subtotal

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, '🗑️ Đã xoá sản phẩm khỏi giỏ hàng.')
    return redirect('cart')

# Thanh toán
@login_required(login_url='/login/')
def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
        total += subtotal

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price
                )

            # Xóa giỏ hàng sau khi đặt hàng xong
            request.session['cart'] = {}

            messages.success(request, "🎉 Bạn đã đặt hàng thành công! Cảm ơn bạn đã mua sắm tại MShop.")
            return redirect('order_success')

    else:
        form = CheckoutForm()

    return render(request, 'store/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total
    })

@login_required(login_url='/login/')
def order_success(request):
    return render(request, 'store/order_success.html')

from django.core.paginator import Paginator

def paginate_products(queryset, request, per_page=8):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)

def laptop_list(request):
    products = Product.objects.filter(category__name__iexact='Laptop')
    laptops = paginate_products(products, request)
    return render(request, 'store/category.html', {'products': laptops, 'title': 'Laptop'})

def phone_list(request):
    products = Product.objects.filter(category__name__iexact='Điện thoại')
    phones = paginate_products(products, request)
    return render(request, 'store/category.html', {'products': phones, 'title': 'Điện thoại'})

def tablet_list(request):
    products = Product.objects.filter(category__name__iexact='Tablet')
    tablets = paginate_products(products, request)
    return render(request, 'store/category.html', {'products': tablets, 'title': 'Tablet'})

def smartwatch_list(request):
    products = Product.objects.filter(category__name__iexact='Smartwatch')
    watches = paginate_products(products, request)
    return render(request, 'store/category.html', {'products': watches, 'title': 'Smartwatch'})

def headphones_list(request):
    products = Product.objects.filter(category__name__iexact='Tai nghe')
    headphones = paginate_products(products, request)
    return render(request, 'store/category.html', {'products': headphones, 'title': 'Tai nghe'})

def pc_list(request):
    products = Product.objects.filter(category__name__iexact='PC')
    pcs = paginate_products(products, request)
    return render(request, 'store/category.html', {'products': pcs, 'title': 'PC'})

from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # newest first
    return render(request, 'store/my_orders.html', {'orders': orders})

# Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def profile_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        if full_name:
            request.user.first_name = full_name  # 👈 Lưu vào first_name
            request.user.save()
        return redirect('profile')  # Cập nhật xong reload lại trang
    return render(request, 'store/profile.html')

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from .forms import CustomSetPasswordForm

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomSetPasswordForm
    template_name = 'store/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

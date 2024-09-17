from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name="productapp"

urlpatterns = [
    path('allproducts/',views.allproducts,name="allproducts"),
    path('uploadproduct/',views.uploadproduct,name="uploadproduct"),
    path('category/<str:tag>/', views.category_view, name='category_view'),
    path('details/<str:product_id>/', views.details, name='details'),
    path('product/<int:product_id>/',views.product_detail,name="product_detail"),
    path('purchase/<int:selection_id>/', views.purchase, name="purchase"),
    path('save-details/', views.save_details, name='save_details'),
    path('account/', views.account, name='account'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('uploadmagazine/', views.uploadmagazine, name='uploadmagazine'),
    path('magazine/', views.magazine, name='magazine'),
    path('shop/',views.shop,name="shop"),
    path('uploadshop/',views.upload_shop,name="upload_shop"),
    path('add-to-cart/',views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('shopdetail/<int:id>/',views.shopdetail, name='shopdetail'),
    path('about/',views.about,name="about"),
    path('fetch_shop/',views.fetch_shop,name="fetch_shop"),
    path('fetch_products/',views.fetch_products,name="fetch_products"),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_summary, name='checkout_summary'),
    path('success/', views.success, name='success'),
    path('designsuccess/', views.designsuccess, name='designsuccess'),
    path('userorders/', views.userorders, name='userorders'),
    path('toggle_like/', views.toggle_like, name='toggle_like'),
    path('liked_products/', views.liked_products, name='liked_products'),
    path('faculty/', views.faculty, name='faculty'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin_product_view/', views.admin_product_view, name='admin_product_view'),
    path('admin_shop_view/', views.admin_shop_view, name='admin_shop_view'),
    path('order-detail/<int:order_id>/<str:order_type>/', views.admin_order_detail, name='admin_order_detail'),


]


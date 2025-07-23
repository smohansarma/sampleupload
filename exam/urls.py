from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
# from .views import GeneratePdf

app_name='exam'

urlpatterns = [
    path('',login,name='login'),
    path('home',home,name='home'),
    path('q1',q1,name='q1'),
    path('technical',technical,name='technical'),
    path('developer',developer,name='developer'),
    path('python',python,name='python'),
    path('java',java,name='java'),
    path('sql',sql,name='sql'),
    path('hardware',hardware,name='hardware'),
    path('cctv',cctv,name='cctv'),
    path('networking',networking,name='networking'),
    path('router',router,name='router'),
    path('server',server,name='server'),
    path('digital',digital,name='digital'),
    path('photoshop',photoshop,name='photoshop'),
    path('flash',flash,name='flash'),
    path('canva',canva,name='canva'),
    path('admin2',admin2,name='admin'),
    path('result/<int:id>/<str:date>/<str:topic>',result,name='result'),
    path('hr',hr,name='hr'),
    path('accounts',accounts,name='accounts'),
    path('form',form,name='form'),
    path(
    'download-pdf/<int:candidate_id>/<str:date>/<str:test_type>/',
    download_candidates_pdf,
    name='download_candidates_pdf'),
    path('emp_detail/<int:emp_id>/', emp_detail, name='emp_detail'),
    path('download_emp_detail_pdf/<int:emp_id>/', download_emp_detail_pdf, name='download_emp_detail_pdf'),
    path('emp_detail_client/<int:emp_id>', emp_detail_client, name='emp_detail_client'),
    #path('generate-pdf/', GeneratePdf.as_view(), name='generate_pdf'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
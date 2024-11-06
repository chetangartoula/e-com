from userapp.models import Main_Category




def subject_renderer(request):
    cat = Main_Category.objects.all()[:9]
    return {
       "Category_list": cat,
    }
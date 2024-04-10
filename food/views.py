from django.shortcuts import redirect, render
from django.http import HttpResponse

from .forms import ItemForm
from .models import Item
from django.template import loader

# class based view import 
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
# Create your views here.

def index(request):
    item_list = Item.objects.all()
    # template = loader.get_template('food/index.html')
    context = {
        'item_list':item_list,
    }
    # return HttpResponse(template.render(context,request))
    return render (request,'food/index.html',context)

# function based view 
# def detail(request, item_id):
#     # pk is primary key 
#     item = Item.objects.get(pk=item_id)
#     context= {
#         'item':item,
#     }
#     # return HttpResponse("This is item no/id: %s" % item_id)
#     return render(request,'food/detail.html',context)

# class based view 
class FoodDetail(DetailView):
    model = Item
    template_name= 'food/detail.html'



def create_item(request):
    form = ItemForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('food:index')
    return render(request, 'food/item-form.html',{'form': form})
# class based view for create item 
class CreateItem(CreateView):
    model = Item
    fields = ['item_name','item_desc', 'item_price','item_image']
    template_name = 'food/item-form.html'
    def form_valid(self,form):
        form.instance.user_name = self.request.user

        return super().form_valid(form)



def update_item(request, id):
    item = Item.objects.get(id=id)
    form = ItemForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('food:index')
    return render(request, 'food/item-form.html',{'form':form, 'item':item})

def delete_item(request,id):
    item = Item.objects.get(id=id)

    if request.method =='POST':
        item.delete()
        return redirect('food:index')
    return render(request, 'food/item_delete.html',{'item':item} )

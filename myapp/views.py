from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Expenses
from django.contrib import messages
from django.db.models import Sum

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
@login_required(login_url='/')
def addExpenses(request):
    Current_user = request.user
    if request.method=='POST':
        expense_reason = request.POST.get('Expense_reason')
        expense_amount = request.POST.get('Expense_amount')
    
        My_Expense = Expenses.objects.create(
            user=Current_user,
            Expense_reason=expense_reason,
            Expense_amount=expense_amount
        )
        My_Expense.save()
        messages.success(request,"Your Expense is logged")
        return redirect("/Expenses")
    if request.method=='GET':
        queryset = Expenses.objects.filter(user=Current_user).order_by("Expense_timestamp")
        p = Paginator(queryset, 5) 
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
            page_obj = p.page(1)
        except EmptyPage:
        # if page is empty then return last page
            page_obj = p.page(p.num_pages)

        total = queryset.aggregate(total_expenses=Sum('Expense_amount'))
        context = {"queryset":page_obj,'total':total}
    return render(request,"Expenses.html",context)

@login_required(login_url='/')
def deleteexpense(request,id):
    queryset= Expenses.objects.get(id=id)
    queryset.delete()
    return redirect('/Expenses')

@login_required(login_url='/')
def updateexpense(request,id):
    queryset= Expenses.objects.get(id=id)
    if request.method == 'POST':
        data=request.POST
        expense_reason=data.get('Expense_reason')
        expense_amount=data.get('Expense_amount')
        queryset.Expense_amount=expense_amount
        queryset.Expense_reason=expense_reason
        queryset.save()
        return redirect('/Expenses')
    return render(request,"UpdateExpenses.html")
# Create your views here.
 
 

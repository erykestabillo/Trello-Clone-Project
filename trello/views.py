from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from .models import Board,BoardList,ListCard,Activity,BoardMembers,CardAttatchments,CardCheckList
from .forms import BoardForm,ListForm,CardForm,UserChangeForm,UserCreationForm,BoardInviteForm, CardAttatchmentForm, CardCheckListForm
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin
from django.contrib.auth.models import PermissionsMixin
from django.urls import reverse,reverse_lazy
from django.views import generic
from django.http import JsonResponse,Http404
from django.views.generic.base import View
from django import template
from django.contrib.auth.models import Group, Permission
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Q


# Create your views here.
class CustomPermissionMixin(object):
    def dispatch(self, request, **kwargs):
        member = BoardMembers.objects.filter(board_id=kwargs.get('board_id'),member_id=request.user)
        if member.exists():
            return super().dispatch(request, **kwargs)
        raise Http404('You do not have permission.')
        
    
class BoardContent(LoginRequiredMixin,CustomPermissionMixin,TemplateView):
    template_name = "trello/board.html"
    login_url = '/accounts/login/'
    def get(self,request, **kwargs):
        board_id = kwargs.get('board_id')
        board = get_object_or_404(Board,id=board_id)
        board_lists = BoardList.objects.filter(board_id=board_id)        
        list_cards = ListCard.objects.filter(is_archived=False)
        board_members = BoardMembers.objects.filter(board=board)
        member_boards = BoardMembers.objects.all()
        activities = Activity.objects.filter(user__in=member_boards.values('member'),board=board).order_by('-date')
        
        return render(request,self.template_name, {'board':board,'board_members':board_members,'board_lists':board_lists,'list_cards':list_cards,'activities':activities,'username':request.user.get_username(),'user':request.user})
        

class ViewBoards(LoginRequiredMixin,TemplateView):
    template_name = "trello/board_list.html"
    login_url = '/accounts/login/'
    def get(self,request):
        boards = Board.objects.filter(date_created__lte=timezone.now(),user=request.user).order_by('date_created')
        member_boards = BoardMembers.objects.filter(member=request.user).exclude(board__user=request.user)        
        
        return render(request, self.template_name, {'boards':boards,'member_boards':member_boards,'user':request.user})

class AddBoard(TemplateView):
    template_name = "trello/board_new.html"
    form = BoardForm
    def get(self,request):
        form = self.form()
        return render(request, self.template_name, {'form':form})
    

class AddBoardAjax(TemplateView):
    template_name = "trello/board_new.html"
    form = BoardForm
    def post(self,request, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            board_form = form.save(commit=False)
            board_form.user = request.user
            board_form.save()
            board_member, created = BoardMembers.objects.get_or_create(member=request.user,board=board_form)
            if (created):
                board_member.save()            
            else:
                template_name ="trello/already_a_member.html"
                return render(request,template_name,{'board_member':board_member})
            return JsonResponse({})
        return JsonResponse({}, status=400)


class EditBoardAjax(TemplateView):
    template_name = "trello/board_edit.html"
    form = BoardForm
    def post(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(request.POST,instance=board)
        if form.is_valid():
            board_form = form.save(commit=False)
            board_form.user = request.user
            board_form.save()
            return JsonResponse({'board_form':board_form.title})
        return JsonResponse({}, status=400)


class EditBoard(TemplateView):
    template_name = "trello/board_edit.html"
    form = BoardForm
    def get(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(instance=board)
        return render(request, self.template_name, {'form':form,'board_id':board.id})
    

class DeleteBoard(LoginRequiredMixin,TemplateView):
    def get(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"), user=request.user)
        board.delete()
        return redirect('viewBoards')


class AddListAjax(TemplateView):
    template_name = "trello/add_list.html"
    form = ListForm
    
    def post(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(request.POST)
        if form.is_valid():
            board_form = form.save(commit=False)
            board_form.board = board
            board_form.save()
            return JsonResponse({'board_form':board_form.title})
        return JsonResponse({}, status=400)


class AddList(TemplateView):
    template_name = "trello/add_list.html"
    form = ListForm
    def get(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form()
        return render(request, self.template_name, {'form':form,'board_id':board.id})
    

class EditList(TemplateView):
    template_name = "trello/edit_list.html"
    form = ListForm
    def get(self,request,**kwargs):
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(instance=board_list)
        return render(request, self.template_name, {'form':form,'list_id':board_list.id,'board_id':board.id})


class EditListAjax(TemplateView):
    template_name = "trello/edit_list.html"
    form = ListForm
    def post(self,request,**kwargs):
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(request.POST,instance=board_list)
        if form.is_valid():
            board_form = form.save(commit=False)
            board_form.board = board
            board_form.save()
            Activity.objects.create(content_object=board_list,board=board, activity_type=Activity.EDIT_LIST, user=request.user)
            return JsonResponse({})
        return JsonResponse({}, status=400)


class EditCard(TemplateView):
    template_name = "trello/edit_card.html"
    form = CardForm
    def get(self,request,**kwargs):
        card = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        form = self.form(instance=card)
        return render(request, self.template_name, {'form':form,'board_id':board.id,'list_id':board_list.id,'card_id':card.id})

class EditCardAjax(TemplateView):
    template_name = "trello/edit_card.html"
    form = CardForm
    def post(self,request,**kwargs):
        card_object = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(request.POST,instance=card_object)
        if form.is_valid():
            board_form = form.save(commit=False)
            board_form.user = request.user
            Activity.objects.create(content_object=card_object,board=board, activity_type=Activity.EDIT_CARD, user=request.user)
            board_form.save()
            return JsonResponse({'board_id':kwargs.get("board_id"),'list_id':kwargs.get("list_id"),'card_id':kwargs.get("card_id")})
        return JsonResponse({}, status=400)


class ChangeCard(TemplateView):
    
    def post(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        card = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        board_list = get_object_or_404(BoardList,id=request.POST.get('id'))
        card.board_list = board_list
        card.save()
        Activity.objects.create(content_object=card,board=board, activity_type=Activity.MOVED_CARD, user=request.user)
        return JsonResponse({}, status=200)


class Attatchments(TemplateView):
    form = CardAttatchmentForm
    def post(self,request,**kwargs):
        card = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(request.POST, request.FILES)
        
        if form.is_valid():
            file_data = form.save(commit=False)
            file_data.card = card
            file_data.save()
            return JsonResponse({'board_id':board.id,'card_id':card.id})
        return JsonResponse({}, status=400)

class DeleteAttatchment(TemplateView):
    def get(self,request,**kwargs):
        card = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        attchmnt = get_object_or_404(CardAttatchments,id=kwargs.get('attchment_id'))
        attchmnt.delete()
        return redirect('boardContent', board_id=board.id, member_id=request.user.id)


class ViewCard(TemplateView):
    template_name = "trello/card_view.html"
    form = CardAttatchmentForm
    formCl = CardCheckListForm
    def get(self,request,**kwargs):
        form = self.form()
        formCl = self.formCl()
        card = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        attatchments = CardAttatchments.objects.filter(card=card)
        checklists = CardCheckList.objects.filter(card=card)
        return render(request, self.template_name,{'form':form,'formCl':formCl,'checklists':checklists,'attatchments':attatchments,'board':board,'list':board_list,'card':card})
    

class AddCard(TemplateView):
    template_name = "trello/add_card.html"
    form = CardForm
    def get(self,request,**kwargs):
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form()
        return render(request, self.template_name, {'form':form,'board_id':board.id,'list_id':board_list.id})
    

class AddCardAjax(TemplateView):
    template_name = "trello/add_card.html"
    form = CardForm
    def post(self,request,**kwargs):
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(request.POST)
        if form.is_valid():
            board_form = form.save(commit=False)
            board_form.board_list = board_list         
            board_form.save()
            Activity.objects.create(content_object=board_form,board=board, activity_type=Activity.ADD_CARD, user=request.user)
            return JsonResponse({})
        return JsonResponse({}, status=400)


class DeleteCard(TemplateView):
    def get(self,request,**kwargs):
        card = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        card.delete()
        return redirect('boardContent', board_id=board.id, member_id=request.user.id)


class ArchiveCard(TemplateView):
    def get(self,request,**kwargs):
        card = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        card.is_archived = True
        card.save()
        Activity.objects.create(content_object=card,board=board, activity_type=Activity.ARCHIVE_CARD, user=request.user)
        return redirect('boardContent', board_id=board.id, member_id=request.user.id)

class CardArchives(TemplateView):
    template_name = "trello/archived_cards.html"
    def get(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        archived_cards = ListCard.objects.filter(is_archived=True)
        return render(request,self.template_name, {'archived_cards':archived_cards,'board_id':board.id})
    
        
class RestoreCard(TemplateView):
    def get(self,request,**kwargs):
        card = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        card.is_archived = False
        card.save()
        Activity.objects.create(content_object=card,board=board, activity_type=Activity.RESTORE_CARD, user=request.user)
        return redirect('boardContent', board_id=board.id, member_id=request.user.id)
    

class DeleteList(TemplateView):
    def get(self,request,**kwargs):
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        board_list.delete()
        
        return redirect('boardContent', board_id=board.id, member_id=request.user.id)



 
class SignUp(TemplateView):
    form = UserCreationForm
    template_name = 'registration/signup.html'
    def get(self,request,**kwargs):
        form = self.form()
        return render(request, self.template_name, {'form':form})
    def post(self,request,**kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            form.clean_password2()
            form.save()
            return redirect('/accounts/login/')
        return render(request,self.template_name,{'form':form})


class PasswordReset(TemplateView):
    template_name = 'registration/signup.html'
    def get(self,request,**kwargs):
        form = self.form()
        return render(request, self.template_name, {'form':form})
    def post(self,request,**kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            form.clean_password2()
            form.save()
            return redirect('/accounts/login/')
        return render(request,self.template_name,{'form':form})

class InviteMember(TemplateView):
    template_name = "trello/invite_member.html"
    login_url = '/accounts/login/'
    form = BoardInviteForm
    def get(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form()
        return render(request, self.template_name, {'form':form,'board_id':board.id})
    def post(self,request,**kwargs):
        form = self.form(request.POST)
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        user = request.user
        if (form.is_valid):
            invite_member_form = form.save(commit=False)
            subject = 'You have been invited to my site'
            message = ' '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [invite_member_form.email,]
            html_message = render_to_string(
                'trello/email_template.html',
                {                
                'board':board,
                'user': user.get_username(),
                'uuid':invite_member_form.uuid,
                'domain': request.META['HTTP_HOST'],
                }
            )
            send_mail( subject, message, email_from, recipient_list, html_message=html_message)
            return JsonResponse({})
        
class LinkInviteMember(LoginRequiredMixin ,TemplateView):
    login_url = '/accounts/login/'
    template_name = "trello/invitation_accept.html"
    def get(self,request,**kwargs):
        return render(request, self.template_name)
    
    def post(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        board_member, created = BoardMembers.objects.get_or_create(member=request.user,board=board)
        if (created):
            board_member.save()            
        else:
            template_name ="trello/already_a_member.html"
            return render(request,template_name,{'board_member':board_member})
            
        return redirect('boardContent', board_id=board.id, member_id=request.user.id)
      
        
class AddCheckList(TemplateView):
    formCl = CardCheckListForm
    def post(self,request,**kwargs):
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        card = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        formCl = self.formCl(request.POST)
        if formCl.is_valid():
            cl_data = formCl.save(commit=False)
            cl_data.card = card
            cl_data.save()
            
            return JsonResponse({})
        return JsonResponse({}, status=400)


        


    

    

    







        
        
        
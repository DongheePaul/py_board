from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator  
from django.contrib.auth.decorators import login_required



def index(request):
    page = request.GET.get('page', '1')
    question_list = Question.objects.order_by('-create_date')
    #전체 데이터, 페이지당 보이는 갯수
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list' : page_obj}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

#urlpatterns에서 설정한 int:question_id 값이 전달됨
@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    '''
    Question, Answer 모델은 외래키로 연결되어 있어 question객체로 답변 데이터를 삽입 가능.
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    혹은 Answer 모델을 직접 사용가능. 
    answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    answer.save()
    '''
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()

    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

                #로그인 url 지정. 로그아웃 상태에서 해당 함수가 호출되면 지정한 url로 이동.
@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        #request.POST를 인수로 QuestionForm을 생성한 경우 reqeust.POST에 담긴 subject, content 값이 QuestionForm의 subject, content 속성에 자동으로 저장됨.
        form = QuestionForm(request.POST)
        #form의 유효성 검사. 저장된 subject, content의 값이 올바르지 않다면 form에 오류 메시지가 저장됨. 이 오류 메시지를 활용 가능.
        if form.is_valid():
            #임시 저장하여 question 객체를 리턴받음. commit=False는 임시저장을 의미.
            #QuestionForm에는 현재 create_date 속성이 없으므로 변수에 임시 저장한 뒤 create_date에 값을 성정한 후 save()로 실제 저장.
            question = form.save(commit=False)
            question.author = request.user #author 속성에 로그인한 계정 저장.
            #데이터 저장 시점에 생성해야 하는 값이므로 QuestionForm에 등록하지 않음.
            question.create_date = timezone.now()
            #데이터를 실제로 저장.
            question.save()
            return redirect('pybo:index')
    #질문등록하기 버튼을 누르면 get 방식으로 들어옴. 링크를 통한 페이지 요청은 무조건 get.
    else:
        form = QuestionForm()
        context = {'form': form}
        return render(request, 'pybo/question_form.html', context)

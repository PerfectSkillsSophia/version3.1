from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from assessments.models import *
from django.contrib import messages
from assessments.models import *
from administration.models import *
from django.urls import reverse
from django.db.models import Q
from sophia import settings
from .result import *
from thefuzz import fuzz

@staff_member_required
@login_required(login_url='login')
def dashboard(request):
	assessment = allAssessment.objects
	video = videoAns.objects.all()[:5]
	return render(request, 'dashboard.html', {'assessment': assessment, 'video': video})


@staff_member_required
@login_required(login_url='login')
def allAnswer(request):
	all_data = videoAns.objects.all().values('user_name', 'assessment_name','identi').distinct()

	#return render(request, 'all_submmision.html', {'video': video, 'url': url})
	return render(request, 'submmision.html', {'all_data': all_data})

@staff_member_required
@login_required(login_url='login')
def detail_view(request, user_name, assessment_name,identi):
    url = settings. MEDIA_URL
    data = videoAns.objects.filter(user_name=user_name, assessment_name=assessment_name ,identi=identi)
    return render(request, 'detail.html', {'data': data , 'url': url,})    
    
@staff_member_required
@login_required(login_url='login')
def searchbar(request):
	query = request.GET.get('q')
	url = settings. MEDIA_URL
	if query:
		results = videoAns.objects.filter(
		    Q(user_name__icontains=query) | Q(assessment_name__icontains=query))
	else:
		results = videoAns.objects.all()
	return render(request, 'all_submmision.html', {'results': results, 'query': query, 'url': url})

@staff_member_required
@login_required(login_url='login')
def add_assessment(request):
	return render(request,'add_assessments.html')

@staff_member_required
@login_required(login_url='login')
def Add_assessment(request):
	if request.method == 'GET':
		ass_name = request.GET.get('ass_name')
		ass_dec = request.GET.get('ass_dec')
		new_ass = allAssessment()
		new_ass.assessmentName = ass_name
		new_ass.assessmentDes = ass_dec
		new_ass.save()
		return redirect('addassessment')
	return redirect('addassessment')

@staff_member_required
@login_required(login_url='login')
def view_assessments(request, ass_id):
	ass_id = ass_id
	assessment = allAssessment.objects.filter(assId=ass_id)
	allque = allAssessment.objects.get(assId=ass_id).question_set.all()[:5]
	return render(request, 'assview.html', {'ques': allque, 'ass': assessment})


@staff_member_required
@login_required(login_url='login')
def Add_question(request):
		if request.method == 'GET':
			que = request.GET.get('que')
			correctanswer = request.GET.get('correctanswer')
			ass_name = request.GET.get('ass')
			ass = allAssessment.objects.get(assessmentName=ass_name)
			ass_id = ass.assId
			new_que = Question()
			new_que.quostion = que
			new_que.correctanswer = correctanswer

			new_que.assessment = ass
			new_que.save()
			return HttpResponseRedirect(reverse("view", args=(ass_id,)))
		return HttpResponseRedirect(reverse("view", args=(ass_id,)))


@staff_member_required
@login_required(login_url='login')
def generate_tras(request, ansId):
	ref_url = request.META.get('HTTP_REFERER')
	result = videoAns.objects.get(ansId=ansId)
	vf = result.videoAns.path
	import requests
	API_KEY = "623cfea0aba24d8f981195bbc20d48e0"
	filename = vf

# Upload Module Begins
	def read_file(filename, chunk_size=5242880):
		with open(filename, 'rb') as _file:
			while True:
				data = _file.read(chunk_size)
				if not data:
					break
				yield data

	headers = {'authorization': API_KEY}
	response = requests.post('https://api.assemblyai.com/v2/upload',
                        headers=headers,
                        data=read_file(filename))

	json_str1 = response.json()
# Upload Module Ends

# Submit Module Begins
	endpoint = "https://api.assemblyai.com/v2/transcript"
	json = {
    	"audio_url": json_str1["upload_url"]
	}

	response = requests.post(endpoint, json=json, headers=headers)

	json_str2 = response.json()
# Submit Module Ends

# CheckStatus Module Begins
	endpoint = "https://api.assemblyai.com/v2/transcript/" + json_str2["id"]

	response = requests.get(endpoint, headers=headers)

	json_str3 = response.json()

	while json_str3["status"] != "completed":
		response = requests.get(endpoint, headers=headers)
		json_str3 = response.json()
# CheckStatus Module Ends
	result.trasnscript = json_str3["text"]
	result.save()
	messages.success(request, 'Transcript is generated Successfully.')
	return HttpResponseRedirect(ref_url)

@staff_member_required
@login_required(login_url='login')
def generate_result(request,ansId):
	if ansId:
		ref_url = request.META.get('HTTP_REFERER')
		answer = videoAns.objects.filter(ansId=ansId)
		for trans in answer:
			s1=trans.question_id.correctanswer
			s2 = trans.trasnscript
		accuracy = FindAcc(s1,s2)
		answer=videoAns.objects.get(ansId=ansId)
		answer.answer_accurecy=accuracy
		answer.save()
		print(s1)
		print(s2)
	return HttpResponseRedirect(ref_url)

@staff_member_required
@login_required(login_url='login')
def testresultfunc(request):
	if request.method == 'GET':
		s1 = request.GET.get('s1')
		s2 = request.GET.get('s2')
		accuracy = FindAcc(s1,s2)
		print(s1,s2)
		print(accuracy)
	return render(request, 'testresult.html',{'accuracy': accuracy,'s1':s1,'s2':s2})

def testresult(request):

	return render(request, 'testresult.html')

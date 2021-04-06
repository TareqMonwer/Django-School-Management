from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from notices.forms import NoticeDocumentForm, NoticeForm
from notices.models import NoticeDocument, Notice


def publish_notice_documents(request, notice_pk=0):
    
    if request.method == 'POST':
        if 'notice-form' in request.POST:
            form = NoticeForm(request.POST, request.FILES)
            if form.is_valid():
                expires_at = form.cleaned_data['expires_at']
                form.instance.uploaded_by = request.user
                form.instance.expires_at = expires_at
                notice = form.save()
                return redirect('notices_dashboard:publish_notice_documents', notice_pk=notice.pk)
        elif 'documents-form' in request.POST:
            form = NoticeDocumentForm(request.POST, request.FILES)
            notice = get_object_or_404(Notice, pk=notice_pk)
            if form.is_valid():
                input_files = form.cleaned_data['input_file']
                for file in input_files:
                    NoticeDocument.objects.create(notice=notice, file=file)
                return redirect(notice.get_absolute_url())
            else:
                data = {
                    'message': 'Error while uploading documents.',
                    'is_valid': False
                }
                return JsonResponse(data)
    else:
        if notice_pk != 0:
            notice = get_object_or_404(Notice, pk=notice_pk)
        else:
            notice = None
        documents_form = NoticeDocumentForm()
        notice_form = NoticeForm()
        ctx = {
            'documents_form': documents_form,
            'notice_form': notice_form,
            'notice': notice,
        }
        return render(request, 'notices/dashboard/add_notice.html', ctx)

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from .models import Track
import json


# Create your views here.
def addLogWork(issueId, workTime):
    import requests

    url = f"http://127.0.0.1:8080/rest/api/2/issue/{issueId}/worklog"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer NTA4NDUzODQzMzQ1OhVJAIXosL+iv2PGjcQY8CloP8ua"
    }
    data = {
        "timeSpentSeconds": workTime,
        "comment": "TimeTracker Logged a Transition"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.status_code)
    print(response.text)


def track(request):
    if request.method == "POST":
        issueId = json.loads(request.body.decode('utf-8'))['issue']['id']
        userKey = json.loads(request.body.decode('utf-8'))['user']['key']
        projectKey = json.loads(request.body.decode(
            'utf-8'))['issue']['fields']['project']['key']
        transitionFromStatus = json.loads(
            request.body.decode('utf-8'))['transition']['from_status']
        transitionToStatus = json.loads(
            request.body.decode('utf-8'))['transition']['to_status']
        if transitionFromStatus == 'To Do' and transitionToStatus == 'In Progress':
            transitionStatus = "Start Work"
        elif transitionFromStatus == 'In Progress' and transitionToStatus == 'To Do':
            transitionStatus = "End Work"

        new = Track()
        new.issueId = issueId
        new.userKey = userKey
        new.projectKey = projectKey
        if transitionStatus == "Start Work":
            new.transitionStatus = 'S'
        elif transitionStatus == "End Work":
            new.transitionStatus = 'E'
        new.save()

        if transitionStatus == "End Work":
            start = get_object_or_404(Track, issueId=issueId, userKey=userKey,
                                      transitionStatus='S', isLastTransition=True)
            startTimestamp = int(datetime.timestamp(start.transitionTime))

            end = get_object_or_404(Track, issueId=issueId, userKey=userKey,
                                    transitionStatus='E', isLastTransition=True)
            endTimestamp = int(datetime.timestamp(end.transitionTime))

            Track.objects.filter(issueId=issueId, userKey=userKey,
                                 transitionStatus='S', isLastTransition=True).update(isLastTransition=False)
            Track.objects.filter(issueId=issueId, userKey=userKey,
                                 transitionStatus='E', isLastTransition=True).update(isLastTransition=False)

            addLogWork(issueId, endTimestamp-startTimestamp)

    else:
        print("Bad Request")

    return HttpResponse()

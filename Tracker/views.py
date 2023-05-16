from django.http import HttpResponse
from .models import Track
import json


# Create your views here.
def addLogWork(issueId):
    import requests

    url = f"http://127.0.0.1:8080/rest/api/2/issue/{issueId}/worklog"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer NTA4NDUzODQzMzQ1OhVJAIXosL+iv2PGjcQY8CloP8ua"
    }
    data = {
        "timeSpent": "1h",
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
            # Track.objects.filter().update(active=True)
            ...

    else:
        print("Request Not POST")

    return HttpResponse()

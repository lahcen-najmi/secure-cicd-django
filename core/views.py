from django.http import HttpResponse


def home(request):
    html = """
    <html>
    <head><title>Secure CI/CD Django App</title></head>
    <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 80px;">
        <h1>Pipeline CI/CD Securise avec Jenkins</h1>
        <p>Application Django deployee avec succes via le pipeline DevSecOps.</p>
        <p>SonarQube - Bandit - Trivy</p>
    </body>
    </html>
    """
    return HttpResponse(html)

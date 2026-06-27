from django.shortcuts import render
import requests
import socket
from .models import Scan
from .models import Scan
from django.db.models import Avg
from django.http import HttpResponse
from .pdf_generator import generate_pdf
def home(request):

    result = None

    if request.method == "POST":

        url = request.POST.get("website_url")

        try:
            import os

            print("HTTP_PROXY =", os.environ.get("HTTP_PROXY"))
            print("HTTPS_PROXY =", os.environ.get("HTTPS_PROXY"))
            print("http_proxy =", os.environ.get("http_proxy"))
            print("https_proxy =", os.environ.get("https_proxy"))
            session = requests.Session()
            session.trust_env = False

            response = session.get(
    url,
    timeout=10,
    allow_redirects=True,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

            response_time = round(
                response.elapsed.total_seconds(),
                2
            )

            domain = url.replace("https://", "").replace("http://", "").split("/")[0]

            ip = socket.gethostbyname(domain)

            status_code = response.status_code

            https = "Oui" if url.startswith("https://") else "Non"

            redirect = "Oui" if response.history else "Non"

            ssl = "Valide" if https == "Oui" else "Non"

            robots = session.get(
           url.rstrip("/") + "/robots.txt",
           timeout=5,
           headers={
           "User-Agent": "Mozilla/5.0"
    }
)

            robots_result = (
                "Trouvé"
                if robots.status_code == 200
                else "Introuvable"
            )

            sitemap = session.get(
    url.rstrip("/") + "/sitemap.xml",
    timeout=5,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

            sitemap_result = (
                "Trouvé"
                if sitemap.status_code == 200
                else "Introuvable"
            )

            x_frame = (
                "Présent"
                if response.headers.get("X-Frame-Options")
                else "Absent"
            )

            csp = (
                "Présent"
                if response.headers.get("Content-Security-Policy")
                else "Absent"
            )

            hsts = (
                "Présent"
                if response.headers.get("Strict-Transport-Security")
                else "Absent"
            )

            powered_by = response.headers.get(
                "X-Powered-By",
                ""
            ).lower()

            server = response.headers.get(
                "Server",
                ""
            ).lower()

            technology = "Inconnue"

            if "wordpress" in powered_by:
                technology = "WordPress"

            elif "php" in powered_by:
                technology = "PHP"

            elif "django" in powered_by:
                technology = "Django"

            elif "laravel" in powered_by:
                technology = "Laravel"

            elif "express" in powered_by:
                technology = "Node.js (Express)"

            elif "asp.net" in powered_by:
                technology = "ASP.NET"

            elif "nginx" in server:
                technology = "Nginx"

            elif "apache" in server:
                technology = "Apache"

            elif "iis" in server:
                technology = "Microsoft IIS"

            elif "cloudflare" in server:
                technology = "Cloudflare"

            cookies = (
                "Oui"
                if response.cookies
                else "Non"
            )

            content_type = response.headers.get(
                "Content-Type",
                "Inconnu"
            )

            content_length = response.headers.get(
                "Content-Length",
                "Inconnu"
            )
            score = 0

            if status_code == 200:
                score += 20

            if https == "Oui":
                score += 20

            if x_frame == "Présent":
                score += 20

            if csp == "Présent":
                score += 20

            if hsts == "Présent":
                score += 20

            print("Before save")

            Scan.objects.create(
                url=url,
                status_code=status_code,
                score=score,
                https=https,
                ssl=ssl,
                technology=technology,
                response_time=response_time
            )

            print("Saved successfully")

            result = {
                "url": url,
                "status_code": status_code,
                "score": score,
                "ssl": ssl,
                "https": https,
                "redirect": redirect,
                "technology": technology,
                "x_frame_options": x_frame,
                "csp": csp,
                "hsts": hsts,
                "response_time": response_time,
                "robots": robots_result,
                "sitemap": sitemap_result,
                "cookies": cookies,
                "content_type": content_type,
                "content_length": content_length,
            }

        except Exception as e:      # ← 8 spaces

            total_scans = Scan.objects.count()      # ← 12 spaces

            average_score = Scan.objects.aggregate( # ← 12 spaces
                Avg("score")                        # ← 16 spaces
            )["score__avg"] or 0                   # ← 12 spaces

            last_scan = Scan.objects.order_by("-created_at").first()   # ← 12 spaces

            history = Scan.objects.order_by("-created_at")[:5]         # ← 12 spaces

            return render(                      # ← 12 spaces
                request,                        # ← 16 spaces
                "index.html",                   # ← 16 spaces
                {                               # ← 16 spaces
                    "result": None,             # ← 20 spaces
                    "error": str(e),            # ← 20 spaces
                    "total_scans": total_scans, # ← 20 spaces
                    "average_score": round(average_score), # ← 20 spaces
                    "last_scan": last_scan,     # ← 20 spaces
                    "history": history,         # ← 20 spaces
                }                               # ← 16 spaces
            )                                   # ← 12 spaces

    total_scans = Scan.objects.count()          # ← 4 spaces

    average_score = Scan.objects.aggregate(     # ← 4 spaces
        Avg("score")                            # ← 8 spaces
    )["score__avg"]                             # ← 4 spaces

    if average_score is None:                   # ← 4 spaces
        average_score = 0                       # ← 8 spaces

    average_score = round(average_score)        # ← 4 spaces

    last_scan = Scan.objects.order_by("-created_at").first()  # ← 4 spaces

    history = Scan.objects.order_by("-created_at")[:5]        # ← 4 spaces

    return render(                             # ← 4 spaces
        request,                               # ← 8 spaces
        "index.html",                          # ← 8 spaces
        {                                      # ← 8 spaces
            "result": result,                  # ← 12 spaces
            "total_scans": total_scans,        # ← 12 spaces
            "average_score": average_score,    # ← 12 spaces
            "last_scan": last_scan,            # ← 12 spaces
            "history": history,                # ← 12 spaces
        }                                      # ← 8 spaces
    )                                          # ← 4 spaces
def download_pdf(request):
    return generate_pdf(request)
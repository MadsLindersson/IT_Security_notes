"""HTTP-only teaching app. Fake accounts and form fields are deliberately readable."""
from html import escape
from pathlib import Path
from string import Template
from portal_data import STUDENTS
from http.cookies import SimpleCookie, CookieError
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import secrets
import threading
import time
from urllib.parse import parse_qs, urlsplit

ACCOUNTS = {"alice": "alice123", "bob": "bob123"}
SESSIONS = {}
LOCK = threading.Lock()
COOKIE = "mosec_session"


ROOT = Path(__file__).resolve().parent
TEMPLATES = {p.stem: Template(p.read_text()) for p in (ROOT / "templates").glob("*.html")}
ASSETS = {
    "/static/css/main.css": (ROOT / "static/css/main.css", "text/css; charset=utf-8"),
    "/static/js/main.js": (ROOT / "static/js/main.js", "text/javascript; charset=utf-8"),
}


def portal_page(view, user=None, error=""):
    context = {"error": f'<p class="alert" role="alert">{escape(error)}</p>' if error else ""}
    if user:
        student = STUDENTS[user]
        context.update({key: escape(str(value)) for key, value in student.items()
                        if not isinstance(value, list)})
        context["username"] = escape(user)
        context["classes"] = "".join(
            '<li><div class="date-block"><span>' + escape(day) + '</span><strong>' + escape(date)
            + '</strong></div><div class="class-details"><span class="class-time">' + escape(hour)
            + '</span><strong>' + escape(course) + '</strong><span class="class-room">' + escape(room)
            + '</span></div></li>' for day, date, hour, course, room in student["classes"])
        context["grades"] = "".join('<tr><td>' + escape(course) + '</td><td><span class="grade">'
            + escape(grade) + '</span></td></tr>' for course, grade in student["grades"])
        context["notifications"] = "".join('<li><strong>' + escape(title) + '</strong><span>'
            + escape(detail) + '</span></li>' for title, detail in student["notifications"])
    content = TEMPLATES[view].substitute(context)
    navigation = ""
    header_right = '<span class="header-label">MoSec Ltd. · Staff services</span>'
    if user:
        header_right = ('<div class="account"><span class="avatar" aria-hidden="true">'
            + context["initials"] + '</span><span class="account-name">' + context["name"]
            + '</span><form action="/logout" method="post"><button class="logout">Log out</button></form></div>')
        links = "".join(f'<a href="/{route}"' + (' aria-current="page"' if view == route else '')
                        + f'>{label}</a>' for route, label in [("dashboard", "Staff Dashboard"), ("profile", "Employee Profile")])
        navigation = '<nav class="nav-bar" aria-label="Main navigation"><div class="nav-inner">' + links + '</div></nav>'
    return TEMPLATES["base"].substitute(title={"login":"Sign in", "dashboard":"Staff Dashboard",
        "profile":"Employee Profile", "error":"Page not found"}[view], header_right=header_right,
        navigation=navigation, main_class="login-page" if view == "login" else "page", content=content)


class App(BaseHTTPRequestHandler):
    def respond(self, status, body="", content_type="text/html; charset=utf-8", **headers):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        for name, value in headers.items():
            self.send_header(name.replace("_", "-"), value)
        self.end_headers()
        self.wfile.write(data)

    def token(self):
        try:
            cookies = SimpleCookie(self.headers.get("Cookie", ""))
            return cookies[COOKIE].value if COOKIE in cookies else ""
        except CookieError:
            return ""

    def user(self):
        with LOCK:
            user, expiry = SESSIONS.get(self.token(), (None, 0))
            return user if expiry > time.monotonic() else None

    def do_GET(self):
        path = urlsplit(self.path).path
        if path in ASSETS:
            file, mime = ASSETS[path]
            self.respond(200, file.read_bytes(), content_type=mime)
            return
        user = self.user()
        if path == "/":
            self.respond(200, portal_page("dashboard" if user else "login", user))
        elif path == "/login":
            self.respond(200, portal_page("login"))
        elif path in {"/dashboard", "/profile"}:
            if not user:
                self.respond(303, Location="/login")
            else:
                self.respond(200, portal_page(path[1:], user))
        else:
            self.respond(404, portal_page("error", user))

    def do_POST(self):
        path = urlsplit(self.path).path
        if path == "/logout":
            with LOCK:
                SESSIONS.pop(self.token(), None)
            self.respond(303, Location="/login", Set_Cookie=f"{COOKIE}=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax")
            return
        if path != "/login":
            self.respond(404, portal_page("error", self.user()))
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 4096:
                raise ValueError()
            if self.headers.get("Content-Type", "").split(";")[0] != "application/x-www-form-urlencoded":
                raise ValueError()
            fields = parse_qs(self.rfile.read(length).decode("utf-8"), max_num_fields=8)
            if len(fields.get("username", [])) != 1 or len(fields.get("password", [])) != 1:
                raise ValueError()
        except (ValueError, UnicodeError):
            self.respond(400, portal_page("login", error="Please check your sign-in details and try again."))
            return
        user, password = fields["username"][0], fields["password"][0]
        if user not in ACCOUNTS or ACCOUNTS[user] != password:
            self.respond(401, portal_page("login", error="Invalid username or password"))
            return
        now = time.monotonic()
        token = secrets.token_urlsafe(32)
        with LOCK:
            for old in list(SESSIONS):
                if SESSIONS[old][1] <= now:
                    del SESSIONS[old]
            SESSIONS.pop(self.token(), None)
            if len(SESSIONS) >= 1024:
                del SESSIONS[next(iter(SESSIONS))]
            SESSIONS[token] = (user, now + 3600)
        # Secure is deliberately absent so the initial HTTP exercise can use sessions.
        self.respond(303, Location="/dashboard",
            Set_Cookie=f"{COOKIE}={token}; Path=/; Max-Age=3600; HttpOnly; SameSite=Lax")


if __name__ == "__main__":
    ThreadingHTTPServer((Path("/etc/mosec/portal-bind").read_text().strip(), 8080), App).serve_forever()

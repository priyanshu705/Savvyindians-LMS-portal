from django.conf import settings


class CSPMiddleware:
    """
    Adds a strict Content-Security-Policy header suitable for this app,
    while allowing YouTube embeds and common fonts. In DEBUG, allows inline
    scripts/styles for developer convenience.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Baseline sources
        self_src = "'self'"
        unsafe_inline = "'unsafe-inline'" if settings.DEBUG else ""
        unsafe_eval = "'unsafe-eval'" if settings.DEBUG else ""

        # Allow YouTube player and assets
        yt_domains = [
            "https://www.youtube.com",
            "https://www.youtube-nocookie.com",
            "https://s.ytimg.com",
            "https://i.ytimg.com",
            "https://www.gstatic.com",
        ]

        # Compose directives
        directives = [
            f"default-src {self_src}",
            # Scripts: self + (inline/eval in DEBUG) + YouTube/gstatic
            "script-src "
            + " ".join(filter(None, [self_src, unsafe_inline, unsafe_eval] + yt_domains)),
            # Styles: self + inline (for Django admin and templates) + Google Fonts CSS
            "style-src "
            + " ".join(
                filter(None, [self_src, unsafe_inline, "https://fonts.googleapis.com"])
            ),
            # Images: self + data: + ytimg
            "img-src "
            + " ".join([self_src, "data:", "https://i.ytimg.com", "https://*.ytimg.com"]),
            # Fonts: self + data: + Google Fonts
            "font-src "
            + " ".join([self_src, "data:", "https://fonts.gstatic.com"]),
            # Frames: allow YouTube embeds
            "frame-src " + " ".join(["https://www.youtube.com", "https://www.youtube-nocookie.com"]),
            # Media could be local uploads
            f"media-src {self_src} blob:",
            # XHR/fetch
            f"connect-src {self_src}",
            # Disallow plugins
            "object-src 'none'",
            # Prevent clickjacking by ancestors
            "frame-ancestors 'none'",
            # Base
            "base-uri 'self'",
            # Upgrade mixed content when possible
            "upgrade-insecure-requests",
        ]

        csp_value = "; ".join(directives)
        response.headers["Content-Security-Policy"] = csp_value
        return response

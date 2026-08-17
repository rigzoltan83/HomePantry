class PrefixMiddleware:
    def __init__(self, app, prefix=""):
        self.app = app

        prefix = (prefix or "").strip()

        if prefix and not prefix.startswith("/"):
            prefix = "/" + prefix

        self.prefix = prefix.rstrip("/")

    def __call__(self, environ, start_response):
        if not self.prefix:
            return self.app(
                environ,
                start_response,
            )

        path = environ.get(
            "PATH_INFO",
            "",
        )

        if path == self.prefix:
            environ["SCRIPT_NAME"] = self.prefix
            environ["PATH_INFO"] = "/"

            return self.app(
                environ,
                start_response,
            )

        prefix_with_slash = (
            self.prefix + "/"
        )

        if path.startswith(prefix_with_slash):
            environ["SCRIPT_NAME"] = self.prefix
            environ["PATH_INFO"] = (
                path[len(self.prefix):]
                or "/"
            )

            return self.app(
                environ,
                start_response,
            )

        start_response(
            "404 Not Found",
            [
                (
                    "Content-Type",
                    "text/plain; charset=utf-8",
                )
            ],
        )

        return [
            b"Not Found"
        ]

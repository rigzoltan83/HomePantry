class PrefixMiddleware:
    def __init__(
        self,
        app,
        prefix="",
    ):
        self.app = app

        prefix = (
            prefix
            or ""
        ).strip()

        if (
            prefix
            and not prefix.startswith("/")
        ):
            prefix = "/" + prefix

        self.prefix = prefix.rstrip("/")

    def __call__(
        self,
        environ,
        start_response,
    ):
        if not self.prefix:
            return self.app(
                environ,
                start_response,
            )

        forwarded_proto = (
            environ.get(
                "HTTP_X_FORWARDED_PROTO",
                "",
            )
            .split(",")[0]
            .strip()
            .lower()
        )

        forwarded_host = (
            environ.get(
                "HTTP_X_FORWARDED_HOST",
                "",
            )
            .split(",")[0]
            .strip()
        )

        remote_addr = environ.get(
            "REMOTE_ADDR",
            "",
        )

        is_local_proxy = (
            remote_addr
            in {
                "127.0.0.1",
                "::1",
            }
        )

        is_https_proxy = (
            forwarded_proto == "https"
            and bool(forwarded_host)
        )

        # Tailscale Serve strips the public mount path
        # before forwarding the request to Gunicorn.
        #
        # Restore the external mount point only for
        # requests arriving from the local HTTPS proxy.
        if (
            is_local_proxy
            and is_https_proxy
        ):
            environ["SCRIPT_NAME"] = (
                self.prefix
            )

            return self.app(
                environ,
                start_response,
            )

        # Also support direct requests that explicitly
        # contain the configured prefix.
        path = environ.get(
            "PATH_INFO",
            "",
        )

        if path == self.prefix:
            environ["SCRIPT_NAME"] = (
                self.prefix
            )
            environ["PATH_INFO"] = "/"

            return self.app(
                environ,
                start_response,
            )

        prefix_with_slash = (
            self.prefix + "/"
        )

        if path.startswith(
            prefix_with_slash
        ):
            environ["SCRIPT_NAME"] = (
                self.prefix
            )

            environ["PATH_INFO"] = (
                path[len(self.prefix):]
                or "/"
            )

            return self.app(
                environ,
                start_response,
            )

        # Normal LAN access remains mounted at /
        return self.app(
            environ,
            start_response,
        )

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const input =
            document.getElementById(
                "movement-list-search"
            );

        if (!input) {
            return;
        }

        const rows =
            Array.from(
                document.querySelectorAll(
                    ".js-movement-row"
                )
            );

        const emptyMessage =
            document.getElementById(
                "movement-search-empty"
            );

        const normalizeText = value => {
            return String(value || "")
                .normalize("NFD")
                .replace(
                    /[\u0300-\u036f]/g,
                    ""
                )
                .toLowerCase()
                .trim();
        };

        input.addEventListener(
            "input",
            () => {
                const needle =
                    normalizeText(
                        input.value
                    );

                let visibleCount = 0;

                rows.forEach(
                    row => {
                        const haystack =
                            normalizeText(
                                row.dataset
                                    .movementSearch
                            );

                        const visible =
                            !needle
                            || haystack.includes(
                                needle
                            );

                        row.hidden =
                            !visible;

                        if (visible) {
                            visibleCount += 1;
                        }
                    }
                );

                if (emptyMessage) {
                    emptyMessage.hidden =
                        visibleCount !== 0;
                }
            }
        );
    }
);

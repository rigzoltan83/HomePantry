document.addEventListener(
    "DOMContentLoaded",
    () => {
        const searchInput =
            document.getElementById(
                "inventory-list-search"
            );

        if (!searchInput) {
            return;
        }

        const groups =
            Array.from(
                document.querySelectorAll(
                    ".js-inventory-group"
                )
            );

        const filterButtons =
            Array.from(
                document.querySelectorAll(
                    ".js-inventory-filter"
                )
            );

        const emptyMessage =
            document.getElementById(
                "inventory-search-empty"
            );

        let activeFilter = "all";

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

        const applyFilters = () => {
            const needle =
                normalizeText(
                    searchInput.value
                );

            let visibleCount = 0;

            groups.forEach(
                group => {
                    const haystack =
                        normalizeText(
                            group.dataset
                                .inventorySearch
                        );

                    const searchMatches =
                        !needle
                        || haystack.includes(
                            needle
                        );

                    let statusMatches = true;

                    if (
                        activeFilter === "low"
                    ) {
                        statusMatches =
                            group.dataset.low
                            === "1";
                    }

                    if (
                        activeFilter
                        === "expiring"
                    ) {
                        statusMatches =
                            group.dataset.expiring
                            === "1";
                    }

                    if (
                        activeFilter
                        === "expired"
                    ) {
                        statusMatches =
                            group.dataset.expired
                            === "1";
                    }

                    const visible =
                        searchMatches
                        && statusMatches;

                    group.hidden =
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
        };

        searchInput.addEventListener(
            "input",
            applyFilters
        );

        filterButtons.forEach(
            button => {
                button.addEventListener(
                    "click",
                    () => {
                        activeFilter =
                            button.dataset.filter
                            || "all";

                        filterButtons.forEach(
                            item => {
                                item.classList
                                    .toggle(
                                        "active",
                                        item === button
                                    );
                            }
                        );

                        applyFilters();
                    }
                );
            }
        );
    }
);

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const searchInput =
            document.getElementById(
                "inventory-list-search"
            );

        const locationFilter =
            document.getElementById(
                "inventory-location-filter"
            );

        const clearButton =
            document.getElementById(
                "inventory-filter-clear"
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

        const params =
            new URLSearchParams(
                window.location.search
            );

        const requestedFilter =
            params.get("filter");

        const allowedFilters = new Set([
            "all",
            "low",
            "expiring",
            "expired",
        ]);

        let activeFilter =
            allowedFilters.has(
                requestedFilter
            )
                ? requestedFilter
                : "all";

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

        const groupMatchesStatus =
            group => {
                if (
                    activeFilter === "low"
                ) {
                    return (
                        group.dataset.low
                        === "1"
                    );
                }

                if (
                    activeFilter
                    === "expiring"
                ) {
                    return (
                        group.dataset.expiring
                        === "1"
                    );
                }

                if (
                    activeFilter
                    === "expired"
                ) {
                    return (
                        group.dataset.expired
                        === "1"
                    );
                }

                return true;
            };

        const applyFilters = () => {
            const needle =
                normalizeText(
                    searchInput.value
                );

            const locationId =
                locationFilter
                    ? locationFilter.value
                    : "";

const isFiltered =
    Boolean(needle)
    || Boolean(locationId)
    || activeFilter !== "all";

            let visibleGroupCount = 0;

            groups.forEach(
                group => {
                    const batches =
                        Array.from(
                            group.querySelectorAll(
                                ".js-inventory-batch"
                            )
                        );

const summaries =
    Array.from(
        group.querySelectorAll(
            ".js-inventory-summary"
        )
    );

summaries.forEach(
    summary => {
        summary.hidden =
            isFiltered;
    }
);

                    let visibleBatchCount = 0;

                    batches.forEach(
                        batch => {
                            const haystack =
                                normalizeText(
                                    batch.dataset
                                        .batchSearch
                                );

                            const searchMatches =
                                !needle
                                || haystack.includes(
                                    needle
                                );

                            const locationMatches =
                                !locationId
                                || (
                                    batch.dataset
                                        .locationId
                                    === locationId
                                );

                            const visible =
                                searchMatches
                                && locationMatches;

                            batch.hidden =
                                !visible;

                            if (visible) {
                                visibleBatchCount += 1;
                            }
                        }
                    );

                    const statusMatches =
                        groupMatchesStatus(
                            group
                        );

                    const visible =
                        visibleBatchCount > 0
                        && statusMatches;

                    group.hidden =
                        !visible;

                    if (visible) {
                        visibleGroupCount += 1;

                        if (
                            needle
                            || locationId
                        ) {
                            group.open = true;
                        }
                    }
                }
            );

            if (emptyMessage) {
                emptyMessage.hidden =
                    visibleGroupCount !== 0;
            }
        };

        searchInput.addEventListener(
            "input",
            applyFilters
        );

        if (locationFilter) {
            locationFilter.addEventListener(
                "change",
                applyFilters
            );
        }

        if (clearButton) {
            clearButton.addEventListener(
                "click",
                () => {
                    searchInput.value = "";

                    if (locationFilter) {
                        locationFilter.value = "";
                    }

                    activeFilter = "all";

                    filterButtons.forEach(
                        button => {
                            button.classList.toggle(
                                "active",
                                button.dataset.filter
                                === "all"
                            );
                        }
                    );

                    applyFilters();
                }
            );
        }

        filterButtons.forEach(
            button => {
                button.classList.toggle(
                    "active",
                    button.dataset.filter
                    === activeFilter
                );
            }
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

        applyFilters();
    }
);

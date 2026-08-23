document.addEventListener(
    "DOMContentLoaded",
    () => {
        const tree =
            document.getElementById(
                "storage-active-tree"
            );

        if (!tree) {
            return;
        }

        const rows = Array.from(
            tree.querySelectorAll(
                ".storage-tree-row"
            )
        );

        const storageKey =
            "homepantry-storage-tree-collapsed";

        let collapsedIds =
            new Set();

        try {
            const saved =
                JSON.parse(
                    localStorage.getItem(
                        storageKey
                    ) || "[]"
                );

            if (Array.isArray(saved)) {
                collapsedIds =
                    new Set(saved);
            }
        } catch (_error) {
            collapsedIds =
                new Set();
        }


        function saveState() {
            try {
                localStorage.setItem(
                    storageKey,
                    JSON.stringify(
                        Array.from(
                            collapsedIds
                        )
                    )
                );
            } catch (_error) {
                // Local storage is optional.
            }
        }


        function rowDepth(
            row
        ) {
            return parseInt(
                row.dataset.depth || "0",
                10
            );
        }


        function setToggleState(
            row,
            collapsed
        ) {
            const button =
                row.querySelector(
                    ".storage-tree-toggle"
                );

            if (!button) {
                return;
            }

            button.setAttribute(
                "aria-expanded",
                collapsed
                    ? "false"
                    : "true"
            );

            const icon =
                button.querySelector(
                    ".storage-tree-toggle-icon"
                );

            if (icon) {
                icon.textContent =
                    collapsed
                        ? "▶"
                        : "▼";
            }

            row.classList.toggle(
                "is-collapsed",
                collapsed
            );
        }


        function refreshTree() {
            const collapsedDepths =
                [];

            rows.forEach(
                row => {
                    const depth =
                        rowDepth(row);

                    while (
                        collapsedDepths.length
                        && depth
                        <= collapsedDepths[
                            collapsedDepths.length
                            - 1
                        ]
                    ) {
                        collapsedDepths.pop();
                    }

                    row.hidden =
                        collapsedDepths.length
                        > 0;

                    const hasChildren =
                        row.dataset.hasChildren
                        === "1";

                    const collapsed =
                        hasChildren
                        && collapsedIds.has(
                            row.dataset.locationId
                        );

                    setToggleState(
                        row,
                        collapsed
                    );

                    if (collapsed) {
                        collapsedDepths.push(
                            depth
                        );
                    }
                }
            );
        }


        rows.forEach(
            row => {
                const button =
                    row.querySelector(
                        ".storage-tree-toggle"
                    );

                if (!button) {
                    return;
                }

                button.addEventListener(
                    "click",
                    event => {
                        event.preventDefault();
                        event.stopPropagation();

                        const id =
                            row.dataset.locationId;

                        if (
                            collapsedIds.has(
                                id
                            )
                        ) {
                            collapsedIds.delete(
                                id
                            );
                        } else {
                            collapsedIds.add(
                                id
                            );
                        }

                        saveState();
                        refreshTree();
                    }
                );
            }
        );


        const expandAll =
            document.getElementById(
                "storage-expand-all"
            );

        if (expandAll) {
            expandAll.addEventListener(
                "click",
                event => {
                    event.preventDefault();

                    collapsedIds.clear();

                    saveState();
                    refreshTree();
                }
            );
        }


        const collapseAll =
            document.getElementById(
                "storage-collapse-all"
            );

        if (collapseAll) {
            collapseAll.addEventListener(
                "click",
                event => {
                    event.preventDefault();

                    collapsedIds.clear();

                    rows.forEach(
                        row => {
                            if (
                                row.dataset.hasChildren
                                === "1"
                            ) {
                                collapsedIds.add(
                                    row.dataset.locationId
                                );
                            }
                        }
                    );

                    saveState();
                    refreshTree();
                }
            );
        }


        refreshTree();
    }
);

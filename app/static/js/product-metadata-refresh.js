document.addEventListener(
    "DOMContentLoaded",
    () => {
        const button =
            document.querySelector(
                ".js-refresh-product-metadata"
            );

        const panel =
            document.getElementById(
                "product-refresh-panel"
            );

        const summary =
            document.getElementById(
                "product-refresh-summary"
            );

        const progress =
            document.getElementById(
                "product-refresh-progress"
            );

        const current =
            document.getElementById(
                "product-refresh-current"
            );

        const log =
            document.getElementById(
                "product-refresh-log"
            );

        if (
            !button
            || !panel
            || !summary
            || !progress
            || !current
            || !log
        ) {
            return;
        }

        const rows = Array.from(
            document.querySelectorAll(
                ".js-product-row[data-refresh-url]"
            )
        );

        /*
         * Konzervatív OFF-védelem.
         * Csak tényleges OFF-lekérés után várunk.
         */
        const delayMs = 25000;

        const sleep = milliseconds => {
            return new Promise(
                resolve => {
                    window.setTimeout(
                        resolve,
                        milliseconds
                    );
                }
            );
        };

        const addLogLine = (
            text,
            className = ""
        ) => {
            const line =
                document.createElement(
                    "div"
                );

            line.className =
                "product-refresh-log-line";

            if (className) {
                line.classList.add(
                    className
                );
            }

            line.textContent =
                text;

            log.appendChild(
                line
            );

            log.scrollTop =
                log.scrollHeight;
        };

        const setProgress = (
            completed,
            total
        ) => {
            const percent =
                total > 0
                    ? Math.round(
                        completed
                        / total
                        * 100
                    )
                    : 0;

            progress.style.width =
                `${percent}%`;

            summary.textContent =
                `${completed} / ${total}`;
        };

        const refreshOne =
            async row => {
                const url =
                    row.dataset
                        .refreshUrl;

                const response =
                    await fetch(
                        url,
                        {
                            method: "POST",
                            headers: {
                                "Accept":
                                    "application/json",
                                "X-CSRFToken":
                                    button.dataset
                                        .csrfToken
                                    || "",
                            },
                        }
                    );

                if (!response.ok) {
                    throw new Error(
                        `HTTP ${response.status}`
                    );
                }

                return await response.json();
            };

        button.addEventListener(
            "click",
            async () => {
                if (
                    button.dataset.running
                    === "1"
                ) {
                    return;
                }

                button.dataset.running =
                    "1";

                button.disabled =
                    true;

                panel.hidden =
                    false;

                log.innerHTML =
                    "";

                progress.style.width =
                    "0%";

                let completed = 0;
                let changedProducts = 0;
                let totalChanges = 0;
                let stopped = false;

                const processedUrls =
                    new Set();

                setProgress(
                    0,
                    rows.length
                );

                for (
                    let index = 0;
                    index < rows.length;
                    index += 1
                ) {
                    const row =
                        rows[index];

                    const refreshUrl =
                        row.dataset
                            .refreshUrl;

                    const name =
                        row.dataset
                            .productName
                        || "—";

const hasBarcode =
    row.dataset
        .hasBarcode
    === "1";

                    /*
                     * Hibás vagy duplikált URL:
                     * nincs kérés és nincs várakozás.
                     */

if (!hasBarcode) {
    addLogLine(
        `${name}: `
        + "nincs vonalkód — "
        + "kihagyva"
    );

    completed += 1;

    setProgress(
        completed,
        rows.length
    );

    continue;
}

                    if (
                        !refreshUrl
                        || processedUrls.has(
                            refreshUrl
                        )
                    ) {
                        completed += 1;

                        setProgress(
                            completed,
                            rows.length
                        );

                        continue;
                    }

                    processedUrls.add(
                        refreshUrl
                    );

                    let offRequestOccurred =
                        false;

                    current.textContent =
                        name;

                    try {
                        const data =
                            await refreshOne(
                                row
                            );

                        /*
                         * A saját HomePantry POST
                         * megtörtént, de no_barcode
                         * esetén OFF-kérés nem volt.
                         */
                        offRequestOccurred =
                            data.reason
                            !== "no_barcode";

                        if (
                            data.reason
                            === "rate_limited"
                            || data.reason
                            === "temporary_unavailable"
                        ) {
                            const retryAfter =
                                data.retry_after;

                            let message =
                                (
                                    data.reason
                                    === "rate_limited"
                                )
                                    ? (
                                        "Open Food Facts "
                                        + "rate limit elérve."
                                    )
                                    : (
                                        "Open Food Facts "
                                        + "átmenetileg "
                                        + "nem elérhető."
                                    );

                            if (retryAfter) {
                                message +=
                                    " Újrapróbálható kb. "
                                    + `${retryAfter} `
                                    + "mp múlva.";
                            }

                            addLogLine(
                                message,
                                "product-refresh-error"
                            );

                            current.textContent =
                                message;

                            stopped = true;

                        } else if (
                            data.reason
                            === "no_barcode"
                        ) {
                            addLogLine(
                                `${name}: `
                                + "nincs vonalkód — "
                                + "kihagyva"
                            );

                        } else if (
                            data.reason
                            === "not_found"
                        ) {
                            addLogLine(
                                `${name}: `
                                + "nincs OFF-találat"
                            );

                        } else if (
                            data.changed
                        ) {
                            changedProducts += 1;

                            totalChanges +=
                                Number(
                                    data.changes
                                    || 0
                                );

                            addLogLine(
                                `${name}: `
                                + `${data.changes} `
                                + "új adat",
                                "product-refresh-success"
                            );

                        } else {
                            addLogLine(
                                `${name}: `
                                + "nincs új adat"
                            );
                        }

                    } catch (error) {
                        console.error(
                            "Product metadata "
                            + "refresh failed:",
                            error
                        );

                        addLogLine(
                            `${name}: `
                            + "frissítési hiba",
                            "product-refresh-error"
                        );

                        /*
                         * Ismeretlen HTTP/network
                         * hibánál nem küldünk tovább
                         * automatikusan OFF-kéréseket.
                         */
                        current.textContent =
                            (
                                `${name}: `
                                + "frissítési hiba, "
                                + "a folyamat leállt."
                            );

                        stopped = true;
                    }

                    completed += 1;

                    setProgress(
                        completed,
                        rows.length
                    );

                    if (stopped) {
                        break;
                    }

                    /*
                     * Csak akkor várunk 25 mp-et,
                     * ha tényleges OFF-lekérés
                     * történt.
                     *
                     * no_barcode esetén tehát
                     * azonnal jön a következő sor.
                     */
                    if (
                        offRequestOccurred
                        && index
                        < rows.length - 1
                    ) {
                        current.textContent =
                            (
                                "Várakozás az OFF API "
                                + "védelme miatt..."
                            );

                        await sleep(
                            delayMs
                        );
                    }
                }

                if (!stopped) {
                    current.textContent =
                        (
                            "Kész. "
                            + `${changedProducts} `
                            + "termék frissült, "
                            + `${totalChanges} `
                            + "új adat."
                        );
                }

                button.disabled =
                    false;

                button.dataset.running =
                    "0";
            }
        );
    }
);

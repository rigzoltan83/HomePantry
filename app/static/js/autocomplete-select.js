document.addEventListener(
    "DOMContentLoaded",
    () => {
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

        const setupAutocomplete = wrapper => {
            const allowCustom =
                wrapper.dataset.allowCustom
                === "1";
            const select =
                wrapper.querySelector(
                    ".js-autocomplete-select"
                );

            const input =
                wrapper.querySelector(
                    ".js-autocomplete-input"
                );

            const results =
                wrapper.querySelector(
                    ".autocomplete-results"
                );

            if (
                !select
                || !input
                || !results
            ) {
                return;
            }

            const getOptions = () => {
                return Array.from(
                    select.options
                );
            };

            const getSelectedLabel = () => {
                const option =
                    select.options[
                        select.selectedIndex
                    ];

                if (
                    !option
                    || !option.value
                    || option.value === "0"
                ) {
                    return "";
                }

                return option.textContent
                    .trim();
            };

            const closeResults = () => {
                results.innerHTML = "";
                results.hidden = true;
            };

            const chooseOption = option => {
                select.value =
                    option.value;

                input.value =
                    option.textContent
                        .trim();

                closeResults();

                select.dispatchEvent(
                    new Event(
                        "change",
                        {
                            bubbles: true,
                        }
                    )
                );
            };

            const renderResults = () => {
                const search =
                    normalizeText(
                        input.value
                    );

                const matching =
                    getOptions().filter(
                        option => {
                            if (
                                option.disabled
                                || !option.value
                                || option.value
                                    === "0"
                            ) {
                                return false;
                            }

                            if (!search) {
                                return true;
                            }

                            return normalizeText(
                                option.textContent
                            ).includes(
                                search
                            );
                        }
                    );

                results.innerHTML = "";

                if (!matching.length) {
                    results.hidden = true;
                    return;
                }

                matching
                    .slice(0, 20)
                    .forEach(
                        option => {
                            const button =
                                document
                                    .createElement(
                                        "button"
                                    );

                            button.type =
                                "button";

                            button.className =
                                "autocomplete-result";

                            button.textContent =
                                option.textContent
                                    .trim();

                            button.addEventListener(
                                "mousedown",
                                event => {
                                    event
                                        .preventDefault();

                                    chooseOption(
                                        option
                                    );
                                }
                            );

                            results.appendChild(
                                button
                            );
                        }
                    );

                results.hidden = false;
            };

            select.hidden = true;

            const selectedLabel =
                getSelectedLabel();

            if (
                selectedLabel
                || !allowCustom
            ) {
                input.value =
                    selectedLabel;
            }

            input.addEventListener(
                "focus",
                renderResults
            );

            input.addEventListener(
                "input",
                () => {
                    select.value = "";
                    renderResults();
                }
            );

            input.addEventListener(
                "keydown",
                event => {
                    if (
                        event.key === "Escape"
                    ) {
                        closeResults();
                        return;
                    }

                    if (
                        event.key === "Enter"
                        && !results.hidden
                    ) {
                        const first =
                            results.querySelector(
                                ".autocomplete-result"
                            );

                        if (first) {
                            event.preventDefault();

                            first.dispatchEvent(
                                new MouseEvent(
                                    "mousedown",
                                    {
                                        bubbles: true,
                                    }
                                )
                            );
                        }
                    }
                }
            );

input.addEventListener(
    "blur",
    () => {
        window.setTimeout(
            () => {
                if (!select.value) {
                    const typedValue =
                        normalizeText(
                            input.value
                        );

                    const exactMatches =
                        getOptions().filter(
                            option => {
                                if (
                                    option.disabled
                                    || !option.value
                                    || option.value
                                        === "0"
                                ) {
                                    return false;
                                }

                                return normalizeText(
                                    option.textContent
                                ) === typedValue;
                            }
                        );

                    if (
                        typedValue
                        && exactMatches.length
                        === 1
                    ) {
                        chooseOption(
                            exactMatches[0]
                        );
                    } else {
                        input.value = "";
                    }
                }

                closeResults();
            },
            150
        );
    }
);
        };

        document
            .querySelectorAll(
                ".autocomplete-select"
            )
            .forEach(
                setupAutocomplete
            );

        const refreshUnits =
            async ingredientSelect => {
                const targetId =
                    ingredientSelect.dataset
                        .unitTarget;

                const apiUrl =
                    ingredientSelect.dataset
                        .unitUrl;

                if (
                    !targetId
                    || !apiUrl
                ) {
                    return;
                }

                const unitSelect =
                    document.getElementById(
                        targetId
                    );

                if (!unitSelect) {
                    return;
                }

                if (
                    !ingredientSelect.value
                    || ingredientSelect.value
                        === "0"
                ) {
                    return;
                }

                const currentValue =
                    unitSelect.value;

                const url =
                    new URL(
                        apiUrl,
                        window.location.origin
                    );

                url.searchParams.set(
                    "ingredient_id",
                    ingredientSelect.value
                );

                try {
                    const response =
                        await fetch(
                            url.toString(),
                            {
                                headers: {
                                    "Accept":
                                        "application/json",
                                },
                            }
                        );

                    if (!response.ok) {
                        return;
                    }

                    const data =
                        await response.json();

                    unitSelect.innerHTML = "";

                    if (
                        unitSelect.dataset
                            .allowEmpty === "1"
                    ) {
                        const emptyOption =
                            document
                                .createElement(
                                    "option"
                                );

                        emptyOption.value = "0";

                        emptyOption.textContent =
                            unitSelect.dataset
                                .emptyLabel
                            || "—";

                        unitSelect.appendChild(
                            emptyOption
                        );
                    }

                    data.units.forEach(
                        unit => {
                            const option =
                                document
                                    .createElement(
                                        "option"
                                    );

                            option.value =
                                String(unit.id);

                            option.textContent =
                                unit.label;

                            unitSelect.appendChild(
                                option
                            );
                        }
                    );

                    const stillExists =
                        Array.from(
                            unitSelect.options
                        ).some(
                            option =>
                                option.value
                                === currentValue
                        );

                    if (stillExists) {
                        unitSelect.value =
                            currentValue;
                    } else if (
                        data.default_unit_id
                    ) {
                        unitSelect.value =
                            String(
                                data.default_unit_id
                            );
                    }
                } catch (error) {
                    console.error(
                        "Unit refresh failed:",
                        error
                    );
                }
            };

        document
            .querySelectorAll(
                ".js-ingredient-select"
            )
            .forEach(
                select => {
                    select.addEventListener(
                        "change",
                        () => {
                            refreshUnits(
                                select
                            );
                        }
                    );
                }
            );

        const productSearch =
            document.getElementById(
                "product-list-search"
            );

        if (productSearch) {
            const productRows =
                Array.from(
                    document.querySelectorAll(
                        ".js-product-row"
                    )
                );

            productSearch.addEventListener(
                "input",
                () => {
                    const needle =
                        normalizeText(
                            productSearch.value
                        );

                    productRows.forEach(
                        row => {
                            const haystack =
                                normalizeText(
                                    row.dataset
                                        .productSearch
                                );

                            row.hidden =
                                Boolean(needle)
                                && !haystack.includes(
                                    needle
                                );
                        }
                    );
                }
            );
        }
    }
);

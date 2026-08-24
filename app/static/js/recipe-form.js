document.addEventListener(
    "DOMContentLoaded",
    () => {
        const panel =
            document.getElementById(
                "recipe-ingredients-panel"
            );

        const rows =
            document.getElementById(
                "recipe-ingredient-rows"
            );

        const addButton =
            document.getElementById(
                "recipe-add-ingredient"
            );

        const template =
            document.getElementById(
                "recipe-ingredient-row-template"
            );

        const initialDataElement =
            document.getElementById(
                "recipe-initial-ingredients"
            );

        let initialIngredients = [];

        if (initialDataElement) {
            try {
                initialIngredients =
                    JSON.parse(
                        initialDataElement.textContent
                    );
            } catch (error) {
                console.error(
                    "Recipe ingredient preload "
                    + "failed:",
                    error
                );
            }
        }

        if (
            !panel
            || !rows
            || !addButton
            || !template
        ) {
            return;
        }

        const searchUrl =
            panel.dataset.searchUrl;

        const unitsUrl =
            panel.dataset.unitsUrl;

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

        const setupRow = row => {
            const ingredientId =
                row.querySelector(
                    ".js-recipe-ingredient-id"
                );

            const input =
                row.querySelector(
                    ".js-recipe-ingredient-name"
                );

            const results =
                row.querySelector(
                    ".js-recipe-ingredient-results"
                );

            const status =
                row.querySelector(
                    ".js-recipe-ingredient-status"
                );

            const unitSelect =
                row.querySelector(
                    ".js-recipe-ingredient-unit-select"
                );

            const unitText =
                row.querySelector(
                    ".js-recipe-ingredient-unit-text"
                );

            const removeButton =
                row.querySelector(
                    ".js-recipe-ingredient-remove"
                );

            let requestSerial = 0;

            const closeResults = () => {
                results.innerHTML = "";
                results.hidden = true;
            };

            const useFreeTextUnit = () => {
                unitSelect.hidden = true;
                unitSelect.value = "0";

                unitText.hidden = false;
            };

const loadIngredientUnits =
    async (
        ingredientIdValue,
        preferredUnitId = 0,
        preferredUnitText = ""
    ) => {
                    if (
                        !ingredientIdValue
                        || !unitsUrl
                    ) {
                        useFreeTextUnit();
                        return;
                    }

                    try {
                        const url =
                            new URL(
                                unitsUrl,
                                window.location.origin
                            );

                        url.searchParams.set(
                            "ingredient_id",
                            ingredientIdValue
                        );

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
                            useFreeTextUnit();
                            return;
                        }

                        const data =
                            await response.json();

                        unitSelect.innerHTML = "";

                        const emptyOption =
                            document.createElement(
                                "option"
                            );

                        emptyOption.value = "0";
                        emptyOption.textContent = "—";

                        unitSelect.appendChild(
                            emptyOption
                        );

                        (
                            data.units || []
                        ).forEach(
                            unit => {
                                const option =
                                    document.createElement(
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

if (
    data.units
    && data.units.length
) {

    const preferredValue =
        preferredUnitId
            ? String(
                preferredUnitId
            )
            : "";

    const preferredExists =
        preferredValue
        && Array.from(
            unitSelect.options
        ).some(
            option =>
                option.value
                === preferredValue
        );

if (preferredExists) {
    unitSelect.value =
        preferredValue;

    unitText.value = "";
    unitText.hidden = true;
    unitSelect.hidden = false;

} else if (
    preferredUnitText
) {
    unitSelect.value = "0";
    unitSelect.hidden = true;

    unitText.value =
        preferredUnitText;

    unitText.hidden = false;

} else if (
    data.default_unit_id
) {
    unitSelect.value =
        String(
            data.default_unit_id
        );
}
} else {
    useFreeTextUnit();
}
                    } catch (error) {
                        console.error(
                            "Recipe ingredient unit "
                            + "load failed:",
                            error
                        );

                        useFreeTextUnit();
                    }
                };

            const showFreeTextStatus = () => {
                if (!input.value.trim()) {
                    status.textContent = "";
                    return;
                }

                if (ingredientId.value) {
                    status.textContent =
                        "✓ Saját alapanyaghoz párosítva";
                } else {
                    status.textContent =
                        "Nincs párosítva — "
                        + "a megadott név ettől még "
                        + "elmenthető.";
                }
            };

            const chooseResult = item => {
                ingredientId.value =
                    String(item.id);

                input.value =
                    item.name;

                closeResults();

                loadIngredientUnits(
                    ingredientId.value
                );

                showFreeTextStatus();
            };

            const renderResults = items => {
                results.innerHTML = "";

                if (!items.length) {
                    results.hidden = true;
                    return;
                }

                items.forEach(
                    item => {
                        const button =
                            document.createElement(
                                "button"
                            );

                        button.type =
                            "button";

                        button.className =
                            "autocomplete-result";

                        button.textContent =
                            item.name;

                        button.addEventListener(
                            "mousedown",
                            event => {
                                event.preventDefault();

                                chooseResult(
                                    item
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

            const searchIngredients =
                async () => {
                    const query =
                        input.value.trim();

                    const serial =
                        ++requestSerial;

                    if (query.length < 2) {
                        closeResults();
                        showFreeTextStatus();
                        return;
                    }

                    try {
                        const url =
                            new URL(
                                searchUrl,
                                window.location.origin
                            );

                        url.searchParams.set(
                            "q",
                            query
                        );

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

                        if (
                            !response.ok
                            || serial
                                !== requestSerial
                        ) {
                            return;
                        }

                        const data =
                            await response.json();

                        renderResults(
                            data.results || []
                        );
                    } catch (error) {
                        console.error(
                            "Recipe ingredient "
                            + "search failed:",
                            error
                        );
                    }

                    showFreeTextStatus();
                };

            let searchTimer = null;

            input.addEventListener(
                "input",
                () => {
                    ingredientId.value = "";

                    useFreeTextUnit();

                    window.clearTimeout(
                        searchTimer
                    );

                    searchTimer =
                        window.setTimeout(
                            searchIngredients,
                            180
                        );

                    showFreeTextStatus();
                }
            );

            input.addEventListener(
                "focus",
                () => {
                    if (
                        input.value
                            .trim()
                            .length >= 2
                    ) {
                        searchIngredients();
                    }
                }
            );

            input.addEventListener(
                "blur",
                () => {
                    window.setTimeout(
                        () => {
                            closeResults();
                            showFreeTextStatus();
                        },
                        150
                    );
                }
            );

            removeButton.addEventListener(
                "click",
                () => {
                    row.remove();

                    if (
                        rows.children.length
                        === 0
                    ) {
                        addRow();
                    }
                }
            );

            useFreeTextUnit();

            return {
                loadIngredientUnits,
                useFreeTextUnit,
            };
        };

        const addRow = (
            initialData = null,
            shouldFocus = true
        ) => {
            const fragment =
                template.content
                    .cloneNode(true);

            const row =
                fragment.querySelector(
                    ".recipe-ingredient-row"
                );

            rows.appendChild(
                fragment
            );

            const rowApi =
                setupRow(
                    row
                );

            const ingredientId =
                row.querySelector(
                    ".js-recipe-ingredient-id"
                );

            const input =
                row.querySelector(
                    ".js-recipe-ingredient-name"
                );

            const quantity =
                row.querySelector(
                    ".js-recipe-ingredient-quantity"
                );

            const unitSelect =
                row.querySelector(
                    ".js-recipe-ingredient-unit-select"
                );

            const unitText =
                row.querySelector(
                    ".js-recipe-ingredient-unit-text"
                );

            if (initialData) {
                ingredientId.value =
                    initialData.ingredient_id
                        ? String(
                            initialData.ingredient_id
                        )
                        : "";

                input.value =
                    initialData.name || "";

                quantity.value =
                    initialData.quantity || "";

                unitText.value =
                    initialData.unit_text || "";

                if (
                    initialData.ingredient_id
                ) {
rowApi.loadIngredientUnits(
    String(
        initialData.ingredient_id
    ),
    initialData.unit_id || 0,
    initialData.unit_text || ""
);
                } else {
                    rowApi.useFreeTextUnit();
                }
            }

            if (shouldFocus) {
                input.focus();
            }
        };

        addButton.addEventListener(
            "click",
            () => {
                addRow();
            }
        );

        if (initialIngredients.length) {
            initialIngredients.forEach(
                ingredient => {
                    addRow(
                        ingredient,
                        false
                    );
                }
            );
        } else {
            addRow(
                null,
                false
            );
        }
    }
);

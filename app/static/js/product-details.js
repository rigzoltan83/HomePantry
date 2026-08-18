document.addEventListener(
    "DOMContentLoaded",
    () => {
        const i18n =
            window.productDetailsI18n
            || {};
        const modal =
            document.getElementById(
                "product-details-modal"
            );

        const title =
            document.getElementById(
                "product-details-title"
            );

        const subtitle =
            document.getElementById(
                "product-details-subtitle"
            );

        const content =
            document.getElementById(
                "product-details-content"
            );

        if (
            !modal
            || !title
            || !subtitle
            || !content
        ) {
            return;
        }


        const escapeHtml = value => {
            return String(
                value ?? ""
            )
                .replaceAll(
                    "&",
                    "&amp;"
                )
                .replaceAll(
                    "<",
                    "&lt;"
                )
                .replaceAll(
                    ">",
                    "&gt;"
                )
                .replaceAll(
                    '"',
                    "&quot;"
                )
                .replaceAll(
                    "'",
                    "&#039;"
                );
        };


        const formatTag = value => {
            const text =
                String(
                    value || ""
                );

            const separatorIndex =
                text.indexOf(":");

            const withoutLanguage =
                separatorIndex >= 0
                    ? text.slice(
                        separatorIndex + 1
                    )
                    : text;

            return withoutLanguage
                .replaceAll(
                    "-",
                    " "
                )
                .replaceAll(
                    "_",
                    " "
                );
        };


        const renderTagList = values => {
            if (
                !Array.isArray(values)
                || !values.length
            ) {
                return "—";
            }

            return values
                .map(
                    value => (
                        `<span class="product-detail-tag">`
                        + escapeHtml(
                            formatTag(value)
                        )
                        + `</span>`
                    )
                )
                .join("");
        };


        const getNutrient = (
            nutriments,
            key
        ) => {
            const value =
                nutriments[
                    `${key}_100g`
                ];

            const unit =
                nutriments[
                    `${key}_unit`
                ];

            if (
                value === undefined
                || value === null
                || value === ""
            ) {
                return null;
            }

            return {
                value,
                unit: unit || "",
            };
        };


        const renderNutritionRow = (
            label,
            nutrient
        ) => {
            if (!nutrient) {
                return "";
            }

            return `
                <tr>
                    <th>
                        ${escapeHtml(label)}
                    </th>

                    <td>
                        ${escapeHtml(
                            nutrient.value
                        )}
                        ${escapeHtml(
                            nutrient.unit
                        )}
                    </td>
                </tr>
            `;
        };


        const renderProductDetails =
            data => {
                const externalData =
                    data.external_data
                    || {};

                const nutriments =
                    externalData
                        .nutriments
                    || {};

const language =
    document.documentElement.lang
    || "hu";

const allergens =
    (
        externalData
            .allergens_display
        || {}
    )[language]
    || (
        externalData
            .allergens_display
        || {}
    ).en
    || externalData.allergens_tags
    || [];

const traces =
    (
        externalData
            .traces_display
        || {}
    )[language]
    || (
        externalData
            .traces_display
        || {}
    ).en
    || externalData.traces_tags
    || [];

const categories =
    (
        externalData
            .categories_display
        || {}
    )[language]
    || (
        externalData
            .categories_display
        || {}
    ).en
    || externalData.categories_tags
    || [];

const labels =
    (
        externalData
            .labels_display
        || {}
    )[language]
    || (
        externalData
            .labels_display
        || {}
    ).en
    || externalData.labels_tags
    || [];

                title.textContent =
                    data.name
                    || "—";

                subtitle.textContent =
                    [
                        data.brand,
                        data.generic_name,
                    ]
                        .filter(Boolean)
                        .join(" · ");


                const energyKj =
                    getNutrient(
                        nutriments,
                        "energy-kj"
                    );

                const energyKcal =
                    getNutrient(
                        nutriments,
                        "energy-kcal"
                    );

                const fat =
                    getNutrient(
                        nutriments,
                        "fat"
                    );

                const saturatedFat =
                    getNutrient(
                        nutriments,
                        "saturated-fat"
                    );

                const carbohydrates =
                    getNutrient(
                        nutriments,
                        "carbohydrates"
                    );

                const sugars =
                    getNutrient(
                        nutriments,
                        "sugars"
                    );

                const proteins =
                    getNutrient(
                        nutriments,
                        "proteins"
                    );

                const salt =
                    getNutrient(
                        nutriments,
                        "salt"
                    );


                content.innerHTML = `
                    <section class="product-detail-section">

<h3>
    ${escapeHtml(
        i18n.ingredients
        || "Ingredients"
    )}
</h3>

                        <p class="product-detail-text">
                            ${
                                data.ingredients_text
                                    ? escapeHtml(
                                        data.ingredients_text
                                    )
                                    : "—"
                            }
                        </p>

                    </section>


                    <section class="product-detail-section">

<h3>
    ${escapeHtml(
        i18n.allergens
        || "Allergens"
    )}
</h3>

                        <div class="product-detail-tags">
                            ${renderTagList(
                                allergens
                            )}
                        </div>

                    </section>


                    <section class="product-detail-section">

<h3>
    ${escapeHtml(
        i18n.traces
        || "May contain traces of"
    )}
</h3>

                        <div class="product-detail-tags">
                            ${renderTagList(
                                traces
                            )}
                        </div>

                    </section>


                    <section class="product-detail-section">

<h3>
    ${escapeHtml(
        i18n.categories
        || "Categories"
    )}
</h3>

                        <div class="product-detail-tags">
                            ${renderTagList(
                                categories
                            )}
                        </div>

                    </section>


                    <section class="product-detail-section">

<h3>
    ${escapeHtml(
        i18n.labels
        || "Labels"
    )}
</h3>

                        <div class="product-detail-tags">
                            ${renderTagList(
                                labels
                            )}
                        </div>

                    </section>


                    <section class="product-detail-section">

<h3>
    Tápérték 100 g-ban
</h3>

                        <div class="inventory-table-wrap">
                            <table class="inventory-table product-nutrition-table">
                                <tbody>

${renderNutritionRow(
    "Energia",
    energyKj
)}

${renderNutritionRow(
    i18n.energy
        || "Energy",
    energyKcal
)}

${renderNutritionRow(
    i18n.fat
        || "Fat",
    fat
)}

${renderNutritionRow(
    i18n.saturatedFat
        || "of which saturates",
    saturatedFat
)}

${renderNutritionRow(
    i18n.carbohydrates
        || "Carbohydrate",
    carbohydrates
)}

${renderNutritionRow(
    i18n.sugars
        || "of which sugars",
    sugars
)}

${renderNutritionRow(
    i18n.proteins
        || "Protein",
    proteins
)}

${renderNutritionRow(
    i18n.salt
        || "Salt",
    salt
)}

                                </tbody>
                            </table>
                        </div>

                    </section>
                `;
            };


        const openModal =
            async button => {
                const url =
                    button.dataset
                        .detailsUrl;

                if (!url) {
                    return;
                }

                modal.hidden =
                    false;

title.textContent =
    i18n.details
    || "Details";

                subtitle.textContent =
                    "";

content.innerHTML =
    `<p class="muted">
        ${escapeHtml(
            i18n.loading
            || "Loading details..."
        )}
    </p>`;

                document.body.classList.add(
                    "modal-open"
                );

                try {
                    const response =
                        await fetch(
                            url,
                            {
                                headers: {
                                    "Accept":
                                        "application/json",
                                },
                            }
                        );

                    if (!response.ok) {
                        throw new Error(
                            `HTTP ${response.status}`
                        );
                    }

                    const data =
                        await response.json();

                    renderProductDetails(
                        data
                    );

                } catch (error) {
                    console.error(
                        "Product details load failed:",
                        error
                    );

content.innerHTML =
    `<p class="field-error">
        ${escapeHtml(
            i18n.loadError
            || "Failed to load product details."
        )}
    </p>`;
                }
            };


        const closeModal = () => {
            modal.hidden =
                true;

            document.body.classList.remove(
                "modal-open"
            );
        };


        document
            .querySelectorAll(
                ".js-product-details-button"
            )
            .forEach(
                button => {
                    button.addEventListener(
                        "click",
                        () => {
                            openModal(
                                button
                            );
                        }
                    );
                }
            );


        modal
            .querySelectorAll(
                "[data-product-details-close]"
            )
            .forEach(
                element => {
                    element.addEventListener(
                        "click",
                        closeModal
                    );
                }
            );


        document.addEventListener(
            "keydown",
            event => {
                if (
                    event.key === "Escape"
                    && !modal.hidden
                ) {
                    closeModal();
                }
            }
        );
    }
);

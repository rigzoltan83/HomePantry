document.addEventListener(
    "DOMContentLoaded",
    () => {
        if (
            typeof window.Quagga
            === "undefined"
        ) {
            console.error(
                "Quagga2 is not loaded."
            );

            return;
        }

        const Quagga =
            window.Quagga;

        let scannerRunning = false;

        const formatMap = {
            ean_13: "ean13",
            ean_8: "ean8",
            upc_a: "upca",
            upc_e: "upce",
            code_128: "code128",
        };

        const stopScanner = (
            scanner,
            wrapper
        ) => {
            if (scannerRunning) {
                Quagga.stop();
                Quagga.offDetected();

                scannerRunning = false;
            }

            scanner.innerHTML = "";

            if (wrapper) {
                wrapper.hidden = true;
            }
        };

        const startScanner = (
            scanner,
            wrapper,
            onCode
        ) => {
            if (scannerRunning) {
                stopScanner(
                    scanner,
                    wrapper
                );

                return;
            }

            wrapper.hidden = false;

            Quagga.init(
                {
                    inputStream: {
                        type: "LiveStream",
                        target: scanner,
                        constraints: {
                            facingMode:
                                "environment",
                        },
                    },

                    locate: true,

                    frequency: 10,

                    decoder: {
                        readers: [
                            "ean_reader",
                            "ean_8_reader",
                            "upc_reader",
                            "upc_e_reader",
                            "code_128_reader",
                        ],
                    },
                },

                error => {
                    if (error) {
                        console.error(
                            error
                        );

                        wrapper.hidden = true;
                        scannerRunning = false;

                        return;
                    }

                    scannerRunning = true;

                    Quagga.start();

                    Quagga.onDetected(
                        result => {
                            const code =
                                result
                                    ?.codeResult
                                    ?.code;

                            const format =
                                result
                                    ?.codeResult
                                    ?.format;

                            if (!code) {
                                return;
                            }

                            stopScanner(
                                scanner,
                                wrapper
                            );

                            onCode(
                                code,
                                format
                            );
                        }
                    );
                }
            );
        };

        const syncAutocomplete = (
            select,
            value
        ) => {
            select.value =
                String(value);

            const wrapper =
                select.closest(
                    ".autocomplete-select"
                );

            if (wrapper) {
                const input =
                    wrapper.querySelector(
                        ".js-autocomplete-input"
                    );

                const option =
                    Array.from(
                        select.options
                    ).find(
                        item =>
                            item.value
                            === String(value)
                    );

                if (
                    input
                    && option
                ) {
                    input.value =
                        option.textContent
                            .trim();
                }
            }

            select.dispatchEvent(
                new Event(
                    "change",
                    {
                        bubbles: true,
                    }
                )
            );
        };

        const selectOptionWhenAvailable = (
            select,
            value
        ) => {
            if (
                !select
                || !value
            ) {
                return;
            }

            const wantedValue =
                String(value);

            const setValue = () => {
                const exists =
                    Array.from(
                        select.options
                    ).some(
                        option =>
                            option.value
                            === wantedValue
                    );

                if (!exists) {
                    return false;
                }

                select.value =
                    wantedValue;

                select.dispatchEvent(
                    new Event(
                        "change",
                        {
                            bubbles: true,
                        }
                    )
                );

                return true;
            };

            if (setValue()) {
                return;
            }

            const observer =
                new MutationObserver(
                    () => {
                        if (setValue()) {
                            observer.disconnect();
                        }
                    }
                );

            observer.observe(
                select,
                {
                    childList: true,
                }
            );

            window.setTimeout(
                () => {
                    observer.disconnect();
                },
                3000
            );
        };

        const lookupContainer =
            document.querySelector(
                ".barcode-lookup"
            );

        if (lookupContainer) {
            const barcodeInput =
                lookupContainer
                    .querySelector(
                        ".js-barcode-lookup-input"
                    );

            const lookupButton =
                lookupContainer
                    .querySelector(
                        ".js-barcode-lookup-button"
                    );

            const scanButton =
                lookupContainer
                    .querySelector(
                        ".js-barcode-scan-button"
                    );

            const status =
                lookupContainer
                    .querySelector(
                        ".js-barcode-status"
                    );

            const scanner =
                lookupContainer
                    .querySelector(
                        ".js-barcode-scanner"
                    );

            const scannerWrapper =
                lookupContainer
                    .querySelector(
                        ".js-barcode-scanner-wrap"
                    );

            const closeButton =
                lookupContainer
                    .querySelector(
                        ".js-barcode-close-button"
                    );

            const newProductPanel =
                document.querySelector(
                    ".js-barcode-new-product"
                );

            const lookupUrl =
                lookupContainer.dataset
                    .lookupUrl;

            const lookupBarcode =
                async () => {
                    const barcode =
                        barcodeInput.value
                            .trim();

                    if (!barcode) {
                        return;
                    }

                    const url =
                        new URL(
                            lookupUrl,
                            window.location.origin
                        );

                    url.searchParams.set(
                        "barcode",
                        barcode
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
                        status.textContent =
                            "Lookup failed.";

                        return;
                    }

                    const data =
                        await response.json();

                    if (
                        !data.found
                        || !data.product
                    ) {
                        status.textContent =
                            "No product found.";

                        if (newProductPanel) {
                            newProductPanel.hidden =
                                false;
                        }

                        const productSelect =
                            document.getElementById(
                                "product_id"
                            );

                        if (productSelect) {
                            productSelect.value = "0";

                            const wrapper =
                                productSelect.closest(
                                    ".autocomplete-select"
                                );

                            const input =
                                wrapper
                                    ?.querySelector(
                                        ".js-autocomplete-input"
                                    );

                            if (input) {
                                input.value = "";
                            }
                        }

                        return;
                    }

                    const product =
                        data.product;

                    if (newProductPanel) {
                        newProductPanel.hidden =
                            true;
                    }

                    const productSelect =
                        document.getElementById(
                            "product_id"
                        );

                    const ingredientSelect =
                        document.getElementById(
                            "ingredient_id"
                        );

                    const quantityInput =
                        document.getElementById(
                            "quantity"
                        );

                    const unitSelect =
                        document.getElementById(
                            "unit_id"
                        );

                    if (productSelect) {
                        syncAutocomplete(
                            productSelect,
                            product.id
                        );
                    }

                    if (ingredientSelect) {
                        syncAutocomplete(
                            ingredientSelect,
                            product.ingredient_id
                        );
                    }

                    if (
                        quantityInput
                        && product.package_quantity
                        !== null
                    ) {
                        quantityInput.value =
                            product.package_quantity;
                    }

                    if (
                        unitSelect
                        && product.package_unit_id
                    ) {
                        selectOptionWhenAvailable(
                            unitSelect,
                            product.package_unit_id
                        );
                    }

                    const productLabel =
                        [
                            product.brand,
                            product.name,
                        ]
                            .filter(Boolean)
                            .join(" — ");

                    const packageLabel =
                        (
                            product.package_quantity
                            && product.package_unit_symbol
                        )
                            ? (
                                product.package_quantity
                                + " "
                                + product.package_unit_symbol
                            )
                            : "";

                    status.textContent =
                        [
                            productLabel,
                            packageLabel,
                        ]
                            .filter(Boolean)
                            .join(" · ");
                };

            lookupButton.addEventListener(
                "click",
                lookupBarcode
            );

            barcodeInput.addEventListener(
                "keydown",
                event => {
                    if (
                        event.key === "Enter"
                    ) {
                        event.preventDefault();

                        lookupBarcode();
                    }
                }
            );

            scanButton.addEventListener(
                "click",
                () => {
                    startScanner(
                        scanner,
                        scannerWrapper,
                        code => {
                            barcodeInput.value =
                                code;

                            lookupBarcode();
                        }
                    );
                }
            );

            closeButton.addEventListener(
                "click",
                () => {
                    stopScanner(
                        scanner,
                        scannerWrapper
                    );
                }
            );

        }

        const productScanButton =
            document.querySelector(
                ".js-product-scan-button"
            );

        if (productScanButton) {
            const input =
                document.querySelector(
                    ".js-product-barcode-input"
                );

            const scanner =
                document.querySelector(
                    ".js-product-barcode-scanner"
                );

            const scannerWrapper =
                document.querySelector(
                    ".js-product-barcode-scanner-wrap"
                );

            const closeButton =
                document.querySelector(
                    ".js-product-barcode-close-button"
                );

            const barcodeType =
                document.getElementById(
                    "barcode_type"
                );

            productScanButton.addEventListener(
                "click",
                () => {
                    startScanner(
                        scanner,
                        scannerWrapper,
                        (
                            code,
                            format
                        ) => {
                            input.value =
                                code;

                            if (
                                barcodeType
                                && formatMap[
                                    format
                                ]
                            ) {
                                barcodeType.value =
                                    formatMap[
                                        format
                                    ];
                            }
                        }
                    );
                }
            );
            closeButton.addEventListener(
                "click",
                () => {
                    stopScanner(
                        scanner,
                        scannerWrapper
                    );
                }
            );
        }
    }
);

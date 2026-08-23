document.addEventListener(
    "DOMContentLoaded",
    () => {
        const lightbox =
            document.getElementById(
                "storage-image-lightbox"
            );

        if (!lightbox) {
            return;
        }

        const image =
            document.getElementById(
                "storage-image-lightbox-image"
            );

        const closeButton =
            lightbox.querySelector(
                ".storage-image-lightbox-close"
            );

        const openButtons =
            document.querySelectorAll(
                "[data-storage-image-open]"
            );


        function closeLightbox() {
            lightbox.hidden = true;

            image.src = "";
            image.alt = "";

            document.body.classList.remove(
                "storage-lightbox-open"
            );
        }


        openButtons.forEach(
            button => {
                button.addEventListener(
                    "click",
                    () => {
                        image.src =
                            button.dataset
                                .imageSrc;

                        image.alt =
                            button.dataset
                                .imageAlt
                            || "";

                        lightbox.hidden = false;

                        document.body.classList.add(
                            "storage-lightbox-open"
                        );
                    }
                );
            }
        );


        closeButton.addEventListener(
            "click",
            closeLightbox
        );


        lightbox.addEventListener(
            "click",
            event => {
                if (
                    event.target
                    === lightbox
                ) {
                    closeLightbox();
                }
            }
        );


        document.addEventListener(
            "keydown",
            event => {
                if (
                    event.key === "Escape"
                    && !lightbox.hidden
                ) {
                    closeLightbox();
                }
            }
        );
    }
);

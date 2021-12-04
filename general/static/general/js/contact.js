src="https://unpkg.com/material-components-web@latest/dist/material-components-web.min.js"
src="https://cdn.jsdelivr.net/npm/simple-parallax-js@5.6.1/dist/simpleParallax.min.js"
new mdc.textField.MDCTextField(document.querySelector(".text-field-fill-leading-custom .mdc-text-field"));
window.addEventListener("load", function () {
                var image = document.querySelectorAll(".cuny");
                new simpleParallax(image, {
                  orientation: "left",
                  scale: 1.2,
                  overflow: false,
                  delay: 0.4,
                  transition: "none",
                });
              });

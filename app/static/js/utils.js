let getWindowSize = (function() {
    let docEl = document.documentElement, IS_BODY_ACTING_ROOT = docEl && docEl.clientHeight === 0;

    function isDocumentElementHeightOff () {
        let d = document, div = d.createElement('div');
        div.style.height = "2500px";
        d.body.insertBefore(div, d.body.firstChild);
        let r = d.documentElement.clientHeight > 2400;
        d.body.removeChild(div);
        return r;
    }

    if (typeof document.clientWidth == "number") {
         return function () {
            return { width: document.clientWidth, height: document.clientHeight };
         };
    } else if (IS_BODY_ACTING_ROOT || isDocumentElementHeightOff()) {
        let b = document.body;
            return function () {return { width: b.clientWidth, height: b.clientHeight };
        };
    } else {
        return function () {
            return { width: docEl.clientWidth, height: docEl.clientHeight };
        };
    }
})();

function num2str(num) {
    if (Number.isInteger(num)) {
        return num + ".0"
    } else {
        return num.toString();
    }
}

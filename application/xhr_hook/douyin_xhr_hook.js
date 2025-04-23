(function() {
    const OriginalXHR = window.XMLHttpRequest;
    window.XMLHttpRequest = function() {
        const xhr = new OriginalXHR();
        xhr.addEventListener('load', function() {

            if (
                xhr.url.includes("/aweme/v1/web/aweme/detail/") ||
                xhr.url.includes("/aweme/v1/web/aweme/feed/")
            ){
                console.log(xhr.url)
                console.log(xhr.response)
            }

        });
        return xhr;
    };
})();
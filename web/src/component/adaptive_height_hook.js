import {useLayoutEffect, useState} from "react";


const AdaptiveHeight = (offset = 150) => {
    const [height, setHeight] = useState(() => {
        const content = document.getElementById("layout-content");
        return content ? content.clientHeight - offset : 500;
    });

    useLayoutEffect(() => {
        const handleResize = () => {
            const content = document.getElementById("layout-content");
            if (content) {
                setHeight(content.clientHeight - offset);
            }
        };

        window.addEventListener('resize', handleResize);
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, [offset]);

    return height;
};

export default AdaptiveHeight
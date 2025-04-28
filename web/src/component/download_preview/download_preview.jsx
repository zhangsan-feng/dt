
import ReactPlayer from 'react-player';
import {Col, Image, Row} from 'antd';
import './download_preview.css'
import {FilePreviewApi} from '../../api/api'
import {useState, useEffect, useRef, useCallback, useLayoutEffect} from 'react'
import Masonry from "react-masonry-css";
import videojs from 'video.js';
import 'video.js/dist/video-js.css';


const LazyVideoPlayer1 = ({ url }) => {
    const [isVisible, setIsVisible] = useState(false);
    const [shouldLoad, setShouldLoad] = useState(false); // 延迟加载元数据
    const ref = useRef();

    useEffect(() => {
        const currentRef = ref.current; // 保存引用，避免闭包问题
        if (!currentRef) return;

        const observer = new IntersectionObserver(
            ([entry]) => {
                if (entry.isIntersecting) {
                    setIsVisible(true);
                    const loadTimer = setTimeout(() => {
                        setShouldLoad(true);
                        observer.unobserve(currentRef); // 加载后停止观察
                    }, 300);

                    return () => clearTimeout(loadTimer); // 清理定时器
                }
            },
            { rootMargin: '200px' }
        );

        observer.observe(currentRef);

        return () => {
            observer.unobserve(currentRef);
            observer.disconnect();
        };
    }, []);

    return (
        <div ref={ref} style={{ width: '100%', height: '100%', minHeight: '200px' }}>

            {isVisible ? (
                <ReactPlayer url={url} controls={true} width="100%" height="100%" playing={false}
                             config={{file: {attributes: {preload: 'metadata'}}}}/>
            ) : (
                <div style={{backgroundColor: '#f0f0f0', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                    Loading...
                </div>
            )}
        </div>
    );
};


const DownloadPreview = ()=>{
    const [data, setData] = useState([]);
    const [page, setPage] = useState(1);
    const containerRef = useRef(null);
    const [hasMore, setHasMore] = useState(true);
    const debounceTimer = useRef(null);

    const [tableHeight, setTableHeight] = useState(() => {
        const content = document.getElementById("layout-content");
        return content ? content.clientHeight - 100 : 500;
    });
    useLayoutEffect(() => {
        const handleResize = () => {
            const content = document.getElementById("layout-content");
            if (content) {setTableHeight(content.clientHeight -100);}
        };
        window.addEventListener('resize', handleResize);
        return () => {window.removeEventListener('resize', handleResize);};
    }, []);


    const loadMoreData = ()=>{
        if (!hasMore){return}
        FilePreviewApi({ page })
            .then((res) => {
                setData((prevData) => [...prevData, ...res.data]);
                setPage((prevPage) => prevPage + 1);
                if (res.data.length === 0) {setHasMore(false);}
            })
    }

    useEffect(() => {loadMoreData()}, []);

    useEffect(() => {
        const container = containerRef.current;
        if (!container) return;

        const handleScroll = () => {
            if (debounceTimer.current) {clearTimeout(debounceTimer.current);}
            debounceTimer.current = setTimeout(() => {
                const { scrollTop, scrollHeight, clientHeight } = container;
                const isAtBottom = scrollHeight - scrollTop <= clientHeight + 50;
                console.log(scrollHeight - scrollTop, clientHeight);
                if (isAtBottom) {loadMoreData();}
            }, 500);
        };

        container.addEventListener("scroll", handleScroll);
        container.addEventListener("wheel", handleScroll);
        return () => {
            container.removeEventListener("scroll", handleScroll);
            container.removeEventListener("wheel", handleScroll);
            if (debounceTimer.current) {
                clearTimeout(debounceTimer.current);
            }
        };
    }, [loadMoreData]);

    const [renderIndex, setRenderIndex] = useState(0);
    const batchSize = 10;
    const delay = 200;

    useEffect(() => {
        if (renderIndex >= data.length) return;
        const timer = setTimeout(() => {
            requestAnimationFrame(() => {
                setRenderIndex(prev => Math.min(prev + batchSize, data.length));
            });
        }, delay);
        return () => clearTimeout(timer);
    }, [renderIndex, data.length]);

    const breakpointColumnsObj = {
        default: 7,
        1920:7,
        1600:6,
        1300:5,
        1000:4,
        700:3,
        500:2,
        300:1
    };

    return (

        <div className="preview-container"  ref={containerRef} style={{height:tableHeight}}>
            <Masonry
                breakpointCols={breakpointColumnsObj}
                className="my-masonry-grid"
                columnClassName="my-masonry-grid_column"
            >
                    {
                        data.slice(0, renderIndex).map((items, index) => {
                            if (items.includes(".png")) {
                                return (
                                    <div key={index}>
                                        <Image src={items} loading="lazy" />
                                    </div>
                                );
                            }
                            if (items.includes(".mp4")) {
                                return (
                                    <div key={index}>
                                        <LazyVideoPlayer1 url={items} />
                                    </div>
                                );
                            }
                        })
                    }
            </Masonry>
        </div>
    )
}


export default DownloadPreview
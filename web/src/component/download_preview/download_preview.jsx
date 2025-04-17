
import ReactPlayer from 'react-player';
import {Col, Image, Row} from 'antd';
import './download_preview.css'
import {FilePreviewApi} from '../../api/api'
import {useState, useEffect, useRef, useCallback, useLayoutEffect} from 'react'

import videojs from 'video.js';
import 'video.js/dist/video-js.css';


const LazyVideoPlayer1 = ({ url }) => {
    const [isVisible, setIsVisible] = useState(false);
    const [shouldLoad, setShouldLoad] = useState(false); // 延迟加载元数据
    const ref = useRef();

    useEffect(() => {
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (entry.isIntersecting) {
                    setIsVisible(true);
                    setTimeout(() => setShouldLoad(true), 300); // 延迟300ms再加载元数据
                    observer.unobserve(ref.current);
                }
            },
            { rootMargin: '200px' } // 提前200px触发观察
        );
        if (ref.current) observer.observe(ref.current);
        return () => {
            if (ref.current) observer.unobserve(ref.current);
        };
    }, []);

    return (
        <div ref={ref} style={{ width: '100%', height: '100%', minHeight: '200px' }}>

            {isVisible ? (
                <ReactPlayer url={url} controls={true} width="100%" height="100%" playing={false}
                             config={{file: {attributes: {preload: 'metadata'}}}}
                />
            ) : (
                <div style={{backgroundColor: '#f0f0f0', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                    Loading...
                </div>
            )}
        </div>
    );
};


const LazyVideoPlayer2 = ({ url, poster }) => {
    const [isVisible, setIsVisible] = useState(false);
    const videoRef = useRef(null);
    const playerRef = useRef(null);
    const containerRef = useRef(null);

    // 初始化 Video.js 播放器
    useEffect(() => {
        if (!isVisible) return;

        const videoElement = videoRef.current;
        if (!videoElement) return;

        const player = playerRef.current = videojs(videoElement, {
            controls: true,
            autoplay: false,
            preload: 'auto',
            fluid: true,
            sources: [{
                src: url,
                type: 'video/mp4'
            }],
            poster: poster // 使用传入的封面图
        });

        return () => {
            if (playerRef.current) {
                playerRef.current.dispose();
                playerRef.current = null;
            }
        };
    }, [isVisible, url, poster]);

    // 懒加载逻辑
    useEffect(() => {
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (entry.isIntersecting) {
                    setIsVisible(true);
                    observer.unobserve(containerRef.current);
                }
            },
            { rootMargin: '100px', threshold: 0.01 }
        );

        const currentRef = containerRef.current;
        if (currentRef) observer.observe(currentRef);

        return () => {
            if (currentRef) observer.unobserve(currentRef);
        };
    }, []);

    return (
        <div
            ref={containerRef}
            style={{
                width: '100%',
                height: '100%',
                minHeight: '200px',
                position: 'relative',
                backgroundColor: '#f0f0f0'
            }}
        >
            {isVisible ? (
                <div data-vjs-player>
                    <video
                        ref={videoRef}
                        className="video-js vjs-big-play-centered"
                        playsInline
                    />
                </div>
            ) : (
                <div style={{
                    width: '100%',
                    height: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                }}>
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
    const [isLoading, setIsLoading] = useState(false);
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


    const loadMoreData = useCallback(() => {
        if (!hasMore || isLoading) return;
        setIsLoading(true);
        FilePreviewApi({ page })
            .then((res) => {
                setData((prevData) => [...prevData, ...res.data]);
                setPage((prevPage) => prevPage + 1);
                if (res.data.length === 0) {
                    setHasMore(false);
                }
            }).finally(() => {setIsLoading(false); setHasMore(false)});
    }, [hasMore, isLoading, page]);
    useEffect(() => {if (data.length === 0) {loadMoreData();}}, [data.length, loadMoreData]);
    useEffect(() => {
        const container = containerRef.current;
        if (!container) return;

        const handleScroll = () => {
            if (debounceTimer.current) {clearTimeout(debounceTimer.current);}
            debounceTimer.current = setTimeout(() => {
                const { scrollTop, scrollHeight, clientHeight } = container;
                const isAtBottom = scrollHeight - scrollTop <= clientHeight + 10;
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

    return (
        <div className="preview-container"  ref={containerRef} style={{height:tableHeight}}>
            <div className="container-box">
                <div className="box-resource">
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
                </div>
            </div>
        </div>
    )
}


export default DownloadPreview
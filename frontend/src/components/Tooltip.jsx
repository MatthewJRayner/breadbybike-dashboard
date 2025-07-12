import React, { useState, useRef } from 'react';

const Tooltip = ({ children, content, position = 'top' }) => {
    const [isVisible, setIsVisible] = useState(false);
    const [tooltipStyle, setTooltipStyle] = useState({ top: 0, left: 0});
    const tooltipRef = useRef(null);
    const triggerRef = useRef(null);

    const handleMouseMove = (e) => {
        if (tooltipRef.current && triggerRef.current) {
            const triggerRect = triggerRef.current.getBoundingClientRect();
            const tooltipRect = tooltipRef.current.getBoundingClientRect();
            let top = e.clientY + 10;
            let left = e.clientX + 10;

            switch (position) {
                case 'top':
                    top = e.clientY - tooltipRect.height - 10;
                    left = e.clientX - tooltipRect.width / 2 + triggerRect.width / 2;
                    break;
                case 'bottom':
                    top = e.clientY + 10;
                    left = e.clientX - tooltipRect.width / 2 + triggerRect.width / 2;
                    break;
                case 'left':
                    top = e.clientY - tooltipRect.height / 2 + triggerRect.height / 2;
                    left = e.clientX - tooltipRect.width - 10;
                    break;
                case 'right':
                    top = e.clientY - tooltipRect.height / 2 + triggerRect.height / 2;
                    left = e.clientX + 10;
                    break;
                default:
                    break;
            }

            const viewportWidth = window.innerWidth;
            const viewportHeight = window.innerHeight;
            left = Math.max(0, Math.min(left, viewportWidth - tooltipRect.width));
            top = Math.max(0, Math.min(top, viewportHeight - tooltipRect.height))

            setTooltipStyle({ top, left })
        }
    };

    const handleMouseEnter = () => setIsVisible(true);
    const handleMouseLeave = () => setIsVisible(false);

    return (
        <div
            ref={triggerRef}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
            onMouseMove={handleMouseMove}
            style={{ position: 'relative', display: 'inline-block' }}
        >
            {children}
            {isVisible && (
                <div
                    ref={tooltipRef}
                    className='tooltip'
                    style={{ position: 'fixed', ...tooltipStyle, zIndex: 1000 }}
                >
                    {content}
                </div>
            )}
        </div>
    );
};

export default Tooltip

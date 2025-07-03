import React, { useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

/**
 * @param {Object} props
 * @param {Array<{time: string, value: number, label: string}>} props.data
 * @param {string} [props.title]
 * @param {string} [props.caption]
 * @param {string} [props.id]
 */
export default function TimeSeriesTimeline({ data, title, caption, id }) {
    const [hoveredIndex, setHoveredIndex] = useState(0);

    const handleChartMouseMove = (state) => {
        if (!state?.activeTooltipIndex) return;
        setHoveredIndex(Number(state.activeTooltipIndex));
    };

    return (
        <figure id={id || undefined}>
            {title && (
                <figcaption style={{ textAlign: "center", fontWeight: 600, marginBottom: "0.5rem" }}>{title}</figcaption>
            )}
            <div
                className="ts-timeline-chart-container"
                style={{
                    display: "flex",
                    gap: "2rem",
                    alignItems: "center",
                    flexDirection: "row",
                    justifyContent: "center",
                }}
            >
                <ul
                    style={{ listStyle: "none", padding: 0 }}
                >
                    {data.map((step, idx) => (
                        <li
                            key={step.time}
                            onMouseMove={() => setHoveredIndex(idx)}
                            style={{
                                display: 'flex',
                                alignItems: 'center',
                                padding: "0.5rem 1rem",
                                margin: "0.5rem 0",
                                background: hoveredIndex === idx ? "#e0e7ff" : "transparent",
                                borderRadius: "6px",
                                cursor: "pointer",
                                fontWeight: 500,
                                transition: 'background 0.15s',
                                minWidth: 160,
                                maxWidth: 220,
                            }}
                        >
                            {/* Highlight dot */}
                            <span
                                style={{
                                    display: 'inline-block',
                                    width: 12,
                                    height: 12,
                                    borderRadius: '50%',
                                    marginRight: 12,
                                    background: hoveredIndex === idx ? '#6366f1' : '#d1d5db',
                                    border: hoveredIndex === idx ? '2px solid #6366f1' : '2px solid #d1d5db',
                                    transition: 'background 0.15s, border 0.15s',
                                }}
                            />
                            <div>
                                <div>{step.time}</div>
                                <div>{step.label}</div>
                            </div>
                        </li>
                    ))}
                </ul>
                <ResponsiveContainer width="95%" height={200}>
                    <LineChart
                        data={data}
                        onMouseMove={handleChartMouseMove}
                        margin={{ right: 24, left: 0, top: 0, bottom: 0 }}
                    >
                        <XAxis dataKey="time" />
                        <YAxis />
                        <Line
                            type="monotone"
                            dataKey="value"
                            stroke="#8884d8"
                            activeDot={{ r: 8, stroke: '#fff', strokeWidth: 2, fill: '#6366f1' }}
                            dot={(props) => {
                                const { cx, cy, index } = props;
                                return (
                                    <circle
                                        cx={cx}
                                        cy={cy}
                                        r={hoveredIndex === index ? 8 : 5}
                                        fill={hoveredIndex === index ? "#6366f1" : "#8884d8"}
                                        stroke="#fff"
                                        strokeWidth={hoveredIndex === index ? 2 : 1}
                                        style={{ transition: 'all 0.15s' }}
                                    />
                                );
                            }}
                        />
                    </LineChart>
                </ResponsiveContainer>
                {/* Responsive styles for stacking on small screens */}
                <style>{`
                @media (max-width: 600px) {
                    .ts-timeline-chart-container {
                        flex-direction: column !important;
                        align-items: center !important;
                        justify-content: center !important;
                    }
                }
            `}</style>
            </div>
            {caption && (
                <figcaption style={{ textAlign: "center", marginTop: "1rem" }}>{caption}</figcaption>
            )}
        </figure>
    );
}
import type { HTMLAttributes, ReactNode } from "react";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
    children: ReactNode;
}

export default function Card({
    children,
    className = "",
    ...card_props
}: CardProps) {
    return (
        <div
            className={`clearvote-card ${className}`.trim()}
            {...card_props}
        >
            {children}
        </div>
    );
}
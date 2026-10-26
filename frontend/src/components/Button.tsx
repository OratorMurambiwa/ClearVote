import type { ButtonHTMLAttributes, ReactNode } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    children: ReactNode;
    variant?: "primary" | "secondary";
}

export default function Button({
    children,
    variant = "primary",
    className = "",
    ...button_props
}: ButtonProps) {
    const button_class =
        variant === "primary"
            ? "clearvote-button clearvote-button-primary"
            : "clearvote-button clearvote-button-secondary";

    return (
        <button
            className={`${button_class} ${className}`.trim()}
            {...button_props}
        >
            {children}
        </button>
    );
}
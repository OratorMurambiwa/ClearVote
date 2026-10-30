type StatusType = "warning" | "success" | "error" | "neutral";

interface StatusBadgeProps {
    label: string;
    status?: StatusType;
}

export default function StatusBadge({
    label,
    status = "neutral",
}: StatusBadgeProps) {
    return (
        <span
            className={`clearvote-status-badge clearvote-status-${status}`}
        >
            {label}
        </span>
    );
}
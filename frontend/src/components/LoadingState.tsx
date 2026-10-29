interface LoadingStateProps {
    message?: string;
}

export default function LoadingState({
    message = "Analyzing evidence...",
}: LoadingStateProps) {
    return (
        <div
            className="clearvote-state"
            role="status"
            aria-live="polite"
        >
            <div
                className="clearvote-spinner"
                aria-hidden="true"
            />

            <p>{message}</p>
        </div>
    );
}
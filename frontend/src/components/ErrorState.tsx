import Button from "./Button";

interface ErrorStateProps {
    title?: string;
    message: string;
    on_retry?: () => void;
}

export default function ErrorState({
    title = "Something went wrong",
    message,
    on_retry,
}: ErrorStateProps) {
    return (
        <div
            className="clearvote-state clearvote-error-state"
            role="alert"
        >
            <h3>{title}</h3>
            <p>{message}</p>

            {on_retry && (
                <Button onClick={on_retry}>
                    Try Again
                </Button>
            )}
        </div>
    );
}
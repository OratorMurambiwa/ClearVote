import {
    Button,
    Card,
    ErrorState,
    LoadingState,
    SourceCard,
    StatusBadge,
} from "./components";


export default function App() {
    return (
        <main style={{ padding: "32px", display: "grid", gap: "24px" }}>
            <StatusBadge label="Needs review" status="warning" />

            <Button>Learn More</Button>

            <Card style={{ padding: "20px" }}>
                <h2>ClearVote Card</h2>
                <p className="clearvote-muted">
                    Shared card component preview.
                </p>
            </Card>

            <SourceCard
                title="Related fact check"
                publisher="Example Publisher"
                published_date="Oct. 2026"
                summary="Example evidence summary for the ClearVote design system."
                url="https://example.com"
            />

            <LoadingState />

            <ErrorState
                message="ClearVote could not complete the analysis."
                on_retry={() => console.log("Retry")}
            />
        </main>
    );
}
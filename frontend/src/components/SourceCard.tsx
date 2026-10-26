interface SourceCardProps {
    title: string;
    publisher: string;
    summary: string;
    url?: string;
    published_date?: string;
}

export default function SourceCard({
    title,
    publisher,
    summary,
    url,
    published_date,
}: SourceCardProps) {
    return (
        <article className="clearvote-source-card">
            <h3 className="clearvote-source-title">{title}</h3>

            <p className="clearvote-source-meta">
                {publisher}
                {published_date ? ` • ${published_date}` : ""}
            </p>

            <p className="clearvote-source-summary">{summary}</p>

            {url && (
                <a
                    className="clearvote-source-link"
                    href={url}
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Open original source →
                </a>
            )}
        </article>
    );
}